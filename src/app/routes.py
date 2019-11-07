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


from flask import render_template, flash, redirect, send_from_directory
from app import app
from app.forms import LoginForm, CreateDatasetForm, EditDatasetForm, DeleteDatasetForm, UploadJson

from app.databasemanager import DataBaseManager

import os

databaseManager = DataBaseManager()

@app.route('/')
@app.route('/index')
@app.route('/datasets', methods=['GET', 'POST'])
def datasets():
    formCreateDataset = CreateDatasetForm()
    formEditDataset = EditDatasetForm()
    formDeleteDataset = DeleteDatasetForm()

    if formCreateDataset.validate_on_submit():
        req_code, req_msg = databaseManager.createDataset(title_p = formCreateDataset.title.data, 
            description_p = formCreateDataset.description.data, 
            type_p = formCreateDataset.annotation_type.data, owner_id_p = 1, 
            license_p = formCreateDataset.license.data, zipfile_=formCreateDataset.zip_file.data, tags_p=formCreateDataset.tags.data)

    #if formEditDataset.validate_on_submit():

    if formDeleteDataset.validate_on_submit():
        req_code, req_msg = databaseManager.deleteDataset(formDeleteDataset.id.data, formDeleteDataset.title.data) 

    datasets = databaseManager.getAllDatasets()
    return render_template('datasets.html', title="DATASETS", 
        formCreateDataset=formCreateDataset, formEditDataset=formEditDataset, 
        formDeleteDataset=formDeleteDataset, datasets=datasets)

@app.route('/editor/<dataset_id>')
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
    formJsonUpload = UploadJson()
    
    if formJsonUpload.validate_on_submit():
        media = databaseManager.getMediaOfDatasetById(dataset_id, media_id)

        if  media is not None:
            databaseManager.set_json(media_id, formJsonUpload.json_document.data)
            return 'ok'

    return 'erro'

@app.route("/get_annotation/<dataset_id>/<media_id>")
def getAnnotation(dataset_id, media_id):
    media = databaseManager.getMediaOfDatasetById(dataset_id, media_id)

    if media is not None:
        annotation = databaseManager.get_json(media_id)
            
        if annotation is not None:
            return annotation.json_data

    return '{ \"boundinboxes\": [] }'


@app.route("/media/<path:path>")
def getMedia(path):
    return send_from_directory(os.path.join(app.instance_path, 'DATASET_UPLOADS'),
                 path, as_attachment=True)


