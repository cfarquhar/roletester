"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.floatingip')


def associate(clients, context):
    """Assocuate a floating ip with a port.

    Uses context['floatingip_id']
    Uses context['port_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    floatingip_id = context['floatingip_id']
    port_id = context['port_id']
    logger.info('Taking action floatingip.associate')
    neutron = clients.get_neutron()
    body = {
        'floatingip': {
            'port_id': port_id
        }
    }
    neutron.update_floatingip(floatingip_id, body=body)


def create(clients, context, floating_network_id, project_id=None):
    """Create a floatingip

    Sets context['floatingip_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param floating_network_id: id of the floating network
    :type name: String
    :param project_id: Optional id of another tenant/project
    :type project_id: String
    """
    logger.info("Taking action floatingip.create.")
    neutron = clients.get_neutron()
    body = {
        "floatingip": {
            "floating_network_id": floating_network_id
        }
    }
    if project_id is not None:
        body['floatingip']['tenant_id'] = project_id
    resp = neutron.create_floatingip(body=body)
    floatingip = resp['floatingip']
    context['floatingip_id'] = floatingip['id']
    context.setdefault('stack', []).append({'floatingip_id': floatingip['id']})


def delete(clients, context):
    """Deletes a floatingip.

    Uses context['floatingip_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    floatingip_id = context['floatingip_id']
    logger.info("Taking action floatingip.delete {}".format(floatingip_id))
    neutron = clients.get_neutron()
    neutron.delete_floatingip(floatingip_id)


def disassociate(clients, context):
    """Assocuate a floating ip with a port.

    Uses context['floatingip_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    floatingip_id = context['floatingip_id']
    logger.info('Taking action floatingip.associate')
    neutron = clients.get_neutron()
    body = {
        'floatingip': {
            'port_id': None
        }
    }
    neutron.update_floatingip(floatingip_id, body=body)


def show(clients, context):
    """Shows info for a specific floatingip.

    Uses context['floatingip_id']
    Sets floatingip['status']
    Sets floatingip['name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    floatingip_id = context['floatingip_id']
    logger.info("Taking action floatingip.show {}".format(floatingip_id))
    neutron = clients.get_neutron()
    resp = neutron.show_floatingip(floatingip_id)
    floatingip = resp['floatingip']
    context['floatingip_status'] = floatingip['status']
