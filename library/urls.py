from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from library.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import get_app, get_models
from django.utils.decorators import method_decorator
from library.views import *

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
# my_aut_urls=[]
# for model in get_models(get_app("library")):
# 	m=str(model._meta)[str(model._meta).find('.')+1:]
# 	s="url(r'^{}'/(?P<pk>\d+)$', SecretDetailView.as_view(model = {}), name='{}_details')".format(m,m,m)
# 	print(s)
# 	my_aut_urls.append(s)
#
# print(my_aut_urls)

dajaxice_autodiscover()


urlpatterns = patterns('',
	url('^$', SecretListView.as_view(model = Library,paginate_by = '100'),name='dashboard'),
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
	url(r'^tagvalues/(?P<pk>\d+)$', SecretDetailView.as_view(model = TagValues), name='tagvalues_details'),
	url(r'^tagvalues/$', SecretListView.as_view(model = TagValues,paginate_by = '20'), name='tagvalues_list'),
	url(r'^tagvalues/new$', SecretCreateView.as_view(model = TagValues , success_url= reverse_lazy('tagvalues_list')), name='tagvalues_new'),
	url(r'^tagvalues/delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = TagValues  , success_url= reverse_lazy('tagvalues_list')), name='tagvalues_delete'),
	url(r'^tagvalues/edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = TagValues ,success_url= reverse_lazy('tagvalues_list')), name='tagvalues_edit'),
  url(r'^drop/(?P<pk>\d+)$', 'library.views.drop_to_library',name='drop_to_library'),
	url(r'^tag/(?P<pk>\d+)$', SecretDetailView.as_view(model = Tag), name='tag_details'),
	url(r'^tag/$', SecretListView.as_view(model = Tag,paginate_by = '20'), name='tag_list'),
	url(r'^tag/new$', SecretCreateView.as_view(model = Tag , success_url= reverse_lazy('tag_list')), name='tag_new'),
	url(r'^tag/delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = Tag  , success_url= reverse_lazy('tag_list')), name='tag_delete'),
	url(r'^tag/edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = Tag ,success_url= reverse_lazy('tag_list')), name='tag_edit'),
	url(r'^csv_import/$', 'library.views.csv_import',name='csv_import'),
	url(r'^data(?P<cmd>(?:/[^/]+)+)$', SecretJsonView.as_view(), name='order_list_json'),
	url(r'^gene_exp/(?P<pk>\d+)$', SecretDetailView.as_view(model = gene_exp), name='gene_exp_details'),
	url(r'^gene_exp/$', SecretListView.as_view(model = gene_exp,paginate_by = '20'), name='gene_exp_list'),
	url(r'^gene_exp/new$', SecretCreateView.as_view(model = gene_exp , success_url= reverse_lazy('gene_exp_list')), name='gene_exp_new'),
	url(r'^gene_exp/delete/(?P<pk>\d+)$', SecretDeleteView.as_view(model = gene_exp  , success_url= reverse_lazy('gene_exp_list')), name='gene_exp_delete'),
	url(r'^gene_exp/edit/(?P<pk>\d+)$', SecretUpdateView.as_view(model = gene_exp ,success_url= reverse_lazy('gene_exp_list')), name='gene_exp_edit'),
	url(r'^table(?P<cmd>(?:/[^/]+)+)$', SecretListView.as_view(template_name='library/auto_model_table.html'),name="cmp_table"),
	url(r'^get_head(?P<cmd>(?:/[^/]+)+)$', 'library.views.get_head',name="get_head"),

)
