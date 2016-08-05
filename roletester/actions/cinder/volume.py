import time
import utils
from roletester.exc import CinderNotFound
from roletester.log import logging

logger = logging.getLogger('roletester.actions.cinder.volume')


def create(clients, context, size=1):
    """Creates cinder volume.

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param size: Volume size in GB
    :type size: int
    """
    logger.info("Taking action create")
    cinder = clients.get_cinder()
    name = utils.randomname(prefix='random-volume')
    meta = {'app': 'roletester'}
    volume = cinder.volumes.create(name=name, size=size, metadata=meta)
    context.update({'volume_id': volume.id})
    context.setdefault('stack', []).append({'volume_id': volume.id})
    logger.info("Created volume {0} with metadata {1}"
                .format(volume.name, volume.metadata))


def delete(clients, context):
    """Deletes volume.

    Uses context['volume_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    logger.info("Taking action delete")
    cinder = clients.get_cinder()

    volume = cinder.volumes.get(context['volume_id'])
    cinder.volumes.delete(volume)
    context.pop('volume_id')
    logger.info("Deleted volume {0} - {1} - {2}"
                .format(volume.name, volume.size, volume.metadata))


def list(clients, context):
    """Lists volumes.

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    logger.info("Listing active volumes")
    cinder = clients.get_cinder()
    volumes = cinder.volumes.list()
    for v in volumes:
        logger.info("{0} - {1}".format(v.name, v.metadata))


def show(clients, context):
    """Shows a cinder volume.

    Uses context['volume_id']
    Sets context['volume_status']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    """
    logger.info("Taking action volume.show")
    cinder = clients.get_cinder()
    volume_id = context['volume_id']
    volume = cinder.volumes.get(volume_id)
    context.update(volume_status=volume.status.lower())


def attach(clients, context, mountpoint='/u01'):
    """Attaches a volume to a server.

    Uses context['server_id']
    Uses context['volume_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    volume_id = context['volume_id']
    server_id = context['server_id']
    logger.info("Attaching volume %s to %s" % (volume_id, server_id))
    volume = clients.get_cinder().volumes.get(volume_id)
    volume.attach(server_id, mountpoint)


def detach(clients, context):
    """Detaches a volume from a server.

    Uses context['volume_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    volume_id = context['volume_id']
    logger.info("Detaching volume %s" % volume_id)
    volume = clients.get_cinder().volumes.get(volume_id)
    volume.detach()


def create_image(clients,
                 context,
                 name='cinder test image',
                 container_format='bare',
                 disk_format='qcow2'):
    """Takes a snapshot of the volume and uploads it to glance.

    Uses context['volume_id']
    Sets context['volume_image_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Image name
    :type name: String
    :param container_format: Disk container format.
    :type container_format: String
    :param disk_format: Disk file format.
    :type disk_format: String
    """
    volume_id = context['volume_id']
    logger.info("Creating image from %s" % volume_id)
    volume = clients.get_cinder().volumes.get(volume_id)
    resp = volume.upload_to_image(False,
                                  name,
                                  container_format,
                                  disk_format)
    # Glance Problems
    image_id = resp[1]['os-volume_upload_image']['image_id']
    context.update(volume_image_id=image_id)


# Statuses that indicate a terminating status
_DONE_STATUS = set(['available',
                    'in-use',
                    'deleting',
                    'error',
                    'error_deleting'])


def wait_for_status(admin_clients,
                    context,
                    timeout=60,
                    interval=5,
                    initial_wait=None,
                    target_status='available'):
    """Waits for a volume to go to a request status.

    Uses context['volume_id']
    Uses context['volume_status']

    :param admin_clients: Client manager
    :type admin_clients: roletester.clients.ClientManager
    :param context: Pass by reference context object.
    :type context: Dict
    :param timeout: Timeout in seconds.
    :type timeout: Integer
    :param interval: Time in seconds to wait between polls.
    :type timeout: Integer
    :param initial_wait: Time in seconds to wait before beginning to poll.
        Useful for expecting a volume that is ACTIVE to go to DELETED
    :type initial_wait: Integer
    :param target_status: Status to wait for. If desired status is DELETED,
        a NotFoundException will be allowed.
    :type target_status: String
    """
    logger.info("Taking action wait for volume")

    if initial_wait:
        time.sleep(initial_wait)

    start = time.time()
    try:
        while (time.time() - start < timeout):
            show(admin_clients, context)
            status = context['volume_status']
            logger.debug("Found status {}".format(status))
            if status == target_status:
                context.pop('volume_status')
                break
            if status in _DONE_STATUS:
                raise Exception(
                    "Was looking for status {} but found {}"
                    .format(target_status, status)
                )
            time.sleep(interval)
    except CinderNotFound:
        if target_status != 'deleting':
            raise