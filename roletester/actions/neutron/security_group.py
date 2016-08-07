"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.security_group')


def _manage_server_security_group(clients, context, direction):
    """add/remove security group from server
    
    Uses context['server_id']
    Uses context['security_group_id']
    
    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param direction: add|remove
    :type direction: String
    """
    server_id = context['server_id']
    neutron = clients.get_neutron()

    resp = neutron.list_ports(device_id=server_id)

    security_group_id = context['security_group_id']
    port_id = resp['ports'][0]['id']
    security_groups = resp['ports'][0]['security_groups']
    if direction == 'add':
        security_groups.append(security_group_id)
    elif direction == 'remove':
        security_groups = [x 
                           for x in security_groups
                           if x != security_group_id]
    else:
        raise ValueError('security group direction must be `add` or `remove`')

    body = {
        'port': {
            'security_groups': security_groups
        }
    }
    resp = neutron.update_port(port_id, body)

def add_to_server(clients, context):
    """Add security group to server

    Finds the first port with matching server id

    Uses context['server_id']
    Uses context['security_group_id']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    logger.debug("Taking action security_group.add_to_server")
    _manage_server_security_group(clients, context, 'add')

def remove_from_server(clients, context):
    """Removes a security group from server.
    
    Finds the first port with matching server id
    
    Uses context['server_id']
    Uses context['security_group_id']
    
    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    logger.debug("Taking action security_group.remove_from_server")
    _manage_server_security_group(clients, context, 'remove')

def create(clients, context, name='test secgroup', description=None):
    """Create a security group.

    Sets context['security_group_id']
    Sets context['security_group_name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the security group
    :type name: String
    :param description: Description of the group.
    :type description: String
    """
    logger.debug("Taking action security_group.create")
    body = {
        'security_group': {
            'name': name
        }
    }
    if description:
        body['security_group']['description'] = description

    neutron = clients.get_neutron()
    resp = neutron.create_security_group(body)
    security_group = resp['security_group']
    context.update(security_group_name=security_group['name'])
    context.update(security_group_id=security_group['id'])
    context.setdefault('stacks', []).append(
        {'security_group_id': security_group['id']}
    )


def delete(clients, context):
    """Deletes a security group.

    Uses context['security_group_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object.
    :type context: Dict
    """
    logger.debug("Taking action security_group.delete")
    neutron = clients.get_neutron()
    security_group_id = context['security_group_id']
    neutron.delete_security_group(security_group_id)


def list(clients, context):
    """Creates server with random image and flavor.

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object.
    :type context: Dict
    """
    logger.debug("Taking action security_group.list")
    neutron = clients.get_neutron()
    groups = neutron.list_security_groups()
    context.update({'security_groups': groups})


def show(clients, context):
    """Retrieves information for a security group.

    Uses context['security_group_id']

    :param clients: ClientManager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object.
    :type context: Dict
    """
    logger.debug("Taking action security_group.show")
    neutron = clients.get_neutron()
    group = neutron.show_security_group(context['security_group_id'])
    context.update({'security_group': group})


def update(clients, context, name=None, description=None):
    """Update the name and/or description.

    Uses context['security_group_id']

    :param clients: ClientManager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object.
    :type context: Dict
    :param name: New name of the security group.
    :type name: String
    :param description: New description of the security group.
    :type description: String
    """
    logger.debug("Taking action security_group_update")
    neutron = clients.get_neutron()

    body = {'security_group': {}}
    if name:
        body['security_group']['name'] = name
    if description:
        body['security_group']['description'] = description

    security_group_id = context['security_group_id']

    resp = neutron.update_security_group(security_group_id, body)
    security_group = resp['security_group']
    context.update(security_group_name=security_group['name'])
    context.update(security_group_id=security_group['id'])
