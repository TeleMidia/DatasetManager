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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CreateDatasetForm(FlaskForm):
    title = StringField('Dataset title', validators=[DataRequired()])
    description = TextAreaField('Description')
    license = SelectField('License', choices=[('Unlicense', 'Unlicense'), ('GNU AGPLv3', 'GNU AGPLv3'), ('GNU GPLv3', 'GNU GPLv3'), ('GNU LGPLv3', 'GNU LGPLv3'), ('Mozilla Public License 2.0', 'Mozilla Public License 2.0'), ('MIT License', 'MIT License')])
    annotation_type = SelectField('Annotation type', choices=[('Classification', 'Classification'), ('Detection', 'Detection'), ('Segmentation', 'Segmentation')])
    submit = SubmitField('Submit')
    tags = StringField('Tags', validators=[DataRequired()])
    zip_file = FileField(validators=[FileRequired()])

class EditDatasetForm(FlaskForm):
    title = StringField('Dataset title', validators=[DataRequired()])
    description = TextAreaField('Description')
    license = SelectField('License', choices=[('Unlicense', 'Unlicense'), ('GNU AGPLv3', 'GNU AGPLv3'), ('GNU GPLv3', 'GNU GPLv3'), ('GNU LGPLv3', 'GNU LGPLv3'), ('Mozilla Public License 2.0', 'Mozilla Public License 2.0'), ('MIT License', 'MIT License')])
    annotation_type = SelectField('Annotation type', choices=[('Classification', 'Classification'), ('Detection', 'Detection'), ('Segmentation', 'Segmentation')])
    submit = SubmitField('Submit')

class DeleteDatasetForm(FlaskForm):
    id = StringField('Dataset id', validators=[DataRequired()])
    title = StringField('Dataset title', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadJson(FlaskForm):
    json_document = StringField('Json document', validators=[DataRequired()]) 