from flask import render_template, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, db
import app
from .models import Project, Activity, Kpi, Timesheet, Billitem, Tasks, Cuos, Activity_type, Customer, Order, Sal, Contact, Rate, Status
from helpers import upload_project, upload_activity
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2ManyWidget, Select2SlaveAJAXWidget, DateTimePickerWidget
from flask_appbuilder.actions import action
from flask import redirect
from helpers import update_billable
from flask_appbuilder import AppBuilder, BaseView, expose, has_access
#from .sec_models import MyUser 
#from .sec_views import MyUserDBModelView

def get_user():
    return g.user

class Activity_typeView(ModelView):
    datamodel = SQLAInterface(Activity_type)
    list_columns = ['name']

class BillitemView(ModelView):
    datamodel = SQLAInterface(Billitem)
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    list_columns = ['deliverable','item','time','comments']
    add_columns = ['tasks','item','time','comments']

class TasksView(ModelView):
    datamodel = SQLAInterface(Tasks)
    related_views = [BillitemView]
    label_columns = {
        
        'total_bill_time': 'Bill Time',
        'bill_filename': 'Billable File',
        'dfrom':'From:',
        'dto':'To:'
    }
    #list_columns = ['date','time', 'bill_filename','total_bill_time']
    
    show_columns = ['date','time','total_bill_time','bill_filename']
    
    list_columns = ['activity', 'dfrom','dto','time','total_bill_time', 'task_vs_bill']
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    add_columns = ['date_from','date_to',  'activity','timesheet','billable' ]
    
    edit_columns = ['date_from','date_to','activity','timesheet', 'billable']
    
     
    @action("billupdate", "Bill Update", "Update the Bill, Really?", "fa-rocket", single=True)
    def billupdate(self, items):
        session = db.session
        session.query(Billitem).filter(Billitem.tasks_id == items.id).delete()
        update_billable(items)
        self.update_redirect()
        return redirect(self.get_redirect())
    '''
    def pre_add(self, item):
        ts = item.timesheet
        item.date_to = ts.end_date
        print('pre add function')
        return super().pre_add(item)
    '''
    

    def post_add(self, item):
        if item.billable is not None:
            print('******** ********* ********** ******** start billable add')
            session = db.session
            session.query(Billitem).filter(Billitem.tasks_id == item.id).delete()
            
            update_billable(item)
            print('******** ********* ********** ******** start billable add')

    def post_update(self,item):
        if item.billable is not None:
            print('******** ********* ********** ******** start billable update')
            session = db.session
            session.query(Billitem).filter(Billitem.tasks_id == item.id).delete()
            
            update_billable(item)
            print('******** ********* ********** ******** start billable update')
        
class TimesheetView(ModelView):
    datamodel = SQLAInterface(Timesheet)
    label_columns = {
        'total_time': 'Tasks Time',
        'total_bill_time': 'Bill Time'
    
    }
    add_columns = ['date','status']
    edit_columns = ['date','status']
    list_columns = ['ts_date','total_time','total_bill_time']
    show_columns = ['ts_date','total_time','total_bill_time']
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    related_views = [TasksView]
    

class KpiView(ModelView):
    datamodel = SQLAInterface(Kpi)
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    list_columns = ['date','activity','kpi']
    edit_columns = ['date','activity','kpi']
    add_columns = ['date','activity','kpi']
    add_query_rel_fields = {
        'activity': [['project_id', FilterEqual, 'project_id']]
    }

class ActivityView(ModelView):
    datamodel = SQLAInterface(Activity)
    list_columns = ['name']

class CuosView(ModelView):
    datamodel = SQLAInterface(Cuos)
    related_views = [ActivityView]

class ProjectView(ModelView):
    datamodel = SQLAInterface(Project)
    list_columns = ['name']
    related_views = [ActivityView,CuosView]

class OrderView(ModelView):
    datamodel = SQLAInterface(Order)
    list_columns = ['name']
    related_views = [ProjectView]

class CustomerView(ModelView):
    datamodel = SQLAInterface(Customer)
    list_columns = ['name']
    related_views = [OrderView]

class SalView(ModelView):
    datamodel = SQLAInterface(Sal)
    list_columns = ['name']

class ContactView(ModelView):
    datamodel = SQLAInterface(Contact)
    list_columns = ['name']

class RateView(ModelView):
    datamodel = SQLAInterface(Rate)
    list_columns = ['rate']

class StatusView(ModelView):
    datamodel = SQLAInterface(Status)
    list_columns = ['name']

###########
##  VUE  ##
###########

class AppView(BaseView):
    #route_base = "/ts"
    default_view = 'show'

    @expose('/show/')
    @has_access
    def show(self):
        # do something with param1
        # and return it
        return render_template('timesheet.html')
    '''
    @expose('/app/<string:param1>')
    @has_access
    def app(self, param1):
        # do something with param1
        # and return it
        self.update_redirect()
        return self.render_template('timesheet.html',
                           param1 = param1)
    '''    
appbuilder.add_view(AppView, "AppHome", category='TS APP')
appbuilder.add_link("Home", href='/app/1', category='TS APP')

############
############




appbuilder.add_view(StatusView, "Status", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(SalView, "Sal", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(ContactView, "Contact", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(RateView, "Rate", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')


appbuilder.add_view(CustomerView, "Customer", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(OrderView, "Order", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(ProjectView, "Project", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(CuosView, "CUO List", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(ActivityView, "Activity", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(Activity_typeView, "Activity Type", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
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


