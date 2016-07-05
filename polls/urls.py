from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^signup/$',views.signup,name='signup'),

    url(r'^signedin/$',views.signedin,name='signedin'),
    url(r'^login/$',views.login,name='login'),
    url(r'^loggedin/$',views.loggedin,name='loggedin'),
    url(r'^loggedout/$',views.loggedout,name='loggedout'),
    url(r'^imageview/$',views.imageview,name='imageview'),
    url(r'^loadui/$',views.loadui,name='loadui'),


]
