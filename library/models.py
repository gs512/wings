# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.fields import UUIDField
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from datetime import datetime
from library.current_user import get_current_user,get_current_user_groups,get_current_user_is_super

# Create your models here.
class auto_model(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User,default=get_current_user,editable=False)
	uuid = UUIDField(auto=True,editable=False)
	is_locked = models.BooleanField(editable=False,default=False)

	def get_fields(self):
		for field in self._meta.fields:
			if field.get_internal_type() == "ForeignKey" and getattr(self,field.name)!=None :
				tmp=field.related.parent_model.objects.get(pk=field.value_to_string(self))
				if hasattr(tmp,'get_absolute_details_url'):
					tmp=("<a href='{}'>{}</a>").format(tmp.get_absolute_details_url(),(getattr(self,field.name)).get_name())
				else :tmp=getattr(self,field.name)
				f.append([field.verbose_name,mark_safe(tmp)])
			else :
				f.append([field.verbose_name,getattr(self,field.name)])
		f.append(["URI",mark_safe(("<a href='{}'>{}</a>").format(self.get_uuid_url(),"Direct Link"))])
		f[0]=''
		return f

	def get_meta_name(self):
		return self.__class__.__name__
	def __unicode__(self):
		if hasattr(self, 'name'):return self.name
		else: return self.get_name()

	def get_name(self):
		if hasattr(self, 'name'):return self.name
		else: return self.get_name()

	def get_id(self):
		return self.id
	def get_absolute_edit_url(self):
		return reverse((self.__class__.__name__+'_edit').lower(), kwargs={'pk': self.pk})
	def get_absolute_delete_url(self):
		return reverse((self.__class__.__name__+'_delete').lower(), kwargs={'pk': self.pk})
	def get_absolute_details_url(self):
		return reverse((self.__class__.__name__+'_details').lower(), kwargs={'pk': self.pk})
	def get_absolute_create_url(self):
		return reverse((self.__class__.__name__+'_new').lower())
	def get_absolute_list_url(self):
		return reverse((self.__class__.__name__+'_list').lower())
	def get_uuid_url(self):
		return reverse('uuid_details', kwargs={'uuid':self.uuid})
	def is_user_editable(self):return False

	def has_status(self): return False
	def get_absolute_url(self):
		return self.get_absolute_edit_url()

	class Meta:
		abstract = True

class Library(auto_model):
	library_id = models.CharField(max_length=255,verbose_name="Library ID")
