Conference Registration
=======================

The registration of conference attendees will be done inside a folder
object. This folder could be created inside the root of the Plone site.
Therefore go to the root of the Plone site and click in the menu bar on
the left side on the entry 'Add new' and choose from the opening submenu
'Conference Registration Folder'. This opens the edit form to create the
folder for conference registrations (see screenshot below).

.. image:: images/conference_registration_folder_form01.png
   :width: 600

The form starts with a field for the title of the registration folder. This
could be e.g. 'Registration'. This field is mandatory. It is followed by a
field for a description of the registration folder, which is optional.

The field with main information about the registration process follows.
This field is not mandatory, but it could and should be used to describe
the registration process, including e.g. a conference fee.

The following field needs an answer to the question about a conference fee.
If this field is set to 'yes' you need to carefully edit the field 'Payment
Options'. The strings in that field will be displayed in and used for the
registration form which a conference attendee has to fill out (see below).

Once the fields were completed save the edit form and the conference
registration folder will be created inside the Plone site root.


Publishing the registration (folder)
************************************

The default state of the created folder will be 'private'. If you want to
change this state, click inside the menu bar on the left site on the entry
with this state and choose from the opening submenu 'Submit for Publication'
or if available 'Publish'. If you could only submit the conference
registration folder for publication a user with the appropriate permission
need to publish the folder later.


Conference Attendee Registration
================================

People, who want to register for the conference, first need to get an
account on the site and log-in. Thus they had first to register on
the site.

Once they logged-in they could click on the folder / page  for
conference registration, that was already created and published. There
they choose from the menu bar on the left the entry 'Add new' and click
in the opening submenu on the item 'Attendee'. This opens a form to add
a new conference attendee (see the screenshot below).

.. image:: images/conference_attendee_form01.png
   :width: 600

The attendee has to fill in his full name, his address and his e-mail
address into the form. If he is member of an organization he could
provide this information in the last field of the form.

If a conference attendee has to pay a conference fee (the appropriate
field in the registration folder edit form is set to yes; see above),
the registration form for the attendee contains three further fields
(see screenshot below).

.. image:: images/conference_attendee_form02.png
   :width: 600

The first field asks, if the conference fee has already been payed.
The next question is about the used bank account out of a list of
available accounts (they are added on the registration folder edit
form). The last field is about the users bank account, which was
used for the payment.

Once the attendee has filled in the necessary information she/he could
save the form and the registration finished. A new attendee will be
created. The default state is 'private'.