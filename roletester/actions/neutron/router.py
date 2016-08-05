"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.router')


def add_interface(clients, context):
    """Adds a router interface to a subnet

    Uses context['subnet_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    router_id = context['router_id']
    subnet_id = context['subnet_id']
    logger.info("Taking action router.add_interface {}".format(router_id))
    neutron = clients.get_neutron()
    body = {
        "subnet_id": subnet_id
    }
    neutron.add_interface_router(router_id, body=body)


def create(clients, context, name, external_network_id):
    """Create a router

    Sets context['router_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the new router
    :type name: String
    :param external_network_id: Id of the external network
    :type external_network_id: String
    """
    logger.info("Taking action router.create{}.".format(name))
    neutron = clients.get_neutron()
    body = {
        "router": {
            "name": name,
            "external_gateway_info": {
                "network_id": external_network_id
            }
        }
    }
    resp = neutron.create_router(body=body)
    router = resp['router']
    context['router_id'] = router['id']
    context.setdefault('stack', []).append({'router_id': router['id']})


def delete(clients, context):
    """Deletes a router.

    Uses context['router_id']
    Removes context['router_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    router_id = context['router_id']
    logger.info("Taking action router.delete {}".format(router_id))
    neutron = clients.get_neutron()
    neutron.delete_router(router_id)
    context.pop('router_id')


def remove_interface(clients, context):
    """Remove an interface from a router

    Uses context['router_id']
    Uses context['subnet_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    router_id = context['router_id']
    subnet_id = context['subnet_id']
    logger.info("Taking action router.remove_interface.")
    neutron = clients.get_neutron()
    body = {
        "subnet_id": subnet_id
    }
    neutron.remove_interface_router(router_id, body=body)


def show(clients, context):
    """Shows info for a specific router.

    Uses context['router_id']
    Sets router['name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    router_id = context['router_id']
    logger.info("Taking action router.show {}".format(router_id))
    neutron = clients.get_neutron()
    resp = neutron.show_router(router_id)
    router = resp['router']
    context['router_name'] = router['name']
    context['router_status'] = router['status']


def update(clients, context, name=None):
    """Update properties of a router.

    Uses context['router_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Optional new name of router
    :type name: String
    """
    router_id = context['router_id']
    logger.info("Taking action router.update {}.".format(router_id))
    neutron = clients.get_neutron()
    body = {'router': {}}
    if name is not None:
        body['router']['name'] = name
    neutron.update_router(router_id, body=body)
