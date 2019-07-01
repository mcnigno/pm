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

def update_billable(items):
        session = db.session
        bill_file = openpyxl.load_workbook(UPLOAD_FOLDER + items.billable)
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
                                session.add(billitem)
                        else:
                                billitem = Billitem(
                                                tasks_id=items.id,
                                                timesheet_id=items.timesheet_id,
                                                item=row[0].value,
                                                time=row[1].value,
                                                comments=row[2].value
                                                )
                                session.add(billitem)
        session.commit() 
