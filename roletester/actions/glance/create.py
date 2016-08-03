from roletester import utils
from roletester.log import logging

logger = logging.getLogger('roletester.actions.glance.create')


def create(clients, conf=None):
    """Creates a glance image

    :param clients: roletester.clients.Clientmanager
    :param conf: Dict
    """
    logger.info("Taking action image_create")
    if conf is None:
        conf = {}
    glance_conf = conf.get('glance', {})
    glance = clients.get_glance()

    name = utils.randomname(prefix='random-image')
    imagedict = utils.randomfromlist(glance_conf.get('images'))
    kwargs = {
        'name': name,
        'disk_format': imagedict.get('disk_format'),
        'container_format': imagedict.get('container_format'),
        'app_id': 'roletester'
    }
    possible_metadata = glance_conf.get('metadata', {})
    for metakey, valuelist in possible_metadata.items():
        kwargs[metakey] = utils.randomfromlist(valuelist)

    image = glance.images.create(**kwargs)

    glance.images.upload(image.id, open(imagedict.get('file'), 'rb'))
    logger.info("Created image {0}".format(image.name))

    # Add a tag to identify image as one created by roletester
    # tag = 'roletester'
    # glance.image_tags.update(image.id, 'roletester')

    # Randomly sample from available random tags
    # extra_tags = utils.randomsample(glance_conf.get('tags', []), 2)
    # for t in extra_tags:
    #    glance.image_tags.update(image.id, t)
