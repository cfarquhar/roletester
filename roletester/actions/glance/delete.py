from roletester import utils
from roletester.log import logging

logger = logging.getLogger('roletester.actions.glance.delete')


def delete(clients, conf=None):
    """Deletes a random image created by roletester.

    :param clients: roletester.clients.ClientManager
    :param conf: Dict
    """
    logger.info("Taking action delete")
    glance = clients.get_glance()
    if conf is None:
        conf = {}

    image_gen = glance.images.list(filters={'tag': ['roletester']})
    images = [i for i in image_gen]
    if not images:
        logger.info("Nothing to delete")
        return

    image = utils.randomfromlist(images)
    glance.images.delete(image.id)
    logger.info("Deleted image {0}".format(image.name))
