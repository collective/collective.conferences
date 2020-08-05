# -*- coding: utf-8 -*-
from DateTime import DateTime
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import RelationList

import datetime
import Missing


def conf_utils_custom_json_handler(obj):
    if obj == Missing.Value:
        return None
    if type(obj) in (datetime.datetime, datetime.date):
        return obj.isoformat()
    if type(obj) == DateTime:
        dt = DateTime(obj)
        return dt.ISO()
    if type(obj) == set:
        return list(obj)
    if type(obj) == RelationValue:
        return obj.to_path.split('/')[-1]
    if type(obj) == RelationList:
        return list(item.to_path.split('/')[-1] for item in obj)
    return obj
