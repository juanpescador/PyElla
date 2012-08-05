PyElla
======

Python module that attempts to separate a full Spanish name into three separate parts: given name, first surname and second surname.

Introduction
------------
Spanish names are different from Anglo Saxon names: there is no concept of
"middle name" (instead there are compound firstnames) and there is usually a
second surname, e.g. José Hernández Almodóvar. There is no limit (in Spain) as
to the number of surnames a person can have. Usually the first surname is the
person's father's first surname and the second surname is the person's mother's
first surname. Subsequent surnames can be the father's second surname followed
by the mother's second surname followed by grandparents' and ancestors'
surnames.

Some Anglo-centric software mistakenly considers the first surname to be a
middle name, causing problems when trying to export <Firstname> <Lastname>
information from them.

Parsing names is difficult. Parsing full Spanish names is further complicated
by the fact that given names and surnames can be compound. This module attempts
to parse Spanish names into the following parts:

 - Given name (simple or compound).
 - First surname (simple or compound).
 - Second (and subsequent) surname(s) (simple or compound).

Issues
------
 - Some compound firstnames aren't taken into account. This is solveable by
   adding the missing compound firstames to a configuration file.
 - In some cases some compound firstnames are actually surnames. There is no
   workaround for this as of yet.

How to use
----------
Example use of the module is demonstrated in CSVexample.py.
