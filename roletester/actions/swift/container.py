"""Module containing actions to manage swift containers."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.swift.container')


def create(clients, context,
           name="test_container"):
    """Create a container

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the new container
    :type name: String
    """
    logger.info("Taking action container.create {}.".format(name))
    swift = clients.get_swift()
    swift.put_container(name)

####

def delete(clients, context):
    """Deletes a subnet.

    Uses context['subnet_id']
    Removes context['subnet_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    subnet_id = context['subnet_id']
    logger.info("Taking action subnet.delete {}".format(subnet_id))
    neutron = clients.get_neutron()
    neutron.delete_subnet(subnet_id)
    context.pop('subnet_id')


def show(clients, context):
    """Shows info for a specific subnet.

    Uses context['subnet_id']
    Sets subnet['name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    subnet_id = context['subnet_id']
    logger.info("Taking action subnet.show {}".format(subnet_id))
    neutron = clients.get_neutron()
    resp = neutron.show_subnet(subnet_id)
    subnet = resp['subnet']
    context['subnet_name'] = subnet['name']


def update(clients, context, name=None):
    """Update properties of a subnet.

    Uses context['subnet_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Optional new name of subnet
    :type name: String
    """
    subnet_id = context['subnet_id']
    logger.info("Taking action subnet.update {}.".format(subnet_id))
    neutron = clients.get_neutron()
    body = {'subnet': {}}
    if name is not None:
        body['subnet']['name'] = name
    neutron.update_subnet(subnet_id, body=body)
