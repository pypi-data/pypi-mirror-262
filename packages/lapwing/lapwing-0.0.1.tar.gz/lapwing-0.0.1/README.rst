=======
Lapwing
=======

Lapwing is an opinionated setup script and project template for creating Wagtail projects.

Installing
----------

Lapwing has the following dependencies:

* dj-database-url
* python-decouple
* wagtail

Usage
-----

Lapwing provides an entry script ``lapwing``. Running the script will ask for the values
for the following information and settings

* Project directory (The directory the project will be created in)
* Project name (The name of the project)
* Log file path
* Database url
* Static root base
* Media root base

In addition, when createing the settings.ini file, it will automatically populate the 
following settings:

* SECRET_KEY
* ALLOWED_HOSTS
* DEBUG
