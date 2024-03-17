"""
Concrete :class:`~.base.TrackerConfigBase` subclass for ANT
"""

import base64

from ...utils import configfiles
from ..base import TrackerConfigBase, exclude


class AntTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9hbnRoZWxpb24ubWU=').decode('ascii'),
        'apikey': configfiles.config_value(
            value='',
            description='Your person upload API key you created in your profile.',
        ),
        'announce_url': configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'source': 'ANT',
        'exclude': (
            exclude.checksums,
            exclude.images,
            exclude.nfo,
            exclude.samples,
        ),
    }

    argument_definitions = {
        'submit': {
        },
    }
