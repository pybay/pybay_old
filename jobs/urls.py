from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name="job_list"),
    url(r'submit/$', views.create, name="job_create"),
    url(r'thanks/$', views.thanks, name="job_thanks"),
    url(r'(?P<slug>[\w-]+)/$', views.detail, name="job_detail"),
]
