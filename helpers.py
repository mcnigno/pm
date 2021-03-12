from app.models import Project, Activity, Billitem
from app import db
import openpyxl
from config import UPLOAD_FOLDER
from datetime import timedelta, datetime

def upload_project():
        session = db.session
        prj = open('xls/progetti.csv', encoding='utf-8-sig')
        for line in prj:
                row = Project(project=line)
                row.created_by_fk = '1'
                row.changed_by_fk = '1'
                session.add(row)
        session.commit()

def upload_activity():
        session = db.session
        prj = open('xls/activities.csv', encoding='utf-8-sig')
        for line in prj:
                row = Activity(activity=line)
                row.created_by_fk = '1'
                row.changed_by_fk = '1'
                session.add(row)
        
        session.commit()

def upload_history():
        session = db.session
        projects = dict([(x.project, x.id) for x in session.query(Project).all()])
        activities = dict([(x.activity, x.id) for x in session.query(Activity).all()])
        act = open('xls/history.csv')

from zip_helper import read_zip
from flask_appbuilder.security.sqla.manager import User
from flask import flash 

def check_tbd(item, deliverable):
    # verifica l'esistenza di billables/items con transmittal TBD (to be defined) e ne aggiorna il transmittal
    session = db.session
    billables = session.query(Billitem).filter(Billitem.deliverable == 'TBD', Billitem.item == item).all()
    for bill in billables:
        bill.deliverable = deliverable
    session.commit()

def update_billable(items):
    session = db.session
    print('update billable started')
    print('file path', UPLOAD_FOLDER,'file', items.billable)
    file_list = []
    if str(items.billable).split('.')[1] == 'zip':
        zip_items = read_zip(UPLOAD_FOLDER + items.billable)
        file_list = zip_items[0]
    
    elif str(items.billable).split('_sep_')[1] == 'tr.xlsx':
        try:
            print('open TR.XLSX file')
            bill_file = openpyxl.load_workbook(UPLOAD_FOLDER + items.billable)
            print('TR.XLSX file OPEND')
            bill_ws = bill_file.active
        
            for row in bill_ws.iter_rows(min_row=4):
                    print(row[0].value)
                    if row[0].value and row[1].value:
                        if row[2].value is None:
                            billitem = Billitem(
                                            tasks_id=items.id,
                                            timesheet_id=items.timesheet_id,
                                            deliverable = row[0].value,
                                            doc_quantity = row[1].value,
                                            item=row[2].value,
                                            time=row[3].value,
                                            comments=row[4].value
                                            )

                            #session.add(billitem)
                        else:
                            billitem = Billitem(
                                            tasks_id=items.id,
                                            timesheet_id=items.timesheet_id,
                                            deliverable = row[0].value,
                                            doc_quantity = row[1].value,
                                            item=row[2].value,
                                            time=row[3].value,
                                            comments=row[4].value
                                            )
                        '''
                        billitem.created_by_fk = '1'
                        billitem.changed_by_fk = '1'
                        '''
                        # add only if the deliverable is unique
                        billables = session.query(Billitem).filter(Billitem.item == billitem.item, Billitem.deliverable == 'TBD').all()
                        for bill in billables:
                            bill.deliverable = billitem.deliverable
                        session.add(billitem)
                        print('added:',billitem)
                    #session.commit()
        except:
            print('EXCEPTION')
            pass
    else:
        file_list.append(items.billable)
    try:
        for file in file_list:
            
            if file[:2] != '__' and '.' in file and file != 'tr.xlsx':
                print(file)
                billitem = Billitem(
                        tasks_id=items.id,
                        timesheet_id=items.timesheet_id,
                        deliverable = 'ND',
                        item=file,
                        time='0.25',
                        doc_quantity = 1
                        )
                session.add(billitem)
                print('added:',billitem)
    except:
        print('Errore lista file')
        pass


    session.commit()
    print('session committed **** ----- ////') 




                        