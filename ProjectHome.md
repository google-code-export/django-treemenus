**Django Tree Menus**


---

**Important**: This repository has now been moved to github: http://github.com/jphalip/django-treemenus

---




This is a simple and generic tree-structured menuing system for [Django](http://www.djangoproject.com/) with an easy-to-use admin interface. It covers all the essentials for building tree-structured menus and should be enough for a lot of projects.
However it is easily extendable if you need to add some special behaviour.

**Please note: django-treemenus requires Django 1.0 or a recent Subversion checkout of Django. It will not work on Django 0.96.**

Full documentation is included in the package or directly accessible: [here](http://django-treemenus.googlecode.com/svn/trunk/docs/MANUAL.txt).
Some sample templates are also provided in the package to get you started.

# Change log #
v0.8.6 - 23/01/2010: Small update to make it compatible with Django 1.2. Also fixed some packaging issues from 0.8.5

v0.8.5 - 21/01/2010: Minor updates (tests and doc fixes, and updated some locales)

v0.8 - 14/03/2009: Few small fixes. There are no backward incompatibilities in this release, but it is recommended to upgrade especially if you use recent development versions of Django.

v0.7.2 - 01/10/2008: Fixed a small edge-case bug and slightly improved the admin interface .

v0.7.1 - 29/09/2008: Fixed a small bug when deleting menu items.

v0.7 - 16/09/2008: A few small bugs fixed. This release generally brings a lot of robustness. Even if your data (ranks, levels, etc.) were corrupted, they should automatically be repaired after saving the faulty menu items. Please also note a few deprecated methods [here](http://code.google.com/p/django-treemenus/wiki/DeprecatedFeatures).

v0.6 - 08/08/2008: Major refactor of the codebase to better fit New-Forms-Admin's API. Few and easily manageable backward incompatible changes are described [here](http://code.google.com/p/django-treemenus/wiki/BackwardIncompatibleChanges).

v0.5 - 22/07/2008: Upgraded code so it works after the merge of the Newforms-Admin branch (Keep using version 0.4 if you haven't upgraded your own code to newforms-admin). Also added German locale kindly provided by Thomas Kerpe.

v0.4 - 26/05/2008: New languages added: Russian (thanks maxim.oransky), dutch (thanks v.oostveen), and French. You can send me your translations and I'll include them in future releases.

v0.3 - 05/03/2008: Added a new section in the documentation "Tips and tricks", and fixed a small bug as described in [this issue](http://code.google.com/p/django-treemenus/issues/detail?id=3).

v0.2.2 - 15/02/2008: Fixed another small bug as in previous release.

v0.2.1 - 15/02/2008: Fixed a bug as described in [this issue](http://code.google.com/p/django-treemenus/issues/detail?id=1).

v0.2 - 14/02/2008: Added a clean and generic way to extend and customize menu items. Have a look at the [manual](http://django-treemenus.googlecode.com/svn/trunk/docs/MANUAL.txt) to see how it works.

v0.1 - 01/02/2008: First release

# Screenshots #

Here's the customized admin interface:

![http://django-treemenus.googlecode.com/files/screenshot-admin.png](http://django-treemenus.googlecode.com/files/screenshot-admin.png)

Here's how it could look like in the front end if you added a little bit of CSS:

![http://django-treemenus.googlecode.com/files/screenshot-frontend.png](http://django-treemenus.googlecode.com/files/screenshot-frontend.png)

# Installation #

Full instructions are provided in the [manual](http://django-treemenus.googlecode.com/svn/trunk/docs/MANUAL.txt).