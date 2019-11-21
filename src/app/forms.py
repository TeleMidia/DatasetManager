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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired,  Email
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired

from app.utils.types import *

class LoginForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired()], render_kw={"placeholder": "e-mail"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField('Sign In')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "e-mail"})
    submit = SubmitField('Submit')

class CreateUserForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()], render_kw={"placeholder": "user name"})
    email = EmailField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "e-mail"})
    role = SelectField('Role', choices=[(USER_TYPE["NORMAL"], "ANNOTATOR"), (USER_TYPE["ADM"], "ADMIN")])
    register = SubmitField('Register')

class EditUserForm(FlaskForm):
    id = StringField('Dataset id', validators=[DataRequired()])
    role = SelectField('Role', choices=[(USER_TYPE["NORMAL"], "ANNOTATOR"), (USER_TYPE["ADM"], "ADMIN")])
    active = SelectField('STATUS', choices=[(USER_STATUS["ACTIVE"], "ACTIVE"), (USER_STATUS["BLOCKED"], "BLOCKED")])
    edit = SubmitField('Edit')

class CreateDatasetForm(FlaskForm):
    title = StringField('Dataset title', validators=[DataRequired()], render_kw={"placeholder": "title"})
    description = TextAreaField('Description')
    license = SelectField('License', choices=[(LICENSE_TYPE["UNLICENSE"], 'Unlicense'), (LICENSE_TYPE["GNU_AGPLV3"], 'GNU AGPLv3'), (LICENSE_TYPE["GNU_GPLV3"], 'GNU GPLv3'), (LICENSE_TYPE["GNU_LGPLV3"], 'GNU LGPLv3'), (LICENSE_TYPE["MOZILLA_PUBLIC_LICENSE_2"], 'Mozilla Public License 2.0'), (LICENSE_TYPE["MIT_LiCENSE"], 'MIT License')])
    annotation_type = SelectField('Annotation type', choices=[(ANNOTATION_TYPE["CLASSIFICATION"], 'Classification'), (ANNOTATION_TYPE["DETECTION"], 'Detection'), (ANNOTATION_TYPE["SEGMENTATION"], 'Segmentation')])
    tags = StringField('Tags', validators=[DataRequired()])
    annotators = StringField('Annotators e-mail', validators=[DataRequired()])
    batch_size = IntegerField('Batch Size', validators=[DataRequired()], render_kw={"value": "100"})
    zip_file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')

class EditDatasetForm(FlaskForm):
    title = StringField('Dataset title', validators=[DataRequired()])
    description = TextAreaField('Description')
    license = SelectField('License', choices=[(LICENSE_TYPE["UNLICENSE"], 'Unlicense'), (LICENSE_TYPE["GNU_AGPLV3"], 'GNU AGPLv3'), (LICENSE_TYPE["GNU_GPLV3"], 'GNU GPLv3'), (LICENSE_TYPE["GNU_LGPLV3"], 'GNU LGPLv3'), (LICENSE_TYPE["MOZILLA_PUBLIC_LICENSE_2"], 'Mozilla Public License 2.0'), (LICENSE_TYPE["MIT_LiCENSE"], 'MIT License')])
    annotation_type = SelectField('Annotation type', choices=[(ANNOTATION_TYPE["CLASSIFICATION"], 'Classification'), (ANNOTATION_TYPE["DETECTION"], 'Detection'), (ANNOTATION_TYPE["SEGMENTATION"], 'Segmentation')])
    submit = SubmitField('Submit')

class DeleteDatasetForm(FlaskForm):
    id = StringField('Dataset id', validators=[DataRequired()])
    title = StringField('Dataset title', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadJson(FlaskForm):
    json_document = StringField('Json document', validators=[DataRequired()]) 