from flask import render_template, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, db
from .models import Project, Activity, History
from helpers import upload_project, upload_activity
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction

def get_user():
    return g.user

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""
class ProjectView(ModelView):
    datamodel = SQLAInterface(Project)

class ActivityView(ModelView):
    datamodel = SQLAInterface(Activity)

class HistoryView(ModelView):
    datamodel = SQLAInterface(History)
    base_filters = [['created_by', FilterEqualFunction, get_user]]



appbuilder.add_view(ProjectView, "Project", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(ActivityView, "Activity", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(HistoryView, "History", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
upload_project()
upload_activity()


