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

from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer) #0-superadmin #1- admin #2- normal
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User id:{} type:{} name:{} e-mail:{} active:{} password_hash:{}>'.format(self.id, 
            self.type, self.name, self.email, self.active, self.password_hash)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#aux function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))
    annotation_type = db.Column(db.Integer, index=True, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    version = db.Column(db.Integer, default=10)
    license =  db.Column(db.Integer, index=True, default=0)
    tags = db.Column(db.String(180))
    load = db.Column(db.Integer, default=0)
    batch_count = db.Column(db.Integer, default=0)
   
    def __repr__(self):
        return '<Dataset id:{} title:{} type:{} timestamp:{} owner_id:{} version:{} license:{}>'.format(
            self.id, self.title, self.type, self.timestamp, self.owner_id, self.version, self.license)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_index = db.Column(db.Integer,  index=True)
    path = db.Column(db.String(64), index=True) 
    database_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))

    def __repr__(self):
        return '<Media id:{} path:{} database_id:{}>'.format(self.id, self.path, self.database_id)



class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    json_data = db.Column(db.JSON)

    def __repr__(self):
        return '<Annotation id:{} media_id:{} json_data:{}>'.format(self.id, self.path, self.database_id)


class User_Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))


