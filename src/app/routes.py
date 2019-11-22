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
from app.utils.types import * 
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

    '''
    if current_user.role != int(USER_TYPE["SUPER_ADM"]):
        return redirect(url_for('500'))
    '''

    editUserForm = EditUserForm() 
    createUserForm = CreateUserForm()
        
    if createUserForm.validate_on_submit():
        temp_password = randomString()
        temp_password = "123456"
        if databaseManager.registerUser(email_p=createUserForm.email.data, type_p=int(createUserForm.role.data), 
                                        name_p=createUserForm.username.data, password=temp_password, active_p=True) == 0:
            print("the user has been created")
            #send_email("Um teste", "ajgbusson@gmail.com", [createUserForm.email.data],"Um teste", "<h4> Um teste </h4>")
        else:
            print("e-mail already registered")
        
    if editUserForm.validate_on_submit():
        print("EDIT", editUserForm.id.data, editUserForm.role.data, editUserForm.active.data)  
        
    
    users = databaseManager.getAllUser()
    return render_template('user_table.html', current_user=current_user, title="USERS", users=users, createUserForm=createUserForm, editUserForm=editUserForm,
                                                getTypeByValue=getTypeByValue)
    


@app.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():

    formCreateDataset = CreateDatasetForm()
    formEditDataset = EditDatasetForm()
    formDeleteDataset = DeleteDatasetForm()

    if formCreateDataset.validate_on_submit():
        req_code, req_msg = databaseManager.createDataset(title_p = formCreateDataset.title.data, 
            description_p = formCreateDataset.description.data, 
            annotation_type_p = int(formCreateDataset.annotation_type.data), owner_id_p = current_user.id, 
            license_p = int(formCreateDataset.license.data), zipfile_=formCreateDataset.zip_file.data, 
            tags_p=formCreateDataset.tags.data, annotators_p=formCreateDataset.annotators.data, batch_size_p=int(formCreateDataset.batch_size.data))

    #if formEditDataset.validate_on_submit():

    if formDeleteDataset.validate_on_submit():
        req_code, req_msg = databaseManager.deleteDataset(formDeleteDataset.id.data, formDeleteDataset.title.data) 

    
    datasets = []

    if current_user.role == int(USER_TYPE["SUPER_ADM"]):
        datasets = databaseManager.getAllDatasets()
    elif current_user.role == int(USER_TYPE["ADM"]): 
        datasets = getAllDatasetsByOwnerId(current_user.id)


    datasets_annotators = []
    for dataset in datasets:
        dataset.annotators = [[], ""]
        users = databaseManager.getUserByDatasetId(dataset_id_p=dataset.id)
        if users is not None:
            dataset.annotators[0] = users 
            for index, user in enumerate(users):
                pre_str = ", "
                if index == 0:
                    pre_str = ""
                if index == users.count()-1:
                    pre_str = " and "
                dataset.annotators[1] += pre_str+databaseManager.getUserById(user.user_id).name

    return render_template('datasets.html', current_user=current_user, title="DATASETS", 
        formCreateDataset=formCreateDataset, formEditDataset=formEditDataset, 
        formDeleteDataset=formDeleteDataset, datasets=datasets, 
        getTypeByValue=getTypeByValue, getUserById=databaseManager.getUserById)

@app.route('/editor/<dataset_id>/<batch_id>')
@login_required
def editor(dataset_id, batch_id):

    dataset = databaseManager.getDataset(dataset_id)
    if dataset is None:
        return

    formJsonUpload = UploadJson()

    mediaList = databaseManager.getAllMediaFromDatasetBatch(dataset.id, batch_id)

    return render_template('editor.html', current_user=current_user, title="EDITOR", 
            dataset=dataset, mediaList=mediaList, tags=dataset.tags.split(","), 
            formJsonUpload=formJsonUpload, batch_id=batch_id)


@app.route("/set_annotation/<dataset_id>/<media_id>", methods=['GET', 'POST'])
def setAnnotation(dataset_id, media_id):

    if not current_user.is_authenticated:
        return 'erro'

    formJsonUpload = UploadJson()
    
    if formJsonUpload.validate_on_submit():
        media = databaseManager.getMediaOfDatasetById(dataset_id, media_id)

        if  media is not None:
            databaseManager.set_json(media_id, current_user.id, formJsonUpload.json_document.data)
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

    return send_from_directory(os.path.join(app.instance_path, app.config['DATASETS_STORAGE']),
                 path, as_attachment=True)


