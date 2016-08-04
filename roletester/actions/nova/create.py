"""Module containing action to create a nova server."""
from roletester import utils
from roletester.log import logging

logger = logging.getLogger('roletester.actions.nova.create')


def create(clients, context, name, flavor, image):
    """Creates server with random image and flavor.

    :param clients: roletester.clients.ClientManager
    :param conf: Configuration
    """
    logger.info("Taking action create")
    nova = clients.get_nova()
    flavor = nova.flavors.get(flavor)
    image = nova.images.get(image)
    server = nova.servers.create(name, image, flavor)
    context.update({'server_id': server.id})
    logger.info("Created server {}".format(name))
