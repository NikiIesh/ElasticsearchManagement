
from django.urls import path,re_path
from .views import *

urlpatterns = [
                   #path(r'deleteall/', Delete.as_view()),
                   path(r'cluster/', BackendList.as_view()),
                   re_path(r'^cluster/(?P<id>\w+)/$',BackendList.as_view()),
                    path(r'node/', NodeInfo.as_view()),
                    re_path(r'^node/(?P<id>\w+)/$',NodeInfo.as_view()),
                    path(r'index/', Indices.as_view()),
                    path(r'health/', Health.as_view()),path(r'stats/', Stats.as_view()),
              ]