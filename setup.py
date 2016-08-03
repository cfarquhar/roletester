from setuptools import setup

from roletester.meta import version

setup(
    name="roletester",
    version=version,
    author="james absalon",
    author_email="james.absalon@rackspace.com",
    packages=[
        'roletester',
        'roletester.actions.nova',
        'roletester.actions.cinder',
        'roletester.actions.nova',
        'roletester.actions.glance'
    ],
    long_description=("Quick tool for testing linked actions with different "
                      "roles."),
    data_files=[
        ('/etc/roletester', ['roletester.yaml'])
    ]
)
