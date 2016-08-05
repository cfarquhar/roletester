from roletester import utils
from roletester.log import logging

logger = logging.getLogger('roletester.actions.glance.image')


def create(clients, 
           context, 
           image_file,
           name="glance test image", 
           disk_format='qcow2', 
           container_format='bare'):
    """Creates a glance image

    Uses context['image_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    :param image_file: File path to image file you are uploading
    :type image_file: String
    :param name: Image name
    :type name: String
    :param disk_format: Glance disk file format
    :type disk_format: String
    :param container_format: Image container format
    :type container_format: String
    """
    logger.info("Taking action image_create")

    kwargs = {
        'name': name,
        'disk_format': disk_format,
        'container_format': container_format,
    }

    image = glance.images.create(**kwargs)

    glance.images.upload(image.id, open(imagedict.get('file'), 'rb'))
    logger.info("Created image {0}".format(image.name))

def delete(clients, context):
    """Deletes an image from Glance.

    Uses context['image_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    image_id = context['image_id']
    logger.info("Deleting image %s" % image_id)
    glance = clients.get_glance()
    image = glance.images.get(image_id)

    glance.images.delete(image.id)
    logger.info("Deleted image %s" % image.name)
    
def show(clients, context):
    """Shows a glance image.
    
    Uses context['image_id']
    Sets context['image_status']
    
    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    image_id = context['image_id']
    logger.info("Showing image %s" %image_id)
    image = clients.get_glance().images.get(image_id)
    logger.debug("Image info %s: name: %s status: %s" %(image.id, 
                                                            image.name, 
                                                            image.status))
    context.update(image_status=image.status)

    
def list(clients, context):
    """Lists glance images
    
    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    glance = clients.get_glance()
    logger.info("Listing all images.")
    images = [x.name for x in glance.images.list()] # It's a generator
    log_template = "Images listing: " + ', '.join(["%s"] * len(images))
    logger.debug(log_template % tuple(images))
