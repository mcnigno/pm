from flask import render_template, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, db
from .models import Project, Activity, Kpi, Timesheet, Billitem, Tasks, Cuos
from helpers import upload_project, upload_activity
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2ManyWidget, Select2SlaveAJAXWidget
from flask_appbuilder.actions import action
from flask import redirect
from helpers import update_billable

def get_user():
    return g.user

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""
class ActivityView(ModelView):
    datamodel = SQLAInterface(Activity)
    list_columns = ['name']





class KpiView(ModelView):
    datamodel = SQLAInterface(Kpi)
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    list_columns = ['date','project','activity','kpi']
    edit_columns = ['date','project','activity','kpi']
    add_columns = ['date','project','activity','kpi']
    add_query_rel_fields = {
        'activity': [['project_id', FilterEqual, 'project_id']]
    }


class BillitemView(ModelView):
    datamodel = SQLAInterface(Billitem)
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    list_columns = ['item','time','comments']
    add_columns = ['tasks','item','time','comments']

class TasksView(ModelView):
    datamodel = SQLAInterface(Tasks)
    related_views = [BillitemView]
    label_columns = {
        
        'total_bill_time': 'Bill Time',
        'bill_filename': 'Billable File',
        'cuos': 'CUO'
    }
    #list_columns = ['date','time', 'bill_filename','total_bill_time']
    show_columns = ['date','time','total_bill_time','bill_filename']
    
    list_columns = ['project','activity','cuos', 'date_from','date_to','time','total_bill_time', 'task_vs_bill']
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    add_columns = ['date_from','date_to', 'project','activity','timesheet','cuos', 'billable' ]
    add_form_extra_fields = {
                    'project': AJAXSelectField('Project',
                    description='This will be populated with AJAX',
                    datamodel=datamodel,
                    col_name='project',
                    widget=Select2AJAXWidget(endpoint='/tasksview/api/column/add/project')),
                    '''
                    'cuos': AJAXSelectField('CUO',
                    description='Extra Field description',
                    datamodel=datamodel,
                    col_name='cuos',
                    widget=Select2SlaveAJAXWidget(master_id='project',
                    endpoint='/tasksview/api/column/add/cuos?_flt_0_project_id={{ID}}')),
                    '''
                    'activity': AJAXSelectField('Activity',
                    description='Extra Field description',
                    datamodel=datamodel,
                    col_name='activity',
                    widget=Select2SlaveAJAXWidget(master_id='project',
                    endpoint='/tasksview/api/column/add/activity?_flt_0_project_id={{ID}}'))
                    } 
    edit_columns = ['date_from','date_to', 'project','activity','timesheet', 'cuos','billable' ]
    edit_form_extra_fields = {
                    'project': AJAXSelectField('Project',
                    description='This will be populated with AJAX',
                    datamodel=datamodel,
                    col_name='project',
                    widget=Select2AJAXWidget(endpoint='/tasksview/api/column/add/project')),
                    '''
                    'cuos': AJAXSelectField('CUO',
                    description='Extra Field description',
                    datamodel=datamodel,
                    col_name='cuos',
                    widget=Select2SlaveAJAXWidget(master_id='project',
                    endpoint='/tasksview/api/column/add/cuos?_flt_0_project_id={{ID}}')),
                    '''
                    'activity': AJAXSelectField('Activity',
                    description='Extra Field description',
                    datamodel=datamodel,
                    col_name='activity',
                    widget=Select2SlaveAJAXWidget(master_id='project',
                    endpoint='/tasksview/api/column/add/activity?_flt_0_project_id={{ID}}'))
                    } 
    @action("billupdate", "Bill Update", "Update the Bill, Really?", "fa-rocket", single=True)
    def billupdate(self, items):
        session = db.session
        session.query(Billitem).filter(Billitem.tasks_id == items.id).delete()
        update_billable(items)
        self.update_redirect()
        return redirect(self.get_redirect())
    
    
    def post_add(self,item):
        session = db.session
        session.query(Billitem).filter(Billitem.tasks_id == item.id).delete()
        update_billable(item)
        


class TimesheetView(ModelView):
    datamodel = SQLAInterface(Timesheet)
    label_columns = {
        'total_time': 'Tasks Time',
        'total_bill_time': 'Bill Time'
    
    }
    add_columns = ['date']
    edit_columns = ['date']
    list_columns = ['date','total_time','total_bill_time']
    show_columns = ['date','total_time','total_bill_time']
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    related_views = [TasksView]



    

class CuosView(ModelView):
    datamodel = SQLAInterface(Cuos)


class ProjectView(ModelView):
    datamodel = SQLAInterface(Project)
    list_columns = ['name']
    related_views = [ActivityView,KpiView]


appbuilder.add_view(ProjectView, "Project", icon="fa-folder-open-o", category="Project", category_icon='fa-folder-open-o')
appbuilder.add_view(CuosView, "CUO List", icon="fa-folder-open-o", category="Timesheet", category_icon='fa-folder-open-o')

appbuilder.add_view(ActivityView, "Activity", icon="fa-folder-open-o", category="Project", category_icon='fa-folder-open-o')
appbuilder.add_view(KpiView, "Kpi", icon="fa-folder-open-o", category="Reporting", category_icon='fa-folder-open-o')

appbuilder.add_view(TimesheetView, "Time Sheet", icon="fa-folder-open-o", category="Timesheet", category_icon='fa-folder-open-o')
appbuilder.add_view(TasksView, "Project Tasks", icon="fa-folder-open-o", category="Timesheet", category_icon='fa-folder-open-o')
appbuilder.add_view(BillitemView, "Billable Items", icon="fa-folder-open-o", category="Timesheet", category_icon='fa-folder-open-o')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
#upload_project()
#upload_activity()


