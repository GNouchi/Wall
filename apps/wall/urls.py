from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^message$', views.message ),
    url(r'^comment$', views.comment ),
    url(r'^message/destroy$', views.destroymessage ),
    url(r'^comment/destroy$', views.destroycomment ),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^wall$', views.wall ),
    url(r'^logout$', views.logout ),
    url(r'^$', views.index ),
]