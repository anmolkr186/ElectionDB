from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path("login", views.login, name = "login"),
    path("updater", views.updater, name = "updater"),
    path("queryprocess", views.queryprocess, name = "queryprocess"),
    path("votinglogin", views.votinglogin, name = "votinglogin"),
    path("votingcast", views.votingcast, name = "votingcast"),
    path("voterdashboard", views.voterdashboard, name = "voterdashboard"),
    path("datalessquery", views.datalessquery, name="datalessquery"),
    # path("api/data", views.tabledata, name = "api-data"),
    
]
