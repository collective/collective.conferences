# -*- coding: utf-8 -*-
from collective.conferences import _
from zope import schema
from plone.supermodel import model
from Products.Five import BrowserView
from plone.supermodel.directives import primary
from Acquisition import aq_inner, aq_parent
from plone.autoform.directives import write_permission, read_permission
from plone.app.textfield import RichText
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from zope.security import checkPermission
from plone.app.textfield import RichText
from collective.conferences.conferencespeaker import IConferenceSpeaker
from collective.conferences.track import ITrack
from plone.namedfile.field import NamedBlobFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Acquisition import aq_inner, aq_parent, aq_get
from collective import dexteritytextindexer
from collective.conferences.callforpaper import ICallforpaper

#from collective.conferences.track import setdates


# class StartBeforeEnd(Invalid):
#   __doc__ = _(u"The start or end date is invalid")


def vocabCfPTracks(context):
    # For add forms

    # For other forms edited or displayed
    
    if context is not None and not ICallforpaper.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    track_list = []
    if context is not None and hasattr(context, 'cfp_tracks'):
        track_list = context.cfp_tracks

    terms = []
    for value in track_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabCfPTracks, IContextSourceBinder)


class ITalk(model.Schema):
    """A conference talk. Talks are managed inside tracks of the Program.
    """
    
    length = SimpleVocabulary(
       [SimpleTerm(value=u'15', title=_(u'15 minutes')),
        SimpleTerm(value=u'30', title=_(u'30 minutes')),
        SimpleTerm(value=u'45', title=_(u'45 minutes')),
        SimpleTerm(value=u'60', title=_(u'60 minutes'))]
        )
 

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Talk title"),
        )

    description = schema.Text(
            title=_(u"Talk summary"),
        )


    primary('details')
    details = RichText(
            title=_(u"Talk details"),
            required=True
        )

    # use an autocomplete selection widget instead of the default content tree
#    form.widget(speaker=AutocompleteFieldWidget)
#    speaker = RelationChoice(
#            title=_(u"Presenter"),
#            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
#            required=False,
#        )
#    form.widget(speaker=AutocompleteFieldWidget)
#    speaker2 = RelationChoice(
#            title=_(u"Co-Presenter"),
#            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
#            required=False,
#        )
 
#    form.widget(speaker=AutocompleteFieldWidget)
#    speaker3 = RelationChoice(
#            title=_(u"Co-Presenter"),
#            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
#            required=False,
#        )
 

    dexteritytextindexer.searchable('call_for_paper_tracks')
    call_for_paper_tracks = schema.List(
        title=_(u"Choose the track for your talk"),
        value_type=schema.Choice(source=vocabCfPTracks),
        required=True,
    )

 
 
#    form.widget(track=AutocompleteFieldWidget)
#    track = RelationChoice(
#            title=_(u"Track"),
#            source=ObjPathSourceBinder(object_provides=ITrack.__identifier__),
#            required=False,
#        )


    write_permission(startitem='collective.conferences.ModifyTalktime')
    startitem = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )
    

    write_permission(enditem='collective.conferences.ModifyTalktime')
    enditem = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )

        
    length= schema.Choice(
            title=_(u"Length"),
            vocabulary=length,
            required=True,
        )
    write_permission(order='collective.conferences.ModifyTrack')
    order=schema.Int(
           title=_(u"Orderintrack"),               
           description=_(u"Order in the track: write in an Integer from 1 to 12"),
           min=1,
           max=12,
           required=False,
        )
                  
    
    slides = NamedBlobFile(
            title=_(u"Presentation slides in ODT-File-Format"),
            description=_(u"Please upload your presentation shortly after you have given your talk."),
            required=False,
        )
    
    slides2 = NamedBlobFile(
            title=_(u"Presentation slides in PDF-File-Format or PDF-Hybrid-File-Format"),
            description=_(u"Please upload your presentation shortly after you have given your talk."),
            required=False,
        )

    slides3 = schema.URI(
            title=_(u"Link to the presentation slides in ODT-File-Format"),
            required=False,
        )
    slides4 = schema.URI(
        title=_(u"Link to the presentation slides in PDF-File-Format or PDF-Hybrid-File-Format"),
        required=False,
       )

    files = NamedBlobFile(
            title=_(u"Additional Files of your presentation."),
            description=_(u"Please upload the additional files of your presentation (in archive format) shortly after you have given your talk."),
            required=False,
        )

    files2 = schema.URI(
            title=_(u"Link to additional Files of your presentation in archive file format (e.g. zip-file-format."),
            required=False,
        )

    video = schema.URI(
            title=_(u"Link to the Video of the talk"),
            required=False,
        )
    creativecommonslicense= schema.Bool(
            title=_(u'label_creative_commons_license', default=u'License is Creative Commons Attribution-Share Alike 3.0 License.'),
                description=_(u'help_creative_commons_license', default=u'You agree that your talk and slides are provided under the Creative Commons Attribution-Share Alike 3.0 License.'),
                default=True
        )
    
    messagetocommittee = schema.Text (
            title=_(u'Messages to the Program Committee'),
            description=_(u'You can give some information to the committee here, e.g. about days you are (not) available to give the talk'),
            required=False,                     
        )
    
    read_permission(reviewNotes='cmf.ReviewPortalContent')
    write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
            title=u"Review notes",
            required=False,
        )

# @indexer(ITalk)
# def speakerIndexer(obj):
#     if obj.speaker is None:
#        return None
#    return obj.speaker
# grok.global_adapter(speakerIndexer, name="Subject")


# @grok.subscribe(ITalk, IObjectMovedEvent)
# def removeCFP_reference(talk, event):
#    if not ICallforpaper.providedBy(event.newParent):
#        talk.call_for_paper_tracks = None

    
#@grok.subscribe(ITalk, IObjectAddedEvent)
#def talkaddedevent(talk, event):
#    setdates(talk)

#@grok.subscribe(ITalk, IObjectModifiedEvent)
#def talkmodifiedevent(talk, event):
#    setdates(talk)
    

#    @invariant
#    def validateStartEnd(data):
#        if data.start is not None and data.end is not None:
#            if data.start > data.end:
#                raise StartBeforeEnd(_(
#                    u"The start date must be before the end date."))

class TalkView(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)


    def TalkRoom(self):
       from collective.conferences.track import ITrack
       parent = aq_parent(aq_inner(self.context))
       if ITrack.providedBy(parent):
           room = parent.room.to_object.title
       else: room = ""
       return room
