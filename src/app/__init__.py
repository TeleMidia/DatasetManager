'''
Copyright (C) 2019  Telemidia/PUC-Rio <http://www.telemidia.puc-rio.br/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy_utils import database_exists
from sqlalchemy import inspect
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

from app import routes, models, models_interface, filemanager, importer
from app.utils.types import *


if database_exists(db.engine.url):
    db_tables = inspect(db.engine).get_table_names()
    if "user" in db_tables:
        dataBaseManager =  models_interface.DataBaseManager()
        if len(dataBaseManager.getAllUser()) == 0:
            if dataBaseManager.registerUser(email_p="admin", type_p=0, 
                                            name_p="admin", password="admin", 
                                            active_p=True) == ERROR_TYPE["SUCCESS"]:
                print("SuperAdmin user has been created\n","login:", "admin\n","password:", "admin")
