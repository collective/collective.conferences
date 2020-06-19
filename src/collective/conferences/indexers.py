# -*- coding: utf-8 -*-
from collective.conferences.talk import ITalk
from collective.conferences.workshop import IWorkshop
from plone.indexer.decorator import indexer
from plone import api


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