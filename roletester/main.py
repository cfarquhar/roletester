from args import parser as argparser
from clients import ClientManager
import config
from log import logging
import time
import utils
from keystone_manager import KeystoneManager

from clients import ClientManager
from actions.nova import delete as server_delete
from actions.nova import create as server_create
from scenario import Scenario

logger = logging.getLogger('roletester')


from exc import NovaNotFound


admin_kwargs = {
    'auth_url': 'someurl',
    'username': 'someusername',
    'password': 'somepassword',
    'project_id': 'someprojectid',
    'user_domain_name': 'Default',
    'project_domain_name': 'Default'
}
admin_clients = ClientManager(**admin_kwargs)


demo_kwargs = {
    'auth_url': 'someurl',
    'username': 'someusername',
    'password': 'somepassword',
    'project_id': 'someprojectid',
    'user_domain_name': 'demodomain',
    'project_domain_name': 'demodeomain'
}
demo_clients = ClientManager(**demo_kwargs)


# Create then delete
logger.debug("\n\nClassic create then delete")
flavor = '1'
image  = '94f3805c-f59c-4dca-9cfe-40edf001c256'
name = 'scenario_test'
scenario = Scenario() \
        .chain(server_create, admin_clients, name, flavor, image) \
        .chain(server_delete, admin_clients)

state = {}
scenario.run(state)


logger.debug("\n\nDelete not found with expected")
scenario = Scenario() \
    .chain(server_delete, admin_clients, expected_exceptions=[NovaNotFound])
scenario.run(context={'server_id': '94f3805c-f59c-4dca-9cfe-40edf001c252'})


logger.debug("\n\nCreate with admin, delete with demo.")
scenario = Scenario() \
    .chain(server_create, admin_clients, name, flavor, image) \
    .chain(server_delete, demo_clients, expected_exceptions=[NovaNotFound])
scenario.run()

# Delete not found with no expected exceptions
#logger.debug("\n\nDelete not found without expected")
#scenario = Scenario() \
#        .chain(server_delete, admin_clients)
#scenario.run(context={'server_id': '94f3805c-f59c-4dca-9cfe-40edf001c252'})
