
'''
from flask_appbuilder.security.sqla.manager import SecurityManager
#from flask_appbuilder.actions import action
from .sec_models import MyUser
from .sec_views import MyUserDBModelView


class MyUserDBView(UserDBModelView):
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())


class MySecurityManager(SecurityManager):
    user_model = MyUser
    userdbmodelview = MyUserDBModelView

'''
