"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.port')


def create(clients, context, name):
    """Create a port

    Uses context['network_id']
    Sets context['port_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the new port
    :type name: String
    """
    network_id = context['network_id']
    logger.info("Taking action port.create_for_server{}.".format(name))
    neutron = clients.get_neutron()
    body = {
        "port": {
            "network_id": network_id,
            "name": name
        }
    }
    resp = neutron.create_port(body=body)
    port = resp['port']
    context['port_id'] = port['id']


def delete(clients, context):
    """Deletes a port.

    Uses context['port_id']
    Removes context['port_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    port_id = context['port_id']
    logger.info("Taking action port.delete {}".format(port_id))
    neutron = clients.get_neutron()
    neutron.delete_port(port_id)
    context.pop('port_id')


def show(clients, context):
    """Shows info for a specific port.

    Uses context['port_id']
    Sets port['name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    port_id = context['port_id']
    logger.info("Taking action port.show {}".format(port_id))
    neutron = clients.get_neutron()
    resp = neutron.show_port(port_id)
    port = resp['port']
    context['port_name'] = port['name']
    context['port_status'] = port['status']


def update(clients, context, name=None):
    """Update properties of a port.

    Uses context['port_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Optional new name of port
    :type name: String
    """
    port_id = context['port_id']
    logger.info("Taking action port.update {}.".format(port_id))
    neutron = clients.get_neutron()
    body = {'port': {}}
    if name is not None:
        body['port']['name'] = name
    neutron.update_port(port_id, body=body)
