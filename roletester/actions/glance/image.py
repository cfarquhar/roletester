<<<<<<< HEAD
from roletester import utils
from roletester.log import logging
=======
import time
from roletester.exc import GlanceNotFound
from roletester.log import logging
import time
>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901

logger = logging.getLogger('roletester.actions.glance.image')


<<<<<<< HEAD
def create(clients, 
           context, 
           image_file,
           name="glance test image", 
           disk_format='qcow2', 
=======
def create(clients,
           context,
           image_file,
           name="glance test image",
           disk_format='qcow2',
>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
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
    glance = clients.get_glance()
    image = glance.images.create(**kwargs)
    context.update(image_id=image.id)
<<<<<<< HEAD
=======
    context.setdefault('stack', []).append({'image_id': image.id})
>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901

    glance.images.upload(image.id, open(image_file, 'rb'))
    logger.info("Created image {0}".format(image.name))

<<<<<<< HEAD
=======

>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
def delete(clients, context, external_id=None):
    """Deletes an image from Glance.

    Uses context['image_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    :param external_id: Image id to delete (optional)
    :type external_id: String
<<<<<<< HEAD
    

    """
    def delete_image(id):
        """*Actually* deletes an image from Glance.
        
        Because delete controls for any image made by other services
        are handled by glance, we need a way to cleanup any image. Excluding
        the external_id param will default to context['image_id']
        
=======
    """
    def delete_image(id):
        """*Actually* deletes an image from Glance.

        Because delete controls for any image made by other services
        are handled by glance, we need a way to cleanup any image. Excluding
        the external_id param will default to context['image_id']

>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
        :param id: Image id to be deleted
        :type id: String
        """
        glance = clients.get_glance()
        image = glance.images.get(id)
        logger.info("Deleting image %s" % image.id)
        glance.images.delete(image.id)
        logger.info("Deleted image %s" % image.id)
<<<<<<< HEAD
    
    if external_id == None:
=======

    if external_id is None:
>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
        image_id = context['image_id']
        delete_image(image_id)
        context.pop('image_id')
    else:
        delete_image(external_id)


def show(clients, context):
    """Shows a glance image.
<<<<<<< HEAD
    
    Uses context['image_id']
    Sets context['image_status']
    
=======

    Uses context['image_id']
    Sets context['image_status']

>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    image_id = context['image_id']
<<<<<<< HEAD
    logger.info("Showing image %s" %image_id)
    image = clients.get_glance().images.get(image_id)
    logger.debug("Image info \"%s\": name: \"%s\" status: \"%s\"" %(image.id, 
                                                            image.name, 
                                                            image.status))
    context.update(image_status=image.status.lower())

    
def list(clients, context):
    """Lists glance images
    
=======
    logger.info("Showing image %s" % image_id)
    image = clients.get_glance().images.get(image_id)
    logger.debug(
        'Image info "%s": name: "%s" status: "%s"' %
        (image.id, image.name, image.status)
    )
    context.update(image_status=image.status.lower())


def list(clients, context):
    """Lists glance images

>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    glance = clients.get_glance()
    logger.info("Listing all images.")
<<<<<<< HEAD
    images = [x.name for x in glance.images.list()] # It's a generator
=======
    # It's a generator
    images = [x.name for x in glance.images.list()]
>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
    log_template = "Images listing: " + ', '.join(["\"%s\""] * len(images))
    logger.debug(log_template % tuple(images))


# Statuses that indicate a terminating status
_DONE_STATUS = set(['active', 'killed', 'deleted'])

<<<<<<< HEAD
=======

>>>>>>> d55e034bd57923da45ecbe0d27628768ea0c9901
def wait_for_status(admin_clients,
                    context,
                    timeout=60,
                    interval=5,
                    initial_wait=None,
                    target_status='active'):
    """Waits for a image to go to a request status.

    Uses context['image_id']
    Uses context['image_status']

    :param admin_clients: Client manager
    :type admin_clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    :param timeout: Timeout in seconds.
    :type timeout: Integer
    :param interval: Time in seconds to wait between polls.
    :type timeout: Integer
    :param initial_wait: Time in seconds to wait before beginning to poll.
        Useful for expecting a server that is ACTIVE to go to DELETED
    :type initial_wait: Integer
    :param target_status: Status to wait for. If desired status is DELETED,
        a NotFoundException will be allowed.
    :type target_status: String
    """
    logger.info("Taking action wait for image")

    if initial_wait:
        time.sleep(initial_wait)

    start = time.time()
    try:
        while (time.time() - start < timeout):
            show(admin_clients, context)
            status = context['image_status']
            logger.debug("Found status {}".format(status))
            if status == target_status:
                context.pop('image_status')
                break
            if status in _DONE_STATUS:
                raise Exception(
                    "Was looking for status {} but found {}"
                    .format(target_status, status)
                )
            time.sleep(interval)
    except GlanceNotFound:
        if target_status != 'deleted':
            raise
