# ImageAnnotator
An ImageAnnotator tool

## Building the repository
With Python >= 3.6 and pip, install the dependencies:

    $ pip3 install flask 
    $ pip3 install flask-wtf
    $ pip3 install flask-sqlalchemy
    $ pip3 install sqlalchemy-utils
    $ pip3 install flask-migrate
    $ pip3 install flask-login
    $ pip3 install flask-mail
    $ pip3 install pyjwt
    
From "/src", run:   

    $ flask db init
    $ flask db migrate -m "users table"
    $ flask db upgrade
    $ export FLASK_APP=datasetmanager.py 

## Starting ImageAnnotator
From "/src", run:

    $ flask run

---
Copyright (C) 2019 PUC-Rio/Laboratorio TeleMidia

Permission is granted to copy, distribute and/or modify this document under
the terms of the GNU Free Documentation License, Version 1.3 or any later
version published by the Free Software Foundation; with no Invariant
Sections, with no Front-Cover Texts, and with no Back-Cover Texts. A copy of
the license is included in the "GNU Free Documentation License" file as part
of this distribution.
