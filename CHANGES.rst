Changelog
=========

0.9 (2020-12-06)
----------------

- Add integration tests for all content type modules. [Andreas Mantke]
- Add import for virus free validation with collective.clamav. [Andreas Mantke]
- Update localization files. [Andreas Mantke]


0.8 (2020-11-17)
----------------

- Add mail notification about workflow state of talk, traininig and
  workflow module [Andreas Mantke]
- Update localization files [Andreas Mantke]


0.7 (2020-11-04)
----------------

- Add validation for the start and end of a training [Andreas Mantke]
- Add function to calculate the end of a training from its start date
  and its length [Andreas Mantke]
- Update localization files [Andreas Mantke]


0.6 (2020-10-20)
----------------

- Add training module with corresponding training folder module,
  add further fields to the configuration control panel for this
  new modules [Andreas Mantke]
- Text fixes on workshop module [Andreas Mantke]
- Fix uniqueness validators on talk and workshop modules [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Add workflow for training objects [Andreas Mantke]
- Add user documentation about new training module and [Andreas Mantke]


0.5 (2020-10-05)
----------------

- Improve speakers and rooms folder listing {Andreas Mantke]
- Fix notify speaker issue, if admin creates a new speaker
  profile [Andreas Mantke]
- Update localization files [Andreas Mantke]


0.4 (2020-09-30)
----------------

- Fix view templates of twfolder, track and program if speaker, track or
  conference room is not set [Andreas Mantke]
- Fix textes on the attendeefolder view template [Andreas Mantke]
- Add function to set start and end time of talks, tracks and
  conference breaks [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]

0.3 (2020-09-22)
----------------

- Add documentation about the conference registration [Andreas Mantke]
- Add new page for conference registration [Andreas Mantke]
- Add new mail form for conference registration [Andreas Mantke]
- Move options for conference fee and bank accounts to the controlpanes, make a
  vocabulary from this accounts and register it as utility [Andreas Mantke]
- Move view templates to a common folder [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Add Python versions 3.6 and 3.8 to the test matrix of Travis CI [Andreas Mantke]


0.2 (2020-08-29)
----------------

- Move functions for validation of email to the common module [Andreas Mantke]
- Add validation for email to attendee module [Andreas Mantke]
- Improve edit mode of talk and workshop module with register for slides,
  files and video [Andreas Mantke]
- Add Barceloneta theme class to table on the program and track view [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Add first version of user documentation, source, HTML and PDF file format [Andreas Mantke]
- Add a new workflow for conference talks and workshops. [Andreas Mantke]
- Add registry.xml, controlpanel.xml to unistall profile [Andreas Mantke]
- Renaming of the controlpanel [Andreas Mantke]
- Use safe_unicode instead of unicode for strings. [Andreas Mantke]
- Add fields to configure allowed file extensions for images, videos, slides and additional
  material and corresponding validators [Andreas Mantke]
- Add unique title validators for talks and workshops [Andreas Mantke]
- Add content types for conferencebreakfolder and talksworkshopfolder [Andreas Mantke]


0.1 (2020-07-10)
----------------

- Package created first using zopeskel and manually added and edited to make it working with Python 3 and
  current Plone 5.2.x