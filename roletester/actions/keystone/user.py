"""Module containing actions to manage keystone users."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.keystone.user')


def create(clients, context, name="test_user", password="test_pass"):
    """Create a new keystone user

    Sets context['user']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name for the new user.
    :type name: String
    :param password: Password for the new user
    :type password: String
    """

    logger.info("Taking action user.create {}.".format(name))
    keystone = clients.get_keystone()
    user = keystone.users.create(name, domain="Default", password="test")
    context.update({'user': user})
    context.setdefault('stack', []).append({'user_obj': user})


def delete(clients, context):
    """Delete an existing keystone user

    Uses context['user']
    Removes context['user']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """

    user = context['user']
    context.pop('user')

    logger.info("Taking action user.delete {}.".format(user.name))
    keystone = clients.get_keystone()
    keystone.users.delete(user)


def change_name(clients, context, new_name="new_test_user"):
    """Changes the name of an existing keystone user

    Uses context['user']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param new_name: New name for user
    :type new_name: String
    """

    user = context['user']

    logger.info("Taking action user.change_name {}.".format(user.name))
    keystone = clients.get_keystone()
    keystone.users.update(user, name=new_name)
