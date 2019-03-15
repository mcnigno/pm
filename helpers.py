from app.models import Project, Activity, History
from app import db

def upload_project():
        session = db.session
        prj = open('xls/progetti.csv')
        for line in prj:
                row = Project(project=line)
                row.created_by_fk = '1'
                row.changed_by_fk = '1'
                session.add(row)
        session.commit()

def upload_activity():
        session = db.session
        prj = open('xls/activities.csv')
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
