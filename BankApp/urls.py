from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('add_account',views.add_account,name='add_account'),
    path('acc_details',views.acc_details,name='acc_details'),
    path('transaction',views.transaction,name='transaction'),
    path('branches',views.branches,name='branches'),
    path('about',views.about,name='about'),
    path('admin',views.admin,name='admin'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('view_customers',views.view_customers,name='view_customers'),
    path('contact_admin',views.contact_admin,name='contact_admin'),
    path('view_queries',views.view_queries,name='view_queries')

]