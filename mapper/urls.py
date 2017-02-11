from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'submit/', views.new_job, name="submit"),
    url(r'results/$', views.recent_jobs),
    url(r'(?i)results/(?P<jobid>[a-zA-Z0-9]+)/$', views.job_results),
]