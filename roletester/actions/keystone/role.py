"""Module containing actions to manage keystone roles."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.keystone.role')


def _get_role_uuid_by_name(keystone, name):
    """Gets a role UUID when provided a role name.

    :param keystone: keystone client
    :type clients: roletester.clients.ClientManager
    :param name: The name of the role whos UUID should be returned
    :type name: String
    :returns: role UUID
    :rtype: String

    """

    role_UUID = None
    roles_list = keystone.roles.list()

    for role in roles_list:
        if role.name == name:
            role_UUID = role.id
            break

    if role_UUID is None:
            raise NameError('Specified role name not found')
    else:
        return role_UUID


def grant_user_project(clients, context, role="_member_"):
    """Grant a role to (user,project)

    Uses context['user']
    Uses context['project']
    Sets context['role']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param role: Name of the role to grant
    :type role: String
    """

    user = context['user']
    project = context['project']

    logger.info("Taking action role.grant_user_project {}.".format(user.name))
    keystone = clients.get_keystone()
    role_uuid = _get_role_uuid_by_name(keystone, role)
    keystone.roles.grant(role_uuid, user=user, project=project)
    context.update({'role': role_uuid})


def revoke_user_project(clients, context):
    """Revokes a role from (user, project)

    Uses context['user']
    Uses context['project']
    Uses context['role']
    Removes context['role']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """

    user = context['user']
    project = context['project']
    role_uuid = context['role']

    logger.info("Taking action role.revoke_user_project {}.".format(user.name))
    keystone = clients.get_keystone()
    keystone.roles.revoke(role_uuid, user=user, project=project)

    context.pop('role')
