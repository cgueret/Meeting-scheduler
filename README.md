# Meeting Scheduler
**Authors**: [Christophe Gueret](http://github.com/cgueret)

**Copyright**: VU University Amsterdam

**License**: [LGPL v3.0](http://www.gnu.org/licenses/lgpl.html)

## About

This is a very simple meeting scheduler currently used to plan the [weekly AI meetings](http://wai.few.vu.nl) at the VU 

## Usage

Here is how to deploy a site similar to <http://wai.few.vu.nl> :

* Create a directory ```/var/www/wai.few.vu.nl/``` and eventually copy waibase.db in it
* Create a directory ```/var/www/wai.few.vu.nl/appli``` and copy the [settings-remote.py](http://github.com/cgueret/Meeting-scheduler/blob/master/settings-remote.py) in it and rename it as "settings.py"
* Clone the content of [the wai directory](http://github.com/cgueret/Meeting-scheduler/tree/master/wai) into /var/lib/django/wai

## Requirements

* Python 2.7
* Django 1.2.1 minimum <https://www.djangoproject.com/>


