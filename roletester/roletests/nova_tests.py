from base import Base as BaseTestCase
from roletester.actions.glance import image_create
from roletester.actions.glance import image_delete
from roletester.actions.glance import image_wait_for_status
from roletester.actions.nova import interface_attach
from roletester.actions.nova import interface_detach
from roletester.actions.nova import server_create
from roletester.actions.nova import server_update
from roletester.actions.nova import server_delete
from roletester.actions.nova import server_list
from roletester.actions.nova import server_show
from roletester.actions.nova import server_create_image
from roletester.actions.nova import server_wait_for_status
from roletester.actions.neutron import network_create
from roletester.actions.neutron import network_delete
from roletester.actions.neutron import port_create
from roletester.actions.neutron import port_delete
from roletester.actions.neutron import subnet_create
from roletester.actions.neutron import subnet_delete
from roletester.exc import NovaNotFound
from roletester.exc import GlanceNotFound
from roletester.exc import GlanceUnauthorized
from roletester.exc import KeystoneUnauthorized
from roletester.scenario import ScenarioFactory as Factory
from roletester.utils import randomname

from roletester.log import logging

logger = logging.getLogger("roletester.test_sample")


class SampleFactory(Factory):

    _ACTIONS = [
        image_create,
        image_wait_for_status,
        server_create,
        server_wait_for_status,
        server_show,
        server_update,
        server_create_image,
        image_wait_for_status,
        image_delete,
        network_create,
        subnet_create,
        port_create,
        interface_attach,
        interface_detach,
        server_delete
    ]

    IMAGE_CREATE = 0
    IMAGE_WAIT = 1
    SERVER_CREATE = 2
    SERVER_WAIT = 3
    SERVER_SHOW = 4
    SERVER_UPDATE = 5
    SERVER_CREATE_IMAGE = 6
    SERVER_IMAGE_WAIT = 7
    SERVER_IMAGE_DELETE = 8 
    NETWORK_CREATE = 9
    SUBNET_CREATE = 10
    PORT_CREATE = 11
    INTERFACE_ATTACH = 12
    INTERFACE_DETACH = 13
    SERVER_DELETE = 14

class SnapFactory(Factory):

    _ACTIONS = [
        image_create,
        image_wait_for_status,
        server_create,
        server_wait_for_status,
        server_show,
        server_update,
        server_create_image,
    ]

    IMAGE_CREATE = 0
    IMAGE_WAIT = 1
    SERVER_CREATE = 2
    SERVER_WAIT = 3
    SERVER_SHOW = 4
    SERVER_UPDATE = 5
    SERVER_CREATE_IMAGE = 6
   

class NetworkPortFactory(Factory):

    _ACTIONS = [
        image_create,
        image_wait_for_status,
        server_create,
        server_wait_for_status,
        network_create,
        subnet_create,
        port_create,
    ]

    IMAGE_CREATE = 0
    IMAGE_WAIT = 1
    SERVER_CREATE = 2
    SERVER_WAIT = 3
    NETWORK_CREATE = 4
    SUBNET_CREATE = 5
    PORT_CREATE = 6
    INTERFACE_ATTACH = 7
    INTERFACE_DETACH = 8
    SERVER_DELETE = 9

class NetworkAttachInterfaceFactory(Factory):

    _ACTIONS = [
        image_create,
        image_wait_for_status,
        server_create,
        server_wait_for_status,
        network_create,
        subnet_create,
        port_create,
        interface_attach,
    ]

    IMAGE_CREATE = 0
    IMAGE_WAIT = 1
    SERVER_CREATE = 2
    SERVER_WAIT = 3
    NETWORK_CREATE = 4
    SUBNET_CREATE = 5
    PORT_CREATE = 6
    INTERFACE_ATTACH = 7

class NetworkDetachInterfaceFactory(Factory):

    _ACTIONS = [
        image_create,
        image_wait_for_status,
        server_create,
        server_wait_for_status,
        network_create,
        subnet_create,
        port_create,
        interface_attach,
        interface_detach,
        server_delete
    ]

    IMAGE_CREATE = 0
    IMAGE_WAIT = 1
    SERVER_CREATE = 2
    SERVER_WAIT = 3
    NETWORK_CREATE = 4
    SUBNET_CREATE = 5
    PORT_CREATE = 6
    INTERFACE_ATTACH = 7
    INTERFACE_DETACH = 8
    SERVER_DELETE = 9

