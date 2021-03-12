from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn, DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, Boolean 
from sqlalchemy.orm import column_property, relationship
import datetime

from sqlalchemy.sql.expression import column
from app import db
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders

from datetime import datetime
from datetime import timedelta
import time

def minutes_between(d1, d2):

    # Convert to Unix timestamp
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())
    
    return (d2-d1) 

class Status(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name

class Customer(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name


class Order(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship(Customer)

    def __repr__(self):
        return str(self.customer) + " | " + self.name


class Sal(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date_from = Column(Date, default=datetime.today, nullable=False)
    date_to = Column(Date, default=datetime.today, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship(Order)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)
    status = relationship(Status)

    def __repr__(self):
        return self.name +' - '+ str(self.order) + " | " + 'from: '+ str(self.date_from) + ' to: ' + str(self.date_to)


class Project(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship(Order)

    def __repr__(self):
        return self.name

class Cuos(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    code = Column(String(5), nullable=False)
    description = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship(Project)
    
    def __repr__(self):
        return self.code

class Contact(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    cuos_id = Column(Integer, ForeignKey('cuos.id'), nullable=False)
    cuos = relationship(Cuos)
    note = Column(String(255), nullable=False)
    report = Column(Boolean, default=False)

    def __repr__(self):
        return self.name

class Activity_type(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name

class Activity(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cuos_id = Column(Integer, ForeignKey('cuos.id'), nullable=False)
    cuos = relationship(Cuos)
    activity_type_id = Column(Integer, ForeignKey('activity_type.id'), nullable=False)
    activity_type = relationship(Activity_type)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1)
    status = relationship(Status)
    bill_file_required = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return self.name

class Rate(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    rate = Column(Integer, nullable=False)
    from_hours = Column(Integer, nullable=False)
    to_hours = Column(Integer, nullable=False)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)

    def __repr__(self):
        return str(self.activity) + " | " + "Man/hours (" + str(self.from_hours)+" - "+ str(self.to_hours) + ")" + " Rate: " + str(self.rate) + " €"

class Kpi(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, default=datetime.today, nullable=False)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    kpi = Column(Integer, nullable=False)

    def __repr__(self):
        return self.name


class Timesheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today().date, nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)
    status = relationship(Status)
    
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
    
    def __repr__(self):
        return self.date.strftime("%d %b, %Y")
    
    @renders('date')
    def ts_date(self):
    # will render this columns as bold on ListWidget
        return self.date.strftime("%A %d %B, %Y")

from flask_appbuilder.models.decorators import renders


class Tasks(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'), nullable=False)
    timesheet = relationship(Timesheet)
    date_from = Column(DateTime, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    date_to = Column(DateTime, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    billable = Column(FileColumn, nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1)
    status = relationship(Status)
 
    def time(self):
        return self.date_to - self.date_from

    def bill_filename(self):
        if self.billable: 
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
    
    def dfrom(self):
        return self.date_from.strftime("%A %d %B %y | %H:%M")

    def dto(self):
        return self.date_to.strftime("%A %d %B %y | %H:%M")
    
    def __repr__(self):
        return 'Task: '+ str(self.activity) + 'by '+ self.dfrom() + self.dto()
 
class Billitem(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    tasks_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    tasks = relationship(Tasks)
    deliverable = Column(String(255), nullable=False)
    doc_quantity = Column(Integer,nullable=False)
    item = Column(String(255), nullable=True)
    time = Column(Float, nullable=False)
    comments = Column(Text)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'), nullable=False)
    timesheet = relationship(Timesheet) 
    sal_id = Column(Integer, ForeignKey('sal.id'), nullable=True)
    sal = relationship(Sal)
    detail_file = Column(FileColumn, nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=True)
    status = relationship(Status) 