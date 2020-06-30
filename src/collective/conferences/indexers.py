# -*- coding: utf-8 -*-
from collective.conferences.conferencebreak import IConferencebreak
from collective.conferences.program import IProgram
from collective.conferences.talk import ITalk
from collective.conferences.workshop import IWorkshop
from DateTime import DateTime
from plone.indexer.decorator import indexer


@indexer(ITalk)
def presenternames(object, **kw):
    results = []
    for rel in object.speaker:
        if rel.isBroken():
            continue
        obj = rel.to_object.title
        results.append(obj)
    return results


@indexer(IWorkshop)
def workshopleadernames(object, **kw):
    results = []
    for rel in object.speaker:
        if rel.isBroken():
            continue
        obj = rel.to_object.title
        results.append(obj)
    return results


@indexer(IConferencebreak)
def conferencebreaktrackname(object, **kw):
    results = []
    for rel in object.conferencetrack:
        if rel.isBroken():
            continue
        obj = rel.to_object.title
        results.append(obj)
    return results


@indexer(IWorkshop)
def workshoptrackname(object, **kw):
    results = []
    for rel in object.conferencetrack:
        if rel.isBroken():
            continue
        obj = rel.to_object.title
        results.append(obj)
    return results


@indexer(ITalk)
def talktrackname(object, **kw):
    results = []
    for rel in object.conferencetrack:
        if rel.isBroken():
            continue
        obj = rel.to_object.title
        results.append(obj)
    return results


@indexer(IProgram)
def programStartIndexer(obj):
    if obj.start is None:
        return None
    programstart = DateTime(obj.start).toZone('UTC')
    return DateTime(programstart).ISO()


@indexer(IProgram)
def programEndIndexer(obj):
    if obj.end is None:
        return None
    programend = DateTime(obj.end).toZone('UTC')
    return DateTime(programend).ISO()
