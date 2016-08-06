"""Module containing actions to manage keystone projects."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.keystone.project')


def create(clients, context, name="test_project", domain='Default'):
    """Create a new keystone project

    Sets context['project']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param name: Name for the new project
    :type name: String
    :param domain: The domain in which to create the project
    :type domain: String
    """

    logger.info("Taking action project.create {}.".format(name))
    keystone = clients.get_keystone()
    project = keystone.projects.create(name, domain)
    context.update({'project': project})
    context.setdefault('stack', []).append({'project_obj': project})


def delete(clients, context):
    """Delete an existing keystone project

    Uses context['project']
    Removes context['project']

    :param clients: Client Manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """

    project = context['project']
    context.pop('project')

    logger.info("Taking action project.delete {}.".format(project.name))
    keystone = clients.get_keystone()
    keystone.projects.delete(project)
