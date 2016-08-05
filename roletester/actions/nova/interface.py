from roletester.log import logging

logger = logging.getLogger('roletester.actions.nova.volume')


def attach(clients, context):
    """Creates an interface for a server and port.

    Uses context['server_id']
    Uses context['port_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    port_id = context['port_id']
    server_id = context['server_id']
    logger.info("Taking action interface.attach")
    nova = clients.get_nova()

    nova.servers.interface_attach(server_id, port_id, None, None)


def detach(clients, context):
    """Detaches a an interface for server and port.

    Uses context['server_id']
    Uses context['port_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    server_id = context['server_id']
    port_id = context['port_id']
    logger.info("Taking action interface.delete")
    nova = clients.get_nova()
    nova.servers.interface_detach(server_id, port_id)
