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

USER_TYPE = {"SUPER_ADM": "0", "ADM": "1", "NORMAL": "2"}

USER_STATUS = {"ACTIVE": "0", "BLOCKED": "1"}

ERROR_TYPE = {"SUCCESS": 0}

ANNOTATION_TYPE = {"CLASSIFICATION": "0", "DETECTION": "1" ,"SEGMENTATION": "2"}

LICENSE_TYPE = {"UNLICENSE": "0", "GNU_AGPLV3": "1", "GNU_GPLV3": "2", 
"GNU_LGPLV3": "3", "MOZILLA_PUBLIC_LICENSE_2": "4", "MIT_LiCENSE": "5"}


def getKeyByValue(dict, value_p):
    for key, value in dict.items():    
        if int(value) == value_p:
            return key

    return None

def getTypeByValue(category_p, value_p):
    global USER_TYPE, USER_STATUS, ERROR_TYPE, ANNOTATION_TYPE, LICENSE_TYPE
    print('CALL!')
    if category_p == "ANNOTATION":
        return getKeyByValue(ANNOTATION_TYPE, value_p)
    elif category_p == "LICENSE":
        return getKeyByValue(LICENSE_TYPE, value_p)