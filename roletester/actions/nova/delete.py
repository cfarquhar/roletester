from roletester.log import logging

logger = logging.getLogger('roletester.actions.nova.delete')


def delete(clients, context):
    """Deletes random server.

    :param clients: roletester.clients.ClientManager
    :param conf: Dict
    """
    logger.info("Taking action delete")
    nova = clients.get_nova()
    server_id = context['server_id']
    logger.info("Deleting {0} ...".format(server_id))
    nova.servers.delete(server_id)
