# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile

import logging


logger = logging.getLogger(__name__)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.conferences:default',
    )
