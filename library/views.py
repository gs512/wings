from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse,reverse_lazy
from django.shortcuts import render_to_response,redirect
from django.views.generic import TemplateView,ListView,DetailView,FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.forms import ModelForm
from django.db.models import get_model,get_app, get_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import template
from django.forms.models import inlineformset_factory,BaseInlineFormSet,modelformset_factory,formset_factory,modelform_factory
from django.contrib.messages.views import SuccessMessageMixin
from library.forms import *
from library.models import *
from django.db import transaction
import json,os
from dateutil import parser
from django.views.static import serve
from pprint import pprint
from subprocess import Popen, PIPE
import subprocess, os
from django.core import serializers
import math,numpy
from scipy import stats
import statistics
import collections
# from django_datatables_view.base_datatable_view import BaseDatatableView


# Create your views here.

import logging
logger = logging.getLogger(__name__)

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AjaxTemplateMixin(object):
	def dispatch(self, request, *args, **kwargs):
		if not hasattr(self, 'ajax_template_name'):
			split = self.template_name.split('.html')
			split[-1] = '_inner'
			split.append('.html')
			self.ajax_template_name = ''.join(split)
		if request.is_ajax():
			self.template_name = self.ajax_template_name
		return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

@login_required(login_url='/library/login/')
def drop(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = Attachment(file = request.FILES['file'])
			new_file.name=request.FILES['file']
			new_file.save()
			return HttpResponseRedirect(reverse_lazy('drop'))
	else:
		form = UploadFileForm()

	data = {'form': form}
	return render_to_response('main/index.html', data, context_instance=RequestContext(request))

@login_required(login_url='/library/login/')
def drop_to_library(request, *args, **kwargs):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = Attachment(file = request.FILES['file'])
			new_file.name=request.FILES['file']
			new_file.save()
			l=Library.objects.get(pk=kwargs['pk'])
			l.attachments.add(new_file)
			l.save()
			return HttpResponseRedirect(reverse_lazy('drop_to_library',kwargs={'pk':kwargs['pk']}))
	else:
		form = UploadFileForm()

	data = {'form': form}
	return render_to_response('main/index.html', data, context_instance=RequestContext(request))

@login_required(login_url='/library/login/')
def csv_import(request, *args, **kwargs):
	try:
		TagValues.objects.all().delete()
		p = Project.objects.get(pk=1)
		u = User.objects.get(username="gs")
		for i in Library.objects.all():
			tv=(i.library_alias).split('_')[0]
			t=TagValues(tag=Tag.objects.get(name="cell_time_point"),library=i,tag_value=tv,tag_number=1)
			t.save();
			tv=(i.library_alias).split('_')[1]
			t=TagValues(tag=Tag.objects.get(name="zone"),library=i,tag_value=tv,tag_number=2)
			t.save();
			tv=(i.library_alias).split('_')[2]
			tv=tv[0:3]
			t=TagValues(tag=Tag.objects.get(name="condition"),library=i,tag_value=tv,tag_number=3)
			t.save();




# 		s=open("/home/gas361/wings/tools/gene_exp.diff","r").read().splitlines()[1:]
# 		for v in s:
# 		# 	line=v.replace(',',"_").split('\t')
# 			line = v.split('\t');cond=str(line[4]+","+line[5]);cond_1=line[4];cond_2=line[5];gene=line[0];inf=str(line[9]);FC=0.0;PV=float(line[11]);fpkm_1=float(line[7]);fpkm_2=float(line[8])
# 			if "inf" in inf:
# 				inf=True;fpkm_1=fpkm_1+1;fpkm_2=fpkm_2+1;FC=math.log((fpkm_2/fpkm_1),2)
# 			else :FC=float(inf);inf=False;
#
# 			g=gene_exp(created_by=u,inf=inf,test_id=gene,sample_1=cond_1,sample_2=cond_2,p_value=PV,FC=FC,fpkm_1=fpkm_1,fpkm_2=fpkm_2,q_value=line[12],\
# 			SEM_1=stats.sem([ i['FPKM'] for i in read_group_tracking.objects.filter(project=p,tracking_id=gene,condition=cond_1).values('FPKM')]),\
# 			SEM_2=stats.sem([ i['FPKM'] for i in read_group_tracking.objects.filter(project=p,tracking_id=gene,condition=cond_2).values('FPKM')]));g.save()# 		if request.method == 'POST':
# 			create_log=[]
# 			form = UploadFileForm(request.POST, request.FILES)
# 			if form.is_valid():
# 				new_file = Attachment(file = request.FILES['file'])
# 				new_file.name=request.FILES['file']
# 				new_file.save()
# 				if not (new_file.file.path.endswith('.csv') or new_file.file.path.endswith('.tsv')):
# 					os.remove(new_file.file.path)
# 					new_file.delete()
# 					data = {'class': 'alert alert-danger','msg':"Wrong File Type"}
# 					return HttpResponse(json.dumps(data))
#
# 				myFile=open(new_file.file.path,"r").read().replace('"','').replace("'",'').replace(',',"\t").splitlines()
# 	# 			for i in range(len(myFile)):
# 	# 				while '\t\t' in myFile[i]:myFile[i]=myFile[i].replace('\t\t','\t')
# 				csv=new_file.name
# 				os.remove(new_file.file.path)
# 				new_file.delete()
# 				error=[]



		return HttpResponse(json.dumps({'class':'alert alert-success','msg':ret}))
	except Exception as e:
# 		for i in create_log:i.delete()
		return HttpResponse(json.dumps({'class':'alert alert-success','msg':'something went wrong :'+str(e)}))
# 	data = {'form': UploadFileForm()}
	return HttpResponse(json.dumps({'class':'alert alert-success','msg':ret}))



@login_required(login_url='/library/login/')
def files(request, *args, **kwargs):
	file_id=kwargs['pk']
	a=Attachment.objects.get(pk=file_id)
	return serve(request, a.file.path, "/")


@login_required(login_url='/library/login/')
def dashboard(request):
	return HttpResponseRedirect(reverse('library:dashboard'))

@login_required(login_url='/library/login/')
@transaction.atomic
def multiDel(request):
	Myids=request.POST.getlist('delete_list[]')
	MyModel=request.POST.get('model')
	result = globals()[MyModel]
	ret="Items Deleted !<br>"
	if request.user.is_superuser:
		result.objects.filter(id__in=Myids).delete()

	else :
		result.objects.filter(id__in=Myids,created_by=request.user,is_locked=False).delete()
	return HttpResponse(ret)

@login_required(login_url='/library/login/')
@transaction.atomic
def multiUserAssign(request):
	if request.user.is_superuser:
		Myids=request.POST.getlist('delete_list[]')
		uid=request.POST.get('uid')
		MyModel=request.POST.get('model')
		result = globals()[MyModel]
		for r in result.objects.filter(id__in=Myids):
			r.created_by=User.objects.get(username=uid)
			r.save()
	else :
		Myids=request.POST.getlist('delete_list[]')
		uid=request.POST.get('uid')
		MyModel=request.POST.get('model')
		result = globals()[MyModel]
		for r in result.objects.filter(id__in=Myids,created_by=User.objects.get(username=get_current_user())):
			r.created_by=User.objects.get(username=uid)
			r.save()

	return HttpResponse("Objects Assigned !")

@login_required(login_url='/library/login/')
@transaction.atomic
def multiUnlock(request):
	if request.user.is_superuser:
		Myids=request.POST.getlist('delete_list[]')
		MyModel=request.POST.get('model')
		result = globals()[MyModel]
		for r in result.objects.filter(id__in=Myids):
			if r.is_locked:r.is_locked=False
			else :r.is_locked=True
			r.save()
	return HttpResponse("Objects (Un)locked !")


@login_required(login_url='/library/login/')
@transaction.atomic
def multiLibDup(request):
	Myids=request.POST.getlist('delete_list[]')
	MyModel=request.POST.get('model')
	error=""
	resp=""
	if MyModel!= "Library": return HttpResponse("Error")
	if len(Myids)>0:resp="<p> Libs Duplicated : </p><ul>"
	for r in Library.objects.filter(id__in=Myids):
		if request.user.is_superuser or r.created_by==request.user:
			tmp_lib=Library.objects.get(pk=r.pk)
			r.pk=None
			r.name=r.name+"_"+str(datetime.now())
			r.is_locked=False
			r.save()
			lpc=LibraryBarcodes.objects.filter(library=tmp_lib)
			for l in lpc:
				tmp_l=l
				tmp_l.pk=None
				tmp_l.library=r
				tmp_l.save()
			resp+="<li>"+r.name+"</li>"
		else :
			error+="<li>"+r.name+"</li>"
	if len(error)>0:
		resp+="<p> dup error : </p><ul>"+error+"</ul>"
	else :resp+="</ul>"
	return HttpResponse(resp)


class SecretDetailView(LoginRequiredMixin, DetailView):
	template_name="library/auto_model_detail.html"

	def get_object(self):
		if 'uuid' in self.kwargs:
			for model in get_models(get_app("library")):
				if model.objects.filter(uuid=self.kwargs.get('uuid')):
					return model.objects.get(uuid=self.kwargs.get('uuid'))
		else: return super().get_object()

	def get_context_data(self, **kwargs):
		context = super(SecretDetailView, self).get_context_data(**kwargs)
		return context

	def render_to_response(self, context):
		if self.request.user.is_superuser or self.get_object().created_by==self.request.user:
			return super(SecretDetailView, self).render_to_response(context)
		if self.model==Run:
			if self.get_object() in [lane.run for lane in [pool.lane for pool in LibraryPool.objects.filter(created_by__in=[g.user_set.all().values('id') for g in self.request.user.groups.all()][0])]]:
				return super(SecretDetailView, self).render_to_response(context)
		for g in self.request.user.groups.all():
			if self.get_object().created_by in g.user_set.all():return super(SecretDetailView, self).render_to_response(context)
		return redirect(self.get_object().get_absolute_list_url())

	def get(self, request, *args, **kwargs):
		super(SecretDetailView, self).get(request, *args, **kwargs)
# 		form_file=""
# 		if(self.model is not None and self.model.__name__ == "Library"):
# 			form_file=UploadFileForm()
# 		return self.render_to_response(self.get_context_data(form_file=form_file))
		return self.render_to_response(self.get_context_data())

class SecretListView(LoginRequiredMixin, ListView):
	template_name="library/auto_model_list.html"
	def get(self, request, *args, **kwargs):
		tpl_resp = super(SecretListView, self).get(request, *args, **kwargs)
		if "sequenced" in kwargs or "queued" in kwargs or "in_progress" in kwargs:
			context = self.get_context_data(**kwargs)
			context['no_display']=1
			return self.render_to_response(context)
		return tpl_resp


	def get_queryset(self):
		if "model" in self.request.GET and len(self.request.GET['model'])>0:
			self.model=globals()[self.request.GET['model']]
		else :
			if self.model==None:
				self.model=Library
		queryset = super(SecretListView,self).get_queryset()

		if self.request.user.is_superuser==False:
			q=[]
			for g in self.request.user.groups.all():
				q.append(queryset.filter(created_by=g.user_set.all()))
			f=self.model.objects.none()
			if self.model==Run:
				return [lane.run for lane in [pool.lane for pool in LibraryPool.objects.filter(created_by__in=[g.user_set.all().values('id') for g in self.request.user.groups.all()][0])]]
			for i in q:
				f|=i
			return f
		return queryset

	def get_context_data(self, **kwargs):
		context = super(SecretListView, self).get_context_data(**kwargs)
		context['user_list']=forms.models.ModelChoiceField(User.objects.all())
		if self.request.user.is_superuser:
			context['add_lnk']=self.model.get_add_link()
		context['model']=self.model.__name__
		if self.model.is_user_editable():context['add_lnk']=self.model.get_add_link()
		return context

def formfield_callback(field):
	usr=User.objects.get(username=get_current_user())

	if field.name == 'library' and usr.is_superuser==False:
		q=[]
		for g in usr.groups.all():
			q.append(Library.objects.filter(created_by=g.user_set.all()))
		f=Library.objects.filter(uuid=0)
		for i in q:
			f|=i
		b_list=[]
		for b in f:
			b_list.append((b.id,b.get_name()))
		return forms.ChoiceField(choices = b_list)
	return field.formfield()


class SecretCreateView(LoginRequiredMixin, CreateView):
	template_name="library/auto_model_form.html"
	@transaction.atomic
	def get(self, request, *args, **kwargs):
		super(SecretCreateView, self).get(request, *args, **kwargs)
		form=self.get_form(self.get_form_class())
		formset=""
		form_file=""
		smart_select=""
		formset_type=self.model.__name__
		if(self.model.__name__=="Project"):
			x=[(b.id,b.get_name())  for b in Library.objects.all()]
			form.fields['libraries'].widget.choices=x
	# 		RelatedFormset = modelformset_factory(Library,fields=('library_alias',),formfield_callback=formfield_callback)
	# 		RelatedFormset.form.base_fields['library_alias'].widget.choices=x
	# 		formset = RelatedFormset(queryset=Library.objects.none())
			smart_select=True
# 		RelatedFormset = modelformset_factory(Library,fields=('name','library_alias',),formfield_callback=formfield_callback)


		if(self.request.user.is_superuser):
			return self.render_to_response(self.get_context_data(form=form,formset=formset,form_file=form_file,formset_type=formset_type,smart_select=smart_select))

		if not self.model.is_user_editable():return redirect(reverse('library.views.dashboard'))

		for fi in form.fields:
			if isinstance(form.fields[fi],forms.models.ModelChoiceField) and len(form.fields[fi].queryset)>0 and isinstance(form.fields[fi].queryset[0],auto_model):
				q=[]
				for g in self.request.user.groups.all():
					q.append(form.fields[fi].queryset.filter(created_by=g.user_set.all()))
				f=form.fields[fi].queryset.filter(uuid=0)
				for i in q:
					f|=i
				form.fields[fi].queryset=f
		return self.render_to_response(self.get_context_data(form=form,formset=formset,form_file=form_file,formset_type=formset_type,smart_select=smart_select))

	def post(self, request, *args, **kwargs):
		if not self.request.user.is_superuser and not self.model.is_user_editable():return redirect(reverse('library.views.dashboard'))
		return super(SecretCreateView, self).post(request, *args, **kwargs)
# 		form=self.get_form(self.get_form_class())
# 		formset=""
# 		form_file=""
# 		smart_select=True
# 		formset_type=self.model.__name__

# 		for fi in form.fields:
# 			if isinstance(form.fields[fi],forms.models.ModelChoiceField) and len(form.fields[fi].queryset) >0 and isinstance(form.fields[fi].queryset[0],auto_model):
# 				q=[]
# 				for g in self.request.user.groups.all():
# 					q.append(form.fields[fi].queryset.filter(created_by=g.user_set.all()))
# 				f=form.fields[fi].queryset.filter(uuid=0)
# 				for i in q:
# 					f|=i
# 				form.fields[fi].queryset=f
# 		return self.render_to_response(self.get_context_data(smart_select=smart_select))

	def render_to_response(self, context):
		if not self.request.user.is_superuser and ( self.get_object().is_locked or self.get_object().created_by!=self.request.user):
			return redirect(self.get_object().get_absolute_details_url())
		if(self.model.__name__=="Project"):
			form=self.get_form(self.get_form_class())
			x=[(b.id,b.get_name())  for b in Library.objects.all()]
			form=self.get_form(self.get_form_class())
			form.fields['libraries'].widget.choices=x
			smart_select=True
			context['smart_select']=True
			context['form']=form
		return super(SecretCreateView, self).render_to_response(context)




class SecretDeleteView(LoginRequiredMixin, DeleteView):
	template_name="library/auto_model_confirm_delete.html"
	@transaction.atomic
	def render_to_response(self, context):
		if not self.request.user.is_superuser and ( self.get_object().is_locked or self.get_object().created_by!=self.request.user):
			return redirect(self.get_object().get_absolute_details_url())
		return super(SecretDeleteView, self).render_to_response(context)

class SecretUpdateView(LoginRequiredMixin, SuccessMessageMixin, AjaxTemplateMixin,UpdateView):
	template_name="library/auto_model_form.html"
	@transaction.atomic
	def render_to_response(self, context):
		if not self.request.user.is_superuser and ( self.get_object().is_locked or self.get_object().created_by!=self.request.user):
			return redirect(self.get_object().get_absolute_details_url())
		if(self.model.__name__=="Project"):
			form=self.get_form(self.get_form_class())
			x=[(b.id,b.get_name())  for b in Library.objects.all()]
			form=self.get_form(self.get_form_class())
			form.fields['libraries'].widget.choices=x
			smart_select=True
			context['smart_select']=True
			context['form']=form
		return super(SecretUpdateView, self).render_to_response(context)

class SecretJsonView(LoginRequiredMixin,ListView):
	columns=[]
	def dispatch(self, request, *args, **kwargs):
		a=super(SecretJsonView, self).get(request, *args, **kwargs)
		cmp=(kwargs['cmd'][1:]).split(',')
		self.columns=cmp
		
# 		for x in cmp:
# 			self.columns.append(x)
# 			self.columns.append('FC')
# 			self.columns.append('p_value')
		return HttpResponse(json.dumps(self.get_queryset()), content_type="application/json")
		return(a)

	def get_queryset(self):
		p=Project.objects.get(pk=1)
		res={}
		glist=read_group_tracking.objects.filter(project=p).values_list('tracking_id').distinct()[:5]
# 		print(glist)
		res=[]
		for gene in glist:
			tmp_d=collections.OrderedDict()	
			g=gene[0]
# 			tmp_d['id']=g[1]
			tmp_d["gene_id"]=g
			for x in self.columns:
				x=x.split(' ')
				tmp=gene_exp.objects.filter(sample_1=x[0],sample_2=x[1],test_id=g).values_list('FC','p_value')
# 				res[g][str(' '.join(x))]=tmp[0]
				tmp_d[(str('_'.join(x))+"_FC").lower()]=tmp[0][0]
				tmp_d[(str('_'.join(x))+"_p_value").lower()]=tmp[0][1]
				
			res.append(tmp_d)
				
		return({"records":res,"queryRecordCount":len(res),"totalRecordCount":read_group_tracking.objects.filter(project=p).values_list('tracking_id').distinct().count() })
		
def get_head(request, *args, **kwargs):
	cmp=(kwargs['cmd'][1:]).split(',')
	ret="<th>gene_id</th>"
	for x in cmp:
		x=x.replace(' ','_').lower()
		ret+=("<th>{}_fc</th><th>{}_p_value</th>").format(x,x)
	return HttpResponse("<thead>"+ret+"</thead><tbody></tbody>")

# 		return read_group_tracking.objects.filter(pk=1) 
		
	
# class OrderListJson(BaseDatatableView):
# 	model = gene_exp
# 
# 	# define the columns that will be returned
# 	columns = ['test_id', 'FC', 'p_value']
# 
# 	# define column names that will be used in sorting
# 	# order is important and should be same as order of columns
# 	# displayed by datatables. For non sortable columns use empty
# 	# value like ''
# 	order_columns = ['test_id', 'FC', 'p_value']
# 
# 	# set max limit of records returned, this is used to protect our site if someone tries to attack our site
# 	# and make it return huge amount of data
# 	max_display_length = 50
# 
# 	def get(self, request, *args, **kwargs):
# 		a=super(BaseDatatableView, self).get(request, *args, **kwargs)
# 		cmp=(kwargs['cmd'][1:]).split(',')
# 		self.columns=['test_id']
# 		for x in cmp:
# 			self.columns.append(x)
# 			self.columns.append('FC')
# 			self.columns.append('p_value')
# 		self.order_columns = self.columns[:]
# 		print(self.order_columns)
# 		return(a)
# 
# 	def render_column(self, row, column):
# 	    # We want to render user as a custom column
# 	    if column == 'user':
# 	        return '{0} {1}'.format(row.customer_firstname, row.customer_lastname)
# 	    else:
# 	        return super(OrderListJson, self).render_column(row, column)
# 
# 	def filter_queryset(self, qs):
# 	    # use parameters passed in POST request to filter queryset
# 
# 	    # simple example:
# 	    search = self.request.POST.get('search[value]', None)
# 	    if search:
# 	        qs = qs.filter(cond_1=search)
# 
# 	    # more advanced example using extra parameters
# 	    filter_customer = self.request.POST.get('cond_2', None)
# 
# # 	    if filter_customer:
# # 	        customer_parts = filter_customer.split(' ')
# # 	        qs_params = None
# # 	        for part in customer_parts:
# # 	            q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
# # 	            qs_params = qs_params | q if qs_params else q
# # 	        qs = qs.filter(qs_params)
# 	    return qs