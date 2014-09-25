from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from library.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import get_app, get_models
from django.utils.decorators import method_decorator
from library.views import *

# my_aut_urls=[]
# for model in get_models(get_app("library")):
# 	m=str(model._meta)[str(model._meta).find('.')+1:]
# 	s="url(r'^{}'/(?P<pk>\d+)$', SecretDetailView.as_view(model = {}), name='{}_details')".format(m,m,m)
# 	print(s)
# 	my_aut_urls.append(s)
#
# print(my_aut_urls)

urlpatterns = patterns('',
	url('^$', 'library.views.dashboard',name='dashboard'),
  url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'library/login.html'}),
  url(r'^logout/$', 'django.contrib.auth.views.logout'),
	url(r'^uuid/(?P<uuid>[\w\-]+)$', SecretDetailView.as_view(), name='uuid_details'),
	url(r'^search$', SecretListView.as_view(paginate_by = '20'), name='list_search'),
	url(r'^list/(?P<pk>\d+)$', SecretDetailView.as_view(model = Library), name='library_details'),
	url(r'^list$',  SecretListView.as_view(model = Library,paginate_by = '100'), name='library_list'),
	url(r'^new$', SecretCreateView.as_view(model = Library , success_url= reverse_lazy('library_list')), name='library_new'),
  url(r'^delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = Library  , success_url= reverse_lazy('library_list')), name='library_delete'),
	url(r'^library/delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = Library  , success_url= reverse_lazy('library_list')), name='library_delete'),
	url(r'^edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = Library ,success_url= reverse_lazy('library_list')), name='library_edit'),
	url(r'^library/edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = Library ,success_url= reverse_lazy('library_list')), name='library_edit'),
	url(r'^project/(?P<pk>\d+)$', SecretDetailView.as_view(model = Project), name='project_details'),
	url(r'^project/$', SecretListView.as_view(model = Project,paginate_by = '20'), name='project_list'),
	url(r'^project/new$', SecretCreateView.as_view(model = Project , success_url= reverse_lazy('project_list')), name='project_new'),
	url(r'^project/delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = Project  , success_url= reverse_lazy('project_list')), name='project_delete'),
	url(r'^project/edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = Project ,success_url= reverse_lazy('project_list')), name='project_edit'),#   my_aut_urls[10],
)
