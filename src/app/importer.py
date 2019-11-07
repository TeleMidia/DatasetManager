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


import json

class Importer():
    
    def __init__(self):
        self.class_name = "Importer"

    def parse_json(self, json_path, file_p):
        
        BOUNDINGBOXES = {}

        file_ = open(json_path+file_p)

        json_data = json.load(file_)
        data_frame = json_data["frames"]

        data_is_normalized = False

        for index_1, image_name in enumerate(data_frame):

            img_path = file_p+image_name    
            BOUNDINGBOXES[img_path] = []
            bbs_data = data_frame.get(image_name)
            for index_2, noise_data in enumerate(bbs_data):
                (wd, ht) = (noise_data["width"], noise_data["height"])
                (x1, y1) = (noise_data["x1"], noise_data["y1"])
                (x2, y2) = (noise_data["x2"], noise_data["y2"])
                tag = noise_data["tags"][0]

                if data_is_normalized is not True:
                   (x1, y1) = (x1/wd, y1/ht)
                   (x2, y2) = (x2/wd, y2/ht)

                BOUNDINGBOXES[img_path].append([tag, x1, y1, x2, y2])
                #print([x1, y1, x2, y2])

        return BOUNDINGBOXES
