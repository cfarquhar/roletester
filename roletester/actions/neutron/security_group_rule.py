"""Module containing action to create a nova server."""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.neutron.security_group_rule')


def create(clients, context,
           direction='ingress',
           ethertype='IPv4',
           protocol='tcp',
           port_range_min=80,
           port_range_max=80):
    """Create a security group.

    Uses context['security_group_id']
    Sets context['security_group_rule_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    :param direction:  Security group rule direction
    :type direction: String
    :param ethertype: Ethertype
    :type ethertype: String
    :param protocol: Protocol
    :type protocol: String
    :param port_range_min: Beginning of port range
    :type port_range_min: Integer
    :param port_range_max: End of port range
    :type port_range_max: Integer
    """
    logger.info("Taking action security_group_rule.create")
    security_group_id = context['security_group_id']
    body = {
        'security_group_rule': {
            'direction': direction,
            'ethertype': ethertype,
            'protocol': protocol,
            'port_range_min': port_range_min,
            'port_range_max': port_range_max,
            'security_group_id': security_group_id
        }
    }
    neutron = clients.get_neutron()
    resp = neutron.create_security_group_rule(body)
    rule = resp['security_group_rule']
    context.update(security_group_rule_id=rule['id'])


def delete(clients, context):
    """Delete a security group rule

    Uses context['security_group_rule_id']

    :param clients: Client manager
    :type clients: roletester.clients.ClientManager
    :param context: Pass by reference object
    :type context: Dict
    """
    logger.info("Taking action security_group_rule.delete")
    neutron = clients.get_neutron()
    security_group_rule_id = context['security_group_rule_id']
    neutron.delete_security_group_rule(security_group_rule_id)
    context.pop('security_group_rule_id')
