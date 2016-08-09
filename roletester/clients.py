import os
from keystoneauth1 import session
from keystoneauth1.identity import v3
from cinderclient import client as cinderclient
from novaclient import client as novaclient
from glanceclient import Client as glanceclient
from keystoneclient import client as keystoneclient
from neutronclient.v2_0 import client as neutronclient
from swiftclient import client as swiftclient


class ClientManager(object):
    """Object that manages multiple openstack clients.

    Operates with the intention of sharing one keystone auth session.
    """
    def __init__(self, **auth_kwargs):
        """Inits the client manager.

        :param auth_url: String keystone auth url
        :param username: String openstack username
        :param password: String openstack password
        :param project_id: String project_id - Tenant uuid
        """
        self.project_session = None
        self.domain_session = None
        self.neutron = None
        self.nova = None
        self.glance = None
        self.cinder = None
        self.swift = None
        self.keystone = None
        self.auth_kwargs = auth_kwargs

    def get_session(self, scope='project'):
        """Get a keystone auth session.

        :param scope: Sets the scope you get back from Session.
        :returns: keystoneauth1.session.Session
        """
        return_session = None
        if scope == 'project':
            if self.project_session is None:
                # loader = loading.get_plugin_loader('password')
                # auth = loader.load_from_options(**self.auth_kwargs)
                auth = v3.Password(**self.auth_kwargs)
                self.project_session = session.Session(auth=auth)
            return_session = self.project_session
        elif scope == 'domain':
            if self.domain_session is None:
                scoped_kwargs = {x: y 
                                 for x,y in self.auth_kwargs.items()
                                 if x is not 'project_name'}
                auth = v3.Password(**scoped_kwargs)
                self.domain_session = session.Session(auth)
            return_session = self.domain_session
        else:
            raise ValueError("scope must be either `domain` or `project`.")
        return return_session

    def get_nova(self, version='2.1', scope='project'):
        """Get a nova client instance.

        :param version: String api version
        :returns: novaclient.client.Client
        """
        if self.nova is None:
            sess = self.get_session(scope=scope)
            self.nova = novaclient.Client(version, session=sess)
        return self.nova

    def get_neutron(self, version='2', scope='project'):
        """Get a neutron client instance.

        :param version: String api version
        :returns: neutronclient.v2_0.client.Client
        """
        if self.neutron is None:
            sess = self.get_session(scope=scope)
            self.neutron = neutronclient.Client(session=sess)
        return self.neutron

    def get_glance(self, version='2', scope='project'):
        """Get a glance client instance.

        :param version: String api version
        :return: glanceclient.Client
        """
        if self.glance is None:
            sess = self.get_session(scope=scope)
            self.glance = glanceclient(version, session=sess)
        return self.glance

    def get_cinder(self, version='2', scope='project'):
        """Get a cinder client instance.

        :param version: String api version
        :return: cinderclient.client.Client
        """
        if self.cinder is None:
            sess = self.get_session(scope=scope)
            iface = os.getenv('OS_ENDPOINT_TYPE', "public")
            self.cinder = cinderclient.Client(version,
                                              session=sess,
                                              interface=iface)
        return self.cinder

    def get_swift(self):
        """Get a swift client.Connection instance.

        :return: swiftclient.client.Connection
        """
        if self.swift is None:
            self.swift = swiftclient.Connection(
                auth_version='3',
                authurl=self.auth_kwargs["auth_url"],
                user=self.auth_kwargs["username"],
                key=self.auth_kwargs["password"],
                tenant_name=self.auth_kwargs["project_name"]
            )
        return self.swift

    def get_keystone(self, version='3', scope='domain'):
        """Get a keystone client instance.

        :param scope: You *probably* want a domain scope, but can override.
        :param version: String api version
        :return: keystoneClient.Client
        """
        if self.keystone is None:
            iface = os.getenv('OS_ENDPOINT_TYPE', "public")
            self.keystone = keystoneclient.Client(
                version=version,
                session=self.get_session(scope=scope),
                interface=iface)
        return self.keystone
