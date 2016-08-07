from volume import create as volume_create
from volume import delete as volume_delete
from volume import update as volume_update
from volume import list as volume_list
from volume import show as volume_show
from volume import attach as volume_attach
from volume import detach as volume_detach
from volume import create_image as volume_create_image
from volume import wait_for_status as volume_wait_for_status

__all__ = [
    'volume_create',
    'volume_delete',
    'volume_update',
    'volume_list',
    'volume_show',
    'volume_attach',
    'volume_detach',
    'volume_create_image',
    'volume_wait_for_status'
]
