from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn, DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, Boolean
from sqlalchemy.orm import relationship
import datetime
from app import db
from flask_appbuilder.filemanager import get_file_original_name


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
from datetime import datetime
from datetime import timedelta
import time

def minutes_between(d1, d2):

    # Convert to Unix timestamp
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())

    
    return (d2-d1) 
    


class Project(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name

class Activity(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship(Project)
    cuo = Column(String(255), nullable=False)
    attachment_required = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.name

class Kpi(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship(Project)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    kpi = Column(Integer, nullable=False)

class Timesheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    

    def total_time(self):
        session = db.session
        task = session.query(Tasks).filter(Tasks.timesheet_id == self.id).all()
        tot_time = sum([(x.date_to - x.date_from) for x in task], timedelta())
        return tot_time
    
    def total_bill_time(self):
        session = db.session
        billitems = session.query(Billitem).filter(Billitem.timesheet_id == self.id).all()
        tot_bill_time = sum([x.time for x in billitems])
        return timedelta(minutes=tot_bill_time * 60)

    
    

    


class Cuos(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    code = Column(String(5), nullable=False)
    description = Column(String(255), nullable=False)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    
    def __repr__(self):
        return self.code





class Tasks(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship(Project)
    cuos_id = Column(Integer, ForeignKey('cuos.id'), nullable=False)
    cuos = relationship(Cuos)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'), nullable=False)
    timesheet = relationship(Timesheet)
    billable = Column(FileColumn, nullable=False)
 
    def time(self):
        return self.date_to - self.date_from

    def bill_filename(self):
        return get_file_original_name(self.billable)
    
    def total_bill_time(self):
        session = db.session
        billitems = session.query(Billitem).filter(Billitem.tasks_id == self.id).all()
        tot_bill_time = sum([x.time for x in billitems])
        return timedelta(minutes=tot_bill_time * 60)
    
    def task_vs_bill(self):

        difference = self.total_bill_time() - self.time()
        if difference.total_seconds() < 0:
            return 'Check Time'
        return difference
    
 
class Billitem(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    tasks_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    tasks = relationship(Tasks)
    item = Column(String(255), nullable=False, unique=True)
    time = Column(Float, nullable=False)
    comments = Column(Text)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id', ondelete="CASCADE"), nullable=False)
    timesheet = relationship(Timesheet) 