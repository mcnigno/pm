from zipfile import ZipFile
from config import UPLOAD_FOLDER
def read_zip(file):
    # specifying the zip file name 
    file_name = UPLOAD_FOLDER + 'file'
    print('file', file_name)
    # opening the zip file in READ mode 
    with ZipFile(file_name, 'r') as zip: 
        # printing all the contents of the zip file 
        return zip.namelist()
         

