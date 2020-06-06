# -*- coding: utf-8 -*-
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICollectiveconfControlPanel(Interface):


    break_length = schema.Tuple(
        title=u"Length Of Conference Breaks",
        description=u"Fill in the time slots for conference breaks in minutes. Use a new line for every "
                      u"value / talk length. Write only the numbers without the addition 'minutes'.",
        value_type=schema.TextLine(),
        required=True,
    )

    talk_length = schema.Tuple(
        title=u"Length Of Talks",
        description=u"Fill in the time slots for conference talks in minutes. Use a new line for every "
                      u"value / talk length. Write only the numbers without the addition 'minutes'.",
        value_type=schema.TextLine(),
        required=True,
    )

    workshop_length = schema.Tuple(
        title=u"Length Of Workshops",
        description=u"Fill in the time slots for workshops at the conference in minutes. Use a new line for every "
                      u"value / workshop length. Write only the numbers without the addition 'minutes'.",
        value_type=schema.TextLine(),
        required=True,
    )

class CollectiveconfControlPanelForm(RegistryEditForm):
    schema = ICollectiveconfControlPanel
    schema_prefix = "collectiveconf"
    label = u'Collectiveconf Settings'

CollectiveconfControlPanelView = layout.wrap_form(
    CollectiveconfControlPanelForm, ControlPanelFormWrapper)
