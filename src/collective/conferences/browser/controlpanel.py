# -*- coding: utf-8 -*-
from collective.conferences import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from Products.CMFPlone.utils import safe_unicode
from zope import schema
from zope.interface import Interface


class ICollectiveconferenceControlPanel(Interface):
    break_length = schema.Tuple(
        title=_(safe_unicode('Length Of Conference Breaks')),
        description=_(safe_unicode('Fill in the time slots for conference breaks in minutes. Use a new line for every '
                                   "value / break length. Write only the numbers without the addition 'minutes'.")),
        default=(15,
                 20,
                 30),
        value_type=schema.TextLine(),
        required=True,
    )

    talk_length = schema.Tuple(
        title=_(safe_unicode('Length Of Talks')),
        description=_(safe_unicode('Fill in the time slots for conference talks in minutes. Use a new line for every '
                                   "value / talk length. Write only the numbers without the addition 'minutes'.")),
        default=(30,
                 45,
                 60),
        value_type=schema.TextLine(),
        required=True,
    )

    workshop_length = schema.Tuple(
        title=_(safe_unicode('Length Of Workshops')),
        description=_(
            safe_unicode('Fill in the time slots for workshops at the conference in minutes. Use a new line for every '
                         "value / workshop length. Write only the numbers without the addition 'minutes'.")),
        default=(60,
                 120,
                 180),
        value_type=schema.TextLine(),
        required=True,
    )

    license = schema.Tuple(
        title=_(safe_unicode('Licenses Of Talks / Workshops')),
        description=_(
            safe_unicode('Fill in the names of the licenses for conference talks and workshops. Use a new line for '
                         'every value / license name.')),
        default=(
            'GNU-GPL-v2 (GNU General Public'
            'License Version 2)',
            'GNU-GPL-v3+ (General Public License'
            'Version 3 and later)',
            'CC-by-sa-v3 (Creative Commons'
            'Attribution-ShareAlike 3.0)',
            'CC-BY-SA-v4 (Creative Commons'
            'Attribution-ShareAlike 4.0 '
            'International)'),
        value_type=schema.TextLine(),
        required=True,
    )

    allowed_conferenceimageextension = schema.TextLine(
        title=_(safe_unicode('Allowed image file extension')),
        description=_(safe_unicode('Fill in the allowed image file extensions, seperated '
                                   "by a pipe '|'.")),
        default=safe_unicode('jpg|jpeg|png|gif'),
    )

    allowed_talk_slide_extensions = schema.TextLine(
        title=_(safe_unicode('Allowed file extensions for slides of conference talks')),
        description=_(safe_unicode('Fill in the allowed file extensions for the slides of'
                                   "conference talks, seperated by a pipe '|'.")),
        default=safe_unicode('odp|pdf'),
    )

    allowed_workshop_material_extension = schema.TextLine(
        title=_(safe_unicode('Allowed workshop material / presentation file extensions')),
        description=_(safe_unicode('Fill in the allowed file extensions for the material of or'
                                   "slides of a workshop, seperated by a pipe '|'.")),
        default=safe_unicode('otp|pdf|zip'),
    )

    allowed_video_file_extensions = schema.TextLine(
        title=_(safe_unicode('Allowed file exensions for conference videos.')),
        description=_(safe_unicode('Fill in the allowed file extensions for the videos of '
                                   "conference talks / workshops, separated by a pipe '|'.")),
        default=safe_unicode('mp4|mpg'),
    )


class CollectiveconferenceControlPanelForm(RegistryEditForm):
    schema = ICollectiveconferenceControlPanel
    schema_prefix = 'collectiveconference'
    label = u'Collective Conference Settings'


CollectiveconferenceControlPanelView = layout.wrap_form(
    CollectiveconferenceControlPanelForm, ControlPanelFormWrapper)
