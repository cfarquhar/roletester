"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.network')


def create(clients, context, name='test network', project_id=None):
    """Create a network

    Sets context['network_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the new network
    :type name: String
    :param project_id: Optional id of another tenant/project
    :type project_id: String
    """
    logger.info("Taking action network.create {}.".format(name))
    neutron = clients.get_neutron()
    body = {
        "network": {
            "name": name
        }
    }
    if project_id is not None:
        body['network']['tenant_id'] = project_id

    resp = neutron.create_network(body=body)
    network = resp['network']
    context['network_id'] = network['id']
    context.setdefault('stack', []).append({'network_id': network['id']})


def delete(clients, context):
    """Deletes a network.

    Uses context['network_id']
    Removes context['network_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    network_id = context['network_id']
    logger.info("Taking action network.delete {}".format(network_id))
    neutron = clients.get_neutron()
    neutron.delete_network(network_id)
    context.pop('network_id')


def show(clients, context):
    """Shows info for a specific network.

    Uses context['network_id']
    Sets network['status']
    Sets network['name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    network_id = context['network_id']
    logger.info("Taking action network.show {}".format(network_id))
    neutron = clients.get_neutron()
    resp = neutron.show_network(network_id)
    network = resp['network']
    context['network_status'] = network['status']
    context['network_subnets'] = network['subnets']
    context['network_name'] = network['name']


def update(clients, context, name=None, admin_state_up=None):
    """Update properties of a network.

    Uses context['network_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Optional new name of network
    :type name: String
    :param admin_state_up: Optional admin state up
    :type admin_state_up: Boolean
    """
    network_id = context['network_id']
    logger.info("Taking action network.update {}.".format(network_id))
    neutron = clients.get_neutron()
    body = {'network': {}}
    if name is not None:
        body['network']['name'] = name
    if admin_state_up is not None:
        body['network']['admin_state_up'] = admin_state_up
    neutron.update_network(network_id, body=body)
