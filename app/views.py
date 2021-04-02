from logging import exception
from flask import render_template, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder.security.decorators import protect
from app import appbuilder, db
import app
from .models import Project, Activity, Kpi, Timesheet, Tasks, Cuos, Activity_type, Customer, Order, Sal, Contact, Rate, Status, Tsfiles
from helpers import upload_project, upload_activity
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual, FilterInFunction
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2ManyWidget, Select2SlaveAJAXWidget, DateTimePickerWidget
from flask_appbuilder.actions import action
from flask import redirect
#from helpers import update_billable
from flask_appbuilder import AppBuilder, BaseView, expose, has_access
#from .sec_models import MyUser 
#from .sec_views import MyUserDBModelView
from .sec_models import MyUser
def get_user():
    return g.user

def get_activity():
    return [x.name for x in g.user.activity]

class Activity_typeView(ModelView):
    datamodel = SQLAInterface(Activity_type)
    list_columns = ['name']
'''
class BillitemView(ModelView):
    datamodel = SQLAInterface(Billitem)
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    label_columns = {
        'item': 'SAL Item',
        'deliverable': 'Reference'
    
    }
    list_columns = ['item','salitem','deliverable','comments','time']  
    add_columns = ['tasks', 'deliverable', 'doc_quantity' ,'item','salitem','time','comments']
'''
from helpers import tasks_update
class TsfilesView(ModelView):
    datamodel = SQLAInterface(Tsfiles)
    base_filters = [['created_by', FilterEqualFunction, get_user]]

    def post_add(self, item):
        tasks_update(self,item)
        #return super().post_add(item)

from helpers import tasks_update
class TasksView(ModelView):
    datamodel = SQLAInterface(Tasks)
    #related_views = [BillitemView]
    label_columns = {
        'dfrom':'From:',
        'dto':'To:'
    }
    def post_add(self, item):
        tasks_update(item)
        return super().post_add(item)
    #list_columns = ['date','time', 'bill_filename','total_bill_time']
    
    show_columns = ['date','time']
    
    list_columns = ['activity', 'dfrom','dto','time']
    base_filters = [['created_by', FilterEqualFunction, get_user]]
    add_form_query_rel_fields = {'activity':[['name', FilterInFunction, get_activity]]}
    add_columns = ['date_from','date_to',  'activity','timesheet' ]
    
    edit_columns = ['date_from','date_to','activity','timesheet']
    
    ''' 
    @action("billupdate", "Bill Update", "Update the Bill, Really?", "fa-rocket", single=True)
    def billupdate(self, items):
        session = db.session
        session.query(Billitem).filter(Billitem.tasks_id == items.id).delete()
        update_billable(items)
        self.update_redirect()
        return redirect(self.get_redirect())
    '''
    '''
    def pre_add(self, item):
        ts = item.timesheet
        item.date_to = ts.end_date
        print('pre add function')
        return super().pre_add(item)
    '''
    def pre_add(self, item):
        from flask import abort, Response, flash
        
        if item.date_from > item.date_to:
            flash('Wrong dates! Task failed.', category='warning')
            abort(400)

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
    '''    
class TimesheetView(ModelView):
    datamodel = SQLAInterface(Timesheet)
    label_columns = {
        'total_time': 'Tasks Time'
    }
    add_columns = ['date','status']
    edit_columns = ['date','status']
    list_columns = ['id','ts_date','total_time']
    show_columns = ['ts_date','total_time']
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
    add_columns = ['name','activity_type','cuos','bill_file_required','status']
    

class CuosView(ModelView):
    datamodel = SQLAInterface(Cuos)
    related_views = [ActivityView]
    list_columns = ['project','code']
    add_columns = ['project','code', 'description']

class ProjectView(ModelView):
    datamodel = SQLAInterface(Project)
    list_columns = ['name']
    related_views = [ActivityView,CuosView]
    #add_columns = ['cuos','name']
    add_columns = ['name','order']

class OrderView(ModelView):
    datamodel = SQLAInterface(Order)
    list_columns = ['name']        
    add_columns = ['customer','name']
    related_views = [ProjectView]

class CustomerView(ModelView):
    datamodel = SQLAInterface(Customer)
    list_columns = ['name']
    add_columns = ['name']
    related_views = [OrderView]

from .models import Salitem

class SalitemView(ModelView):
    datamodel = SQLAInterface(Salitem)
    list_columns = ['id','item','references','sal']

class SalView(ModelView):
    datamodel = SQLAInterface(Sal)
    
    related_views = [SalitemView]

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
from flask import jsonify, make_response
class AppView(BaseView):
    #route_base = "/ts"
    default_view = 'show'

    @expose('/show/') 
    @has_access
    def show(self):
        # do something with param1
        # and return it
        letters = {
            'a':'letter A',
            'b':'letter B'
        } 
        return render_template('timesheet.html',
                    base_template=appbuilder.base_template, 
                    appbuilder=appbuilder, letters=jsonify(letters)) 
    
    @expose('/ts/')
    @has_access
    def ts_all(self):
        session = db.session
        my_ts = session.query(Timesheet).filter(Timesheet.created_by_fk == g.user.id).all()
        self.update_redirect()
        ts = {}
        a = [(t.id,t.date) for t in my_ts]
        ts.update(a)
        return [ts]
    
    @expose('/ts2/')
    @has_access
    def ts_all(self):
        session = db.session
        my_ts = session.query(Timesheet).filter(Timesheet.created_by_fk == g.user.id).all()
        self.update_redirect()
        for t in my_ts:
            print(t)
        ts = {}
        #a = [{'id':t.id,'data':t.date} for t in my_ts]
        a = [(t.id,t.date) for t in my_ts]
        ts.update(a)
        print(ts)
        return ts


    @expose('/ts/<int:id>')
    @has_access
    def ts(self,id):
        session = db.session
        t = session.query(Timesheet).filter(
                                Timesheet.created_by_fk == g.user.id,
                                Timesheet.id == id
                                ).first()
        self.update_redirect()
        if t:
            ts = {}
            ts.update([(t.id,t.date)])
            return ts
        return 'not found'


    @expose('/myuser/')
    @has_access
    def myuser(self):
        return {'user': str(g.user)} 
    '''
    @expose('/timesheet/<int:id>')
    @has_access
    def timesheet(self,id):
        session = db.session
        t = session.query(Timesheet).filter(
                                Timesheet.created_by_fk == g.user.id,
                                Timesheet.id == id
                                ).first()
        self.update_redirect()
        ts = {}
        ts.update((t.id,t.date))
        return ts
    '''    
from flask_appbuilder.api import ModelRestApi

class ProjectModelApi(ModelRestApi):
    resource_name = 'project'
    datamodel = SQLAInterface(Project)

    @expose('/all')
    @protect()
    def all(self):
        return self.response(200, message="This is ALL")


appbuilder.add_api(ProjectModelApi)


appbuilder.add_view(AppView, "AppHome", category='TS APP')
#appbuilder.add_link("Home", href='/app/1', category='TS APP')

############
############

appbuilder.add_view(StatusView, "Status", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(SalView, "Sal", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(SalitemView, "Salitem", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')
appbuilder.add_view(TsfilesView, "TS Files", icon="fa-folder-open-o", category="Setting", category_icon='fa-folder-open-o')

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
#appbuilder.add_view(BillitemView, "Billable Items", icon="fa-folder-open-o", category="Timesheet", category_icon='fa-folder-open-o')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
#upload_project()
#upload_activity()

from helpers import upload_pm_items
#pload_pm_items() 
