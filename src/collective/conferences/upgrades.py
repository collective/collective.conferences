# -*- coding: utf-8 -*-
import logging

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

logger = logging.getLogger(__name__)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.conferences:default',
    )
