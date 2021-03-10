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
def update_billable(items):
    session = db.session
    print('update billable started')
    print('file path', UPLOAD_FOLDER,'file', items.billable)
    zip_items = read_zip(UPLOAD_FOLDER + items.billable)
    file_list = zip_items[0]
    try:
        print('tr file?',zip_items[1])
        tr_file = zip_items[1]
        print('open TR.XLSX file')
        bill_file = openpyxl.load_workbook(tr_file)
        print('TR.XLSX file OPEND')
        bill_ws = bill_file.active
        
        for row in bill_ws.iter_rows(min_row=4):
                print(row[0].value)
                if row[0].value and row[1].value:
                    if row[2].value is None:
                        billitem = Billitem(
                                        tasks_id=items.id,
                                        timesheet_id=items.timesheet_id,
                                        item=row[0].value,
                                        time=row[1].value,
                                        comments=''
                                        )

                        #session.add(billitem)
                    else:
                        billitem = Billitem(
                                        tasks_id=items.id,
                                        timesheet_id=items.timesheet_id,
                                        item=row[0].value,
                                        time=row[1].value,
                                        comments=row[2].value
                                        )
                    '''
                    billitem.created_by_fk = '1'
                    billitem.changed_by_fk = '1'
                    '''
                    # add only if the item is unique
                    item = session.query(Billitem).filter(Billitem.item == row[0].value).first()
                    if item is not None:
                        user = session.query(User).filter(User.id == item.change_by_fk).first()
                        message = item.item + ' has been already billed by ' + user.first_name + ' ' + user.last_name + ' '+str(item.changed_on)
                        flash(message=message, category='info')
                    else:
                        session.add(billitem)
                        print('added:',billitem)
                #session.commit()
    except:
        print('EXCEPTION')
        pass
    
    for file in file_list:
        
        if file[:2] != '__' and '.' in file:
            print(file)
            billitem = Billitem(
                    tasks_id=items.id,
                    timesheet_id=items.timesheet_id,
                    item=file,
                    time='0.25',
                    comments=''
                    )
            session.add(billitem)
            print('added:',billitem)


    session.commit()
    print('session committed **** ----- ////') 




                        