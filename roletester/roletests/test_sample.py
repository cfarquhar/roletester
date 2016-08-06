from base import Base as BaseTestCase
from roletester.actions.nova import server_create
from roletester.actions.nova import server_delete
from roletester.actions.nova import server_show
from roletester.actions.nova import server_wait_for_status
from roletester.exc import NovaNotFound
from roletester.scenario import ScenarioFactory as Factory


from roletester.log import logging

logger = logging.getLogger("roletester.test_sample")


class SampleFactory(Factory):

    _ACTIONS = [
        server_create,
        server_wait_for_status,
        server_show,
        server_delete
    ]

    CREATE = 0
    WAIT = 1
    SHOW = 2
    DELETE = 3


class TestSample(BaseTestCase):

    name = 'scratch'
    flavor = '1'
    image = '94f3805c-f59c-4dca-9cfe-40edf001c256'

    def test_admin_create_admin_delete(self):
        """Test that admin can create and delete a server."""
        admin = self.km.find_user_credentials('Default', 'admin', 'admin')
        SampleFactory(admin) \
            .set_args(SampleFactory.CREATE, (self.name, self.flavor, self.image)) \
            .produce() \
            .run(context=self.context)

    def test_admin_create_demo_delete(self):
        """Test that admin can create and demo can delete."""
        admin = self.km.find_user_credentials('Default', 'admin', 'admin')
        demo = self.km.find_user_credentials('Default', 'demo', 'member')
        SampleFactory(admin) \
            .set_args(SampleFactory.CREATE, (self.name, self.flavor, self.image)) \
            .set(SampleFactory.DELETE, clients=demo, expected_exceptions=[NovaNotFound]) \
            .produce() \
            .run(context=self.context)
