import pprint
from roletester.log import logging

logger = logging.getLogger('roletester.scenario')


class ExpectedException(Exception):
    def __init__(self, expected_exceptions):
        msg = 'Was expecting one of {} to be raised and none were raised.' \
            .format(', '.join([str(e) for e in expected_exceptions]))
        super(ExpectedException, self).__init__(msg)


class Scenario(list):

    def chain(self, action, clients, *args, **kwargs):
        """Add an action to the list of actions in a scenario.

        :param action: Action to take
        :type action: Function
        :param clients: Client manager
        :type clients: roletester.clients.ClientManager
        :param context: Context of the scenario. An object that is passed by
            reference and altered throughout the scenario.
        :type context: Dict | None
        :param expected_exceptions: List of expected exceptions
        :type expected_exceptions: List
        """
        expected_exceptions = None
        if 'expected_exceptions' in kwargs:
            expected_exceptions = kwargs.pop('expected_exceptions')

        self.append(
            [action, clients, expected_exceptions, args, kwargs]
        )
        return self

    def run(self, context=None):
        """Run the scenario

        :param context: Object that will be passed by reference to
            each action in the scenario.
        :type context: Dict
        """
        context = context or {}
        for action, clients, expected_exceptions, args, kwargs in self:
            try:
                action(clients, context, *args, **kwargs)
                if expected_exceptions:
                    raise ExpectedException(expected_exceptions)
            except Exception as e:
                matches = [isinstance(e, t) for t in expected_exceptions or []]
                if not any(matches):
                    raise e
                logger.debug("Found expected exception {}".format(type(e)))
            logger.debug('Context: {}'.format(pprint.pprint(context)))
