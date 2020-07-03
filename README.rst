.. contents::

Introduction
============

The goal of this Plone add-on is to provide a framework for the organization
of conferences.

The add-on creates a content type conferencespeaker inside a speaker folder. The speaker
folder could be created at every place on the Plone site. A conferencespeaker is
restricted to a speaker folder.

The site admin can create a conference program and as much tracks as needed inside
this program. The title of the tracks will be indexed to the portal_catalog.

The site admin could create a page for the call for papers. The call for papers object
provides a field to add topics for the conference program. It's
view template provides for anonymus user the information that they need to
create an account on the site and the link to the register form.
If a user is already linked in she/he gets the links to submit a new talk or workshop
proposal. This proposal will be placed into a talksfolder or a workshopfolder
in the root of the site. The papers - talks or workshops - will be reviewed
and assigned to a track. The reviewers or site admins will set a number for the
order in this track too.

The view of a track creates a dynamic listing of its talks and workshops, ordered
by the ordering number a reviewer/site admin set for each talk. The listing (table)
will submit information about start time of every talk and its subject too. The track
view holds information about its time slot (begin and end) and the conference room
where it take place. The name of the room is linked to the appropriate room object thus
the audience could get very easy information about its location (the room object has
spaces to provide such information including a picture of the room).

The conference rooms are merged into a roomfolder, which could be placed everywhere on the
site.

The conference program shows a list of all conference tracks with their title,
description and dates. The tracks had to fit inside the program timeslot. The
editor of a track will get an error message, if this isn't the case.

There is also a section for the registration of people who want to attend the conference.
It is necessary to create an account on the site, before one could register for the
conference.

The add-on is currently in a alpha status. Further improvemments and missing features will
be added in the near future. Help in this development would be appreciated.
