from zipfile import ZipFile
from config import UPLOAD_FOLDER

def read_zip(file_name):
    # specifying the zip file name 
    print('read_zip file path:', file_name)
    zip_items = []
    # opening the zip file in READ mode 
    with ZipFile(file_name, 'r') as zip: 
        # printing all the contents of the zip file 
        print('# printing all the contents of the zip file')
        zip_items.append(zip.namelist())
        '''
        print('try open tr.xlsx')
        filezip_name = file_name.split('_sep_')[1].split('.')[0]
        print(filezip_name)
        for x in zip.namelist():
            print(x)  
        tr_file = zip.open(filezip_name + '/tr.xlsx', mode='r', pwd=None) 
        
        print('OK open tr.xlsx', tr_file)
        zip_items.append(tr_file)
        #print(zip_items)
        '''
        
    return zip_items
         

