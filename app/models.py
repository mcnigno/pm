from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date 
from sqlalchemy.orm import relationship
import datetime
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class Project(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    project = Column(String(255), nullable=False)

    def __repr__(self):
        return self.project

class Activity(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    activity = Column(String(255), nullable=False)

    def __repr__(self):
        return self.activity

class History(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.datetime.now().strftime('%Y-%m-%d'))
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship(Project)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    activity = relationship(Activity)
    quantity = Column(Integer, nullable=False)

