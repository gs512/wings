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
from django.forms.models import inlineformset_factory,BaseInlineFormSet,modelformset_factory,formset_factory
from django.contrib.messages.views import SuccessMessageMixin
from library.forms import *
from library.models import *
from django.db import transaction
import json
from django.views.static import serve

# Create your views here.
import logging
logger = logging.getLogger(__name__)

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

@login_required(login_url='/library/login/')
def dashboard(request):
	if request.method == 'POST':
		return HttpResponseRedirect(reverse('library:dashboard'))
	else:
		return render_to_response('base.html', context_instance=RequestContext(request))


@login_required(login_url='/library/login/')
@transaction.atomic
def multiDel(request):
	Myids=request.POST.getlist('delete_list[]')
	MyModel=request.POST.get('model')
	result = globals()[MyModel]
	ret="Items Delted !<br>"
	if request.user.is_superuser:
		result.objects.filter(id__in=Myids).delete()

	else :
		for r in result.objects.filter(id__in=Myids,created_by=request.user,is_locked=False):
			r.delete()
			ret+="<li>"+r.get_name()+"</li>"
	return HttpResponse(ret)


@login_required(login_url='/library/login/')
@transaction.atomic
def multiUnlock(request):
	if request.user.is_superuser:
		Myids=request.POST.getlist('delete_list[]')
		MyModel=request.POST.get('model')
		result = globals()[MyModel]
		for r in result.objects.filter(id__in=Myids):
			r.is_locked=False
			r.save()
	return HttpResponse("Objects Unlocked !")

@login_required(login_url='/library/login/')
@transaction.atomic
def multiSubmit(request):
	Myids=request.POST.getlist('delete_list[]')
	MyModel=request.POST.get('model')
	result = globals()[MyModel]
	error=""
	submited=""
	removed=""
	err_h="<p>There was an error with the following libraries :</p><ul>"
	sub_h="<p>There was an error with the following libraries :</p><ul>"
	rem_h="<p>There was an error with the following libraries :</p><ul>"
	resp=""
	for r in result.objects.filter(id__in=Myids):
		if request.user.is_superuser or r.created_by==request.user:
			removed+="<li>"+r.name+"</li>"
			r.save()
		else :
			error+="<li>"+r.name+"</li>"
		if len(error)>0:
			resp+=err_h+error+"</ul>"
		if len(removed)>0:
			resp+=rem_h+removed+"</ul>"
	return HttpResponse(resp)




class SecretDetailView(LoginRequiredMixin, DetailView):
	template_name="library/auto_model_detail.html"

	def get_object(self):
		if 'uuid' in self.kwargs:
			for model in get_models(get_app("library")):
				if model.objects.filter(uuid=self.kwargs.get('uuid')):
					return model.objects.get(uuid=self.kwargs.get('uuid'))
		else: return super().get_object()


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
				q.append(self.model.objects.filter(created_by=g.user_set.all()))
			f=self.model.objects.filter(uuid=0)
			for i in q:
				f|=i
			return f
		return queryset

	def get_context_data(self, **kwargs):
		context = super(SecretListView, self).get_context_data(**kwargs)
		if self.request.user.is_superuser:
			context['user_list']=forms.models.ModelChoiceField(User.objects.all())
		context['model']=self.model.__name__# .objects.latest('uuid').get_meta_name()
		return context

class SecretCreateView(LoginRequiredMixin, CreateView):
	template_name="library/auto_model_form.html"

class SecretDeleteView(LoginRequiredMixin, DeleteView):
	template_name="library/auto_model_confirm_delete.html"
	@transaction.atomic
	def render_to_response(self, context):
		if not self.request.user.is_superuser and not self.get_object().is_locked and  self.get_object().created_by!=self.request.user:
			return redirect(self.get_object().get_absolute_details_url())
		return super(SecretDeleteView, self).render_to_response(context)

class SecretUpdateView(LoginRequiredMixin, SuccessMessageMixin,UpdateView):
	template_name="library/auto_model_form.html"
	@transaction.atomic
	def render_to_response(self, context):
		if not self.request.user.is_superuser and not self.get_object().is_locked and self.get_object().created_by!=self.request.user:
			return redirect(self.get_object().get_absolute_details_url())
		return super(SecretUpdateView, self).render_to_response(context)

