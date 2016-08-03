"""This is just a playing around module. Please ignore it"""
from roletester.log import logging

logger = logging.getLogger('roletester.actions.cinder.list')


def list(clients, conf):
    logger.info("Listing active volumes")
    cinder = clients.get_cinder()
    volumes = cinder.volumes.list()
    for v in volumes:
        logger.info("{0} - {1}".format(v.name, v.metadata))
