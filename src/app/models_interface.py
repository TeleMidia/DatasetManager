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

from app import app, db
from app.models import User, Dataset, Media, Annotation, User_Dataset
from app.filemanager import FileManager
from app.importer import Importer
from app.utils.types import *
import os
import math

from werkzeug.utils import secure_filename

class DataBaseManager():
    
    def __init__(self):
        self.folder = "/"
        self.fileManager = FileManager()

    #begin user interface
    def getAllUser(self):
         return User.query.all()

    def getUserById(self, user_id_p):
        return User.query.get(user_id_p)
    
    def getUserByEmail(self, email_p):
        return User.query.filter_by(email=email_p).first()

    def getUserByDatasetId(self, dataset_id_p):
        return User_Dataset.query.filter_by(dataset_id=dataset_id_p)

    def registerUser(self, email_p, type_p, name_p, password, active_p):

        # check if e-mail already registered
        if User.query.filter_by(email=email_p).first() is None:
            new_user = User(email=email_p, role=type_p, name=name_p, active=active_p)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return 0, "Sucess"
        else:
            return 1, "Error: e-mail name already registered."   
    #end user interface

    def createDataset(self, title_p, description_p, annotation_type_p, owner_id_p, license_p, zipfile_, tags_p, annotators_p, batch_size_p):
        # check if exists a dataset with same name
        if Dataset.query.filter_by(title=title_p).first() is None:
            new_dataset = Dataset(title=title_p, description=description_p, annotation_type=annotation_type_p, owner_id=owner_id_p, license=license_p, tags=tags_p)
            db.session.add(new_dataset)
            db.session.commit()

            #who can annotate this dataset
            annotators = annotators_p.split(",")
            for annotator in annotators:
                user = self.getUserByEmail(annotator)
                if  user is not None:
                    new_user_dataset = User_Dataset(user_id=user.id, dataset_id=new_dataset.id)
                    db.session.add(new_user_dataset)
            db.session.commit()
            
            #extract all files from .zip
            if zipfile_ is not None:
                #save and extract dataset
                file_name = secure_filename(zipfile_.filename)
                storage_path = os.path.join(app.instance_path, 'datasets')
                dataset_root_folder = "dataset_"+str(new_dataset.id)
                self.fileManager.saveDataset(storage_path, dataset_root_folder, file_name, zipfile_)

                storage_path = os.path.join(storage_path, dataset_root_folder)
                
                #get all images
                imagesPathList = self.fileManager.getAllFilePaths(storage_path, ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]) 

                new_dataset.load = len(imagesPathList)
                
                new_dataset.batch_count = math.ceil(len(imagesPathList)/batch_size_p)
                
                batch_index=0

                for index, file_ in enumerate(imagesPathList):
                    if index%batch_size_p == 0:
                        batch_index += 1    

                    new_media = Media(path=file_, batch_index=batch_index, database_id=new_dataset.id)
                    db.session.add(new_media)
                
                

                db.session.commit()
               
                
            return 0, "Sucess"
        else:
            return 1, "Error: dataset name already exists."    

    def deleteDataset(self, dataset_id_p, dataset_title_p):

        dataset = Dataset.query.get(dataset_id_p)

        if dataset is None:
            return

        if dataset.title == dataset_title_p:
            #delete dataset
            db.session.delete(dataset)

            #get all media from dataset    
            media = Media.query.filter_by(database_id=dataset_id_p)
            if media is not None:
                for m in media:
                    annotations = Annotation.query.filter_by(media_id=m.id)
                    if annotations is not None:
                        for a in annotations:
                            db.session.delete(a)
                    db.session.delete(m)
            

            #get all related users to this dataset
            user_datasets = User_Dataset.query.filter_by(dataset_id=dataset_id_p)
            if user_datasets is not None:
                for user_dataset in user_datasets:
                    db.session.delete(user_dataset)    

            db.session.commit()

            storage_path = os.path.join(app.instance_path, 'datasets', "dataset_"+str(dataset.id))
            self.fileManager.deleteFolder(storage_path)

            return 0, "Sucess"

        return 1, "Error: wrong dataset name." 

    def getAllDatasets(self):
        return Dataset.query.all()

    def getAllDatasetsByOwnerId(self, owner_id_p):
        return Dataset.query.filter_by(owner_id=owner_id_p)
    
    def getDatasetsIdByUser(self, user_id_p):
        return User_Dataset.query.filter_by(user_id=user_id_p)

    def getDataset(self, dataset_id_p):
        return Dataset.query.get(dataset_id_p) 
    
    def getAllMediaFromDataset(self, dataset_id_p):
        return Media.query.filter_by(database_id=dataset_id_p)

    def getAllMediaFromDatasetBatch(self, dataset_id_p, batch_id_p):
        return Media.query.filter_by(database_id=dataset_id_p, batch_index=batch_id_p )



    def getMediaOfDatasetById(self, dataset_id_p, media_id_p):
        return Media.query.filter_by(database_id=dataset_id_p, id=media_id_p)

    def set_json(self, media_id_p, user_id_p, json_document):
        annotation = Annotation.query.filter_by(media_id=media_id_p).first()

        if annotation is None:
            annotation = Annotation(media_id=media_id_p, user_id=user_id_p, json_data=json_document)
            db.session.add(annotation)
        else:
            annotation.json_data = json_document

        db.session.commit()

    def get_json(self, media_id_p):
        return Annotation.query.filter_by(media_id=media_id_p).first()