"""Module containing actions to manage swift containers."""
from roletester.log import logging
import copy

logger = logging.getLogger('roletester.actions.swift.swift_container')


def create(clients, context,
           name="test_container"):
    """Create a container

    Sets context['container_name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name of the new container
    :type name: String
    """
    logger.info("Taking action container.create {}.".format(name))
    swift = clients.get_swift()
    swift.put_container(name)
    context.update({'container_name': name})


def delete(clients, context):
    """Deletes a container.

    Uses context['container_name']
    Removes context['container_name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    name = context['container_name']
    logger.info("Taking action container.delete {}.".format(name))
    swift = clients.get_swift()
    swift.delete_container(name)
    context.pop('container_name')


def get(clients, context):
    """Retrieves stats and lists objects in a container.

    Uses context['container_name']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    name = context['container_name']
    logger.info("Taking action container.get {}.".format(name))
    swift = clients.get_swift()
    swift.get_container(name)
    swift.head_container(name)


def add_metadata(clients, context,
                 metadata={"X-Container-Meta-Author": "JohnDoe"}):
    """Sets metadata on a container.

    Uses context['container_name']
    Sets context['container_metadata']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param metadata: Dict of metadata headers
    :type metadata: Dict
    """
    name = context['container_name']
    context.update({"container_metadata": copy.deepcopy(metadata)})
    logger.info("Taking action container.add_metadata {}.".format(name))
    swift = clients.get_swift()
    swift.post_container(name, metadata)


def delete_metadata(clients, context):
    """Sets metadata on a container.

    Uses context['container_name']
    Deletes context['container_metadata']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param metadata: Dict of metadata headers
    :type metadata: Dict
    """
    name = context['container_name']
    metadata = copy.deepcopy(context['container_metadata'])
    logger.info("Taking action container.delete_metadata {}.".format(name))

    # Delete metadata by removing each key's value
    for key in metadata.keys():
        metadata[key] = ''

    swift = clients.get_swift()
    swift.post_container(name, metadata)
    context.pop('container_metadata')
