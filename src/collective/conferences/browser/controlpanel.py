# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICollectiveconferenceControlPanel(Interface):
    break_length = schema.Tuple(
        title=u'Length Of Conference Breaks',
        description=u'Fill in the time slots for conference breaks in minutes. Use a new line for every '
                    u"value / talk length. Write only the numbers without the addition 'minutes'.",
        default=(15,
                 20,
                 30,),
        value_type=schema.TextLine(),
        required=True,
    )

    talk_length = schema.Tuple(
        title=u'Length Of Talks',
        description=u'Fill in the time slots for conference talks in minutes. Use a new line for every '
                    u"value / talk length. Write only the numbers without the addition 'minutes'.",
        default=(30,
                 45,
                 60,),
        value_type=schema.TextLine(),
        required=True,
    )

    workshop_length = schema.Tuple(
        title=u'Length Of Workshops',
        description=u'Fill in the time slots for workshops at the conference in minutes. Use a new line for every '
                    u"value / workshop length. Write only the numbers without the addition 'minutes'.",
        default=(60,
                 120,
                 180,),
        value_type=schema.TextLine(),
        required=True,
    )

    license = schema.Tuple(
        title=u'Licenses Of Talks / Workshops',
        description=u'Fill in the names of the licenses for conference talks and workshops. Use a new line for '
                    u'every value / license name.',
        default=(
            'GNU-GPL-v2 (GNU General Public'
            'License Version 2)',
            'GNU-GPL-v3+ (General Public License'
            'Version 3 and later)',
            'CC-by-sa-v3 (Creative Commons'
            'Attribution-ShareAlike 3.0)',
            'CC-BY-SA-v4 (Creative Commons'
            'Attribution-ShareAlike 4.0 '
            'International)',),
        value_type=schema.TextLine(),
        required=True,
    )


class CollectiveconferenceControlPanelForm(RegistryEditForm):
    schema = ICollectiveconferenceControlPanel
    schema_prefix = 'collectiveconference'
    label = u'Collective Conference Settings'


CollectiveconferenceControlPanelView = layout.wrap_form(
    CollectiveconferenceControlPanelForm, ControlPanelFormWrapper)
