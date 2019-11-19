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

import zipfile
import os
import shutil

class FileManager():

    def __init__(self):
        self.folder = "/"


    def saveDataset(self, root_path, dataset_name, file_name, file_data):
        
        folder_path = os.path.join(root_path, dataset_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)
        file_data.save(file_path)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)

        

    def deleteFolder(self, folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)        
            return True
        return False

    def getAllFilePaths(self, folder_path, ext):
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(folder_path):
            for file in f:
                if file[0] == '.': 
                    continue
                
                if file.split('.')[-1] in ext:
                    files.append(os.path.join(r, file).replace(folder_path,''))
                  
        
        return files
