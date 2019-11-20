from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^loginReg$', views.loginReg),
    url(r'^processReg$', views.processReg),
    url(r'^processLogin$', views.processLogin),
    url(r'^(?P<userID>\d+)/about$', views.about),
    url(r'^(?P<userID>\d+)/makeAppointment$', views.schedule),
    url(r'^(?P<userID>\d+)/review$', views.review),
    url(r'^(?P<userID>\d+)/processReview$', views.processReview),
    url(r'^(?P<userID>\d+)/edit$', views.edit),
    url(r'^(?P<userID>\d+)/addReview$', views.addReview),
    url(r'^(?P<userID>\d+)/processEdit$', views.processEdit),
    url(r'^(?P<userID>\d+)/processRequest$', views.processRequest),
    url(r'^(?P<userID>\d+)/appointments$', views.appointments),
    url(r'^(?P<userID>\d+)/likeReview$', views.likeReview),
    url(r'^(?P<userID>\d+)/takeAppointment$', views.takeAppointment),
    url(r'^(?P<userID>\d+)/appointments/delete$', views.deleteAppointment),
    url(r'^logout$', views.logout),
    url(r'^index$', views.index),
]