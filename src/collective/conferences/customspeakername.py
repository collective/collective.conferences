# -*- coding: utf-8 -*-
from plone.dexterity.content import Item


class CustomSpeakerName(Item):
    """Custom name for a release and linked release from the title and
    the release number"""

    @property
    def title(self):
        return self.firstname + ' ' + self.lastname

    def setTitle(self, value):
        return
