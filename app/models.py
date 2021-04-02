#from app.views import get_user
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn, DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, Boolean, Table
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.orm import column_property, relationship
import datetime

from sqlalchemy.sql.expression import column
#from app import db
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders

from datetime import datetime
from datetime import timedelta
import time
from flask import jsonify


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

from flask_appbuilder.filemanager import get_file_original_name

class Tsfiles(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    file = Column(FileColumn, nullable=False)
    
    def __repr__(self):
        return get_file_original_name(self.file)


class Timesheet(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today().date, nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship(Status)

    
    def total_time(self):
        from app import db
        session = db.session
        task = session.query(Tasks).filter(Tasks.timesheet_id == self.id).all()
        tot_time = sum([(x.date_to - x.date_from) for x in task], timedelta())
        return str(tot_time)
    
    '''
    def total_bill_time(self):
        from app import db
        session = db.session
        tasks = session.query(Tasks).filter(Tasks.timesheet_id == self.id).all()
        tot_bill_time = sum([int(x.total_bill_time().total_seconds()) for x in tasks])
        #billitems = session.query(Billitem).filter(Billitem.timesheet_id == self.id).all()
        #tot_bill_time = sum([x.time for x in billitems])
        
        return str(timedelta(minutes=tot_bill_time / 60))
    '''
    def __repr__(self):
        return self.date.strftime("%d %b, %Y")
    
    @renders('date')
    def ts_date(self):
    # will render this columns as bold on ListWidget
        #return self.date.strftime("%A %d %B, %Y")
        return self.date

from flask_appbuilder.models.decorators import renders


class Tasks(Model, AuditMixin): 
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity = relationship(Activity)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'), nullable=False)
    timesheet = relationship(Timesheet)
    date_from = Column(DateTime, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    date_to = Column(DateTime, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    attachment = Column(FileColumn, nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship(Status)
    task_status = Column(String(255), nullable=True)
    sal_id = Column(Integer, ForeignKey('sal.id'), nullable=True)
    sal = relationship(Sal)
    sal_item = Column(String(255), nullable=True)
    doc_quantity = Column(Integer,nullable=True, default=1)
    ref_item = Column(String(255), nullable=True)
    time = Column(Float, nullable=True)
    comments = Column(Text) 

 
    def time(self):
        return self.date_to - self.date_from

    def attachment_filename(self): 
        if self.attachment: 
            return get_file_original_name(self.attachment)
    
    '''
    def total_bill_time(self):
        from app import db
        session = db.session
        billitems = session.query(Billitem).filter(Billitem.tasks_id == self.id).all()
        tot_bill_time = sum([x.time for x in billitems])
        return timedelta(minutes=tot_bill_time * 60)
    
    def task_vs_bill(self):
        difference = self.total_bill_time() - self.time()
        if difference.total_seconds() < 0:
            return 'Check Time'
        return difference
    '''
    def dfrom(self):
        return self.date_from.strftime("%A %d %B %y | %H:%M")

    def dto(self):
        return self.date_to.strftime("%A %d %B %y | %H:%M")
    
    def __repr__(self):
        return 'Task: '+ str(self.activity) + 'by '+ get_user + ' | ' + self.dfrom() + ' ' + self.dto()
 
class Salitem(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    item = Column(String(255), nullable=True, unique=True)
    references = Column(String(255), nullable=False)
    date = Column(Date, default=datetime.today, nullable=False)
    sal_id = Column(Integer, ForeignKey('sal.id'), nullable=False)
    sal = relationship(Sal)
    kpi = Column(Integer, nullable=False)

    def __repr__(self):
        return self.item
'''


class Billitem(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.today, nullable=False)
    tasks_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    tasks = relationship(Tasks)
    deliverable = Column(String(255), nullable=False)
    doc_quantity = Column(Integer,nullable=False, default=1)
    item = Column(String(255), nullable=True)
    time = Column(Float, nullable=False)
    comments = Column(Text) 
    salitem_id = Column(Integer, ForeignKey('salitem.id'), nullable=True)
    salitem = relationship(Salitem)
    detail_file = Column(FileColumn, nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=True)
    status = relationship(Status) 


'''