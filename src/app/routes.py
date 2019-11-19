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

from flask import render_template, flash, redirect, send_from_directory, url_for
from app import app
from app.forms import LoginForm, ForgotPasswordForm, CreateDatasetForm, EditDatasetForm, DeleteDatasetForm, UploadJson, CreateUserForm, EditUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models_interface import DataBaseManager
from app.utils.gen import *
from app.utils.messages import send_email
import os

databaseManager = DataBaseManager()

@app.route('/')
@app.route('/index')
@app.route('/login',  methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        logout_user()

    loginForm = LoginForm()
    forgotPasswordForm = ForgotPasswordForm()

    error_code = 0

    if loginForm.validate_on_submit():
        user = databaseManager.getUserByEmail(email_p=loginForm.username.data)
        if user is None:
            error_code = 1
        else:
            if not user.check_password(loginForm.password.data):
                error_code = 2
                print(user.password_hash, hash(loginForm.password.data))
            else:
                login_user(user, remember=True)
                return redirect(url_for('datasets'))

    if forgotPasswordForm.validate_on_submit():
        print("FORGOT", forgotPasswordForm.email.data)

    return render_template('login.html', loginForm=loginForm, forgotPasswordForm=forgotPasswordForm, error_code=error_code)   

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():

    editUserForm = EditUserForm() 
    createUserForm = CreateUserForm()
    
    if createUserForm.validate_on_submit():

        temp_password = randomString()

        if databaseManager.registerUser(email_p=createUserForm.email.data, type_p=int(createUserForm.role.data), 
                                    name_p=createUserForm.username.data, password=temp_password, active_p=False) == 0:
            print("the user has been created")
            send_email("Um teste", "ajgbusson@gmail.com", [createUserForm.email.data],"Um teste", "<h4> Um teste </h4>")
        else:
            print("e-mail already registered")
    
    if editUserForm.validate_on_submit():
        print("EDIT", editUserForm.id.data, editUserForm.role.data, editUserForm.active.data)  
    
   
    users = databaseManager.getAllUser()
    return render_template('user_table.html', title="USERS", users=users, createUserForm=createUserForm, editUserForm=editUserForm)


@app.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():

    formCreateDataset = CreateDatasetForm()
    formEditDataset = EditDatasetForm()
    formDeleteDataset = DeleteDatasetForm()

    if formCreateDataset.validate_on_submit():
        req_code, req_msg = databaseManager.createDataset(title_p = formCreateDataset.title.data, 
            description_p = formCreateDataset.description.data, 
            type_p = formCreateDataset.annotation_type.data, owner_id_p = current_user.id, 
            license_p = formCreateDataset.license.data, zipfile_=formCreateDataset.zip_file.data, tags_p=formCreateDataset.tags.data)

    #if formEditDataset.validate_on_submit():

    if formDeleteDataset.validate_on_submit():
        req_code, req_msg = databaseManager.deleteDataset(formDeleteDataset.id.data, formDeleteDataset.title.data) 


    datasets = databaseManager.getAllDatasets()
    return render_template('datasets.html', title="DATASETS", 
        formCreateDataset=formCreateDataset, formEditDataset=formEditDataset, 
        formDeleteDataset=formDeleteDataset, datasets=datasets)

@app.route('/editor/<dataset_id>')
@login_required
def editor(dataset_id):

    dataset = databaseManager.getDataset(dataset_id)
    if dataset is None:
        return

    formJsonUpload = UploadJson()

    mediaList = databaseManager.getAllMediaFromDataset(dataset.id)

    return render_template('editor.html', title="EDITOR", 
            dataset=dataset, mediaList=mediaList, tags=dataset.tags.split(","), 
            formJsonUpload=formJsonUpload)


@app.route("/set_annotation/<dataset_id>/<media_id>", methods=['GET', 'POST'])
def setAnnotation(dataset_id, media_id):

    if not current_user.is_authenticated:
        return 'erro'

    formJsonUpload = UploadJson()
    
    if formJsonUpload.validate_on_submit():
        media = databaseManager.getMediaOfDatasetById(dataset_id, media_id)

        if  media is not None:
            databaseManager.set_json(media_id, formJsonUpload.json_document.data)
            return 'ok'

    return 'erro'

@app.route("/get_annotation/<dataset_id>/<media_id>")
def getAnnotation(dataset_id, media_id):

    if not current_user.is_authenticated:
        return '{}'

    media = databaseManager.getMediaOfDatasetById(dataset_id, media_id)

    if media is not None:
        annotation = databaseManager.get_json(media_id)
            
        if annotation is not None:
            return annotation.json_data

    return '{ \"boundinboxes\": [] }'


@app.route("/media/<path:path>")
def getMedia(path):

    if not current_user.is_authenticated:
        return 

    return send_from_directory(os.path.join(app.instance_path, 'DATASET_UPLOADS'),
                 path, as_attachment=True)


