'''
Copyright (C) 2019  Antonio José Grandson Busson (Telemidia/PUC-Rio)

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
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer) #0-admin 1-annotator
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return '<User id:{} type:{} username:{} e-mail:{}>'.format(self.id, 
            self.type, self.username, self.email)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))
    type = db.Column(db.String(20), index=True) 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    version = db.Column(db.Integer, default=10)
    license = db.Column(db.String(30), index=True, default="Unlicense")
    tags = db.Column(db.String(180))

   
    def __repr__(self):
        return '<Database id:{} title:{} type:{} timestamp:{} owner_id:{} version:{} license:{}>'.format(
            self.id, self.title, self.type, self.timestamp, self.owner_id, self.version, self.license)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(64), index=True) 
    database_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))

    def __repr__(self):
        return '<Media id:{} path:{} database_id:{}>'.format(self.id, self.path, self.database_id)


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    json_data = db.Column(db.JSON)

    def __repr__(self):
        return '<Annotation id:{} media_id:{} json_data:{}>'.format(self.id, self.path, self.database_id)