class TestSample(BaseTestCase):

    name = 'scratch'
    flavor = '1'
    image_file = '/Users/chalupaul/cirros-0.3.4-x86_64-disk.img'
    project = randomname()

    def test_cloud_admin_all_cloud_admin_user(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        cloud_admin = self.km.find_user_credentials('Default', self.project, 'admin')
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SampleFactory(cloud_admin) \
            .set(SampleFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,), 
                 kwargs={'visibility': 'public'}) \
            .set(SampleFactory.IMAGE_WAIT, clients=creator) \
            .set(SampleFactory.SERVER_IMAGE_WAIT, 
                  clients=creator, 
                  kwargs=server_image_kwargs) \
            .set(SampleFactory.SERVER_IMAGE_DELETE, 
                 kwargs=server_image_kwargs) \
            .set(SampleFactory.NETWORK_CREATE, clients=creator) \
            .set(SampleFactory.SUBNET_CREATE, clients=creator) \
            .produce() \
            .run(context=self.context)

    def test_cloud_admin_same_domain_different_user(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        cloud_admin = self.km.find_user_credentials('Default', self.project, 'admin')
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SampleFactory(cloud_admin) \
            .set(SampleFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(SampleFactory.IMAGE_WAIT, clients=creator) \
            .set(SampleFactory.SERVER_CREATE, clients=user1) \
            .set(SampleFactory.SERVER_WAIT, clients=user1) \
            .set(SampleFactory.SERVER_IMAGE_WAIT, 
                  kwargs=server_image_kwargs) \
            .set(SampleFactory.SERVER_IMAGE_DELETE, 
                 clients=creator,
                 kwargs=server_image_kwargs) \
            .set(SampleFactory.NETWORK_CREATE, clients=creator) \
            .set(SampleFactory.SUBNET_CREATE, clients=creator) \
            .produce() \
            .run(context=self.context)
            
    def test_cloud_admin_different_domain_different_user(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        cloud_admin = self.km.find_user_credentials('Default', self.project, 'admin') #TODO this should work with Domain2
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SampleFactory(cloud_admin) \
            .set(SampleFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(SampleFactory.IMAGE_WAIT, clients=creator) \
            .set(SampleFactory.SERVER_CREATE, clients=user1) \
            .set(SampleFactory.SERVER_WAIT, clients=user1) \
            .set(SampleFactory.SERVER_IMAGE_WAIT, 
                  kwargs=server_image_kwargs) \
            .set(SampleFactory.SERVER_IMAGE_DELETE, 
                 clients=creator,
                 kwargs=server_image_kwargs) \
            .set(SampleFactory.NETWORK_CREATE, clients=creator) \
            .set(SampleFactory.SUBNET_CREATE, clients=creator) \
            .produce() \
            .run(context=self.context)
            
    def test_bu_admin_all_cloud_admin_user(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        bu_admin = self.km.find_user_credentials('Default', self.project, 'admin')
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SampleFactory(bu_admin) \
            .set(SampleFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,), 
                 kwargs={'visibility': 'public'}) \
            .set(SampleFactory.IMAGE_WAIT, clients=creator) \
            .set(SampleFactory.SERVER_IMAGE_WAIT, 
                  clients=creator, 
                  kwargs=server_image_kwargs) \
            .set(SampleFactory.SERVER_IMAGE_DELETE, 
                 kwargs=server_image_kwargs) \
            .set(SampleFactory.NETWORK_CREATE, clients=creator) \
            .set(SampleFactory.SUBNET_CREATE, clients=creator) \
            .produce() \
            .run(context=self.context)

    def test_bu_admin_same_domain_different_user(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        bu_admin = self.km.find_user_credentials('Default', self.project, 'admin')
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SampleFactory(bu_admin) \
            .set(SampleFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(SampleFactory.IMAGE_WAIT, clients=creator) \
            .set(SampleFactory.SERVER_CREATE, clients=user1) \
            .set(SampleFactory.SERVER_WAIT, clients=user1) \
            .set(SampleFactory.SERVER_IMAGE_WAIT, 
                  kwargs=server_image_kwargs) \
            .set(SampleFactory.SERVER_IMAGE_DELETE, 
                 clients=creator,
                 kwargs=server_image_kwargs) \
            .set(SampleFactory.NETWORK_CREATE, clients=creator) \
            .set(SampleFactory.SUBNET_CREATE, clients=creator) \
            .produce() \
            .run(context=self.context)
   
            
    def test_bu_admin_different_domain_different_user_server_and_snapshot(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        bu_admin = self.km.find_user_credentials('Domain2', self.project, 'admin') #TODO this should work with Domain2
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        SnapFactory(bu_admin) \
            .set(SnapFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(SnapFactory.IMAGE_WAIT, clients=creator) \
            .set(SnapFactory.SERVER_CREATE, clients=user1) \
            .set(SnapFactory.SERVER_WAIT, clients=user1) \
            .set(SnapFactory.SERVER_SHOW, 
                 expected_exceptions=[KeystoneUnauthorized]) \
            .set(SnapFactory.SERVER_UPDATE, 
                 expected_exceptions=[KeystoneUnauthorized]) \
            .set(SnapFactory.SERVER_CREATE_IMAGE, 
                 expected_exceptions=[KeystoneUnauthorized]) \
            .produce() \
            .run(context=self.context)
           
    def test_bu_admin_different_domain_different_user_network(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        bu_admin = self.km.find_user_credentials('Domain2', self.project, 'admin') #TODO this should work with Domain2
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        NetworkPortFactory(bu_admin) \
            .set(SnapFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(NetworkPortFactory.IMAGE_WAIT, clients=creator) \
            .set(NetworkPortFactory.SERVER_CREATE, clients=user1) \
            .set(NetworkPortFactory.SERVER_WAIT, clients=user1) \
            .set(NetworkPortFactory.NETWORK_CREATE, clients=creator) \
            .set(NetworkPortFactory.SUBNET_CREATE, clients=creator) \
            .set(NetworkPortFactory.PORT_CREATE,
                 expected_exceptions=[KeystoneUnauthorized]) \
            .produce() \
            .run(context=self.context)
    def test_bu_admin_different_domain_different_user_attach_interface(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        bu_admin = self.km.find_user_credentials('Domain2', self.project, 'admin') #TODO this should work with Domain2
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        NetworkAttachInterfaceFactory(bu_admin) \
            .set(SnapFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(NetworkAttachInterfaceFactory.IMAGE_WAIT, clients=creator) \
            .set(NetworkAttachInterfaceFactory.SERVER_CREATE, clients=user1) \
            .set(NetworkAttachInterfaceFactory.SERVER_WAIT, clients=user1) \
            .set(NetworkAttachInterfaceFactory.NETWORK_CREATE, clients=creator) \
            .set(NetworkAttachInterfaceFactory.SUBNET_CREATE, clients=creator) \
            .set(NetworkAttachInterfaceFactory.PORT_CREATE,
                 clients=creator) \
            .set(NetworkAttachInterfaceFactory.INTERFACE_ATTACH,
                 expected_exceptions=[KeystoneUnauthorized]) \
            .produce() \
            .run(context=self.context)
            
    def test_bu_admin_different_domain_different_user_detach_interface(self):
        creator = self.km.find_user_credentials('Default', self.project, 'admin')
        user1 = self.km.find_user_credentials('Default', self.project, '_member_')
        bu_admin = self.km.find_user_credentials('Domain2', self.project, 'admin') #TODO this should work with Domain2
        
        server_image_kwargs = {'image_key': 'server_image_id'}
        NetworkDetachInterfaceFactory(bu_admin) \
            .set(SnapFactory.IMAGE_CREATE, 
                 clients=creator, 
                 args=(self.image_file,),
                 kwargs={'visibility': 'public'}) \
            .set(NetworkDetachInterfaceFactory.IMAGE_WAIT, clients=creator) \
            .set(NetworkDetachInterfaceFactory.SERVER_CREATE, clients=user1) \
            .set(NetworkDetachInterfaceFactory.SERVER_WAIT, clients=user1) \
            .set(NetworkDetachInterfaceFactory.NETWORK_CREATE, clients=creator) \
            .set(NetworkDetachInterfaceFactory.SUBNET_CREATE, clients=creator) \
            .set(NetworkDetachInterfaceFactory.PORT_CREATE,
                 clients=creator) \
            .set(NetworkDetachInterfaceFactory.INTERFACE_ATTACH,
                 clients=creator) \
            .set(NetworkDetachInterfaceFactory.INTERFACE_DETACH,
                 expected_exceptions=[KeystoneUnauthorized]) \
            .set(NetworkDetachInterfaceFactory.SERVER_DELETE,
                 expected_exceptions=[KeystoneUnauthorized]) \
            .produce() \
            .run(context=self.context)
       
            
            
