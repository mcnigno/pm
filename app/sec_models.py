'''
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model

from .models import Activity


assoc_activity_users = Table('activity_users', Model.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('activity_id', Integer, ForeignKey('activity.id')),
                                      Column('myuser_id', Integer, ForeignKey('ab_user.id'))
)

class MyUser(User):
    __tablename__ = 'ab_user'
    extra = Column(String(256))
    #activity = relationship("Activity",secondary=assoc_activity_users, backref="users" )


'''