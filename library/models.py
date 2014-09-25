# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django_extensions.db.fields import UUIDField
from datetime import datetime
from library.current_user import get_current_user,get_current_user_groups,get_current_user_is_super

# Create your models here.
class auto_model(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User,default=get_current_user,editable=False)
	uuid = UUIDField(auto=True,editable=False)
	is_locked = models.BooleanField(editable=False,default=False)
	name = models.CharField(max_length=255,null=True,blank=True,editable=False)

# 	def __init__(self, *args, **kwargs):
# 		models.Model.__init__(self, *args, **kwargs)
# 		if "name" not in kwargs:
# 			self.name=self.object.__class__.__name__+"_"+self.object.id

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
	reads_type	= models.CharField(max_length=255,verbose_name="Reads Type",null=True)
	flowcell_id	= models.CharField(max_length=255,verbose_name="Flowcell Id",null=True,blank=True)
	determined_reads = models.IntegerField(verbose_name="Determined Reads #",null=True,blank=True)
	average_phred	 = models.CharField(max_length=255,verbose_name="Average Phred",null=True,blank=True)
	qc_report_url	= models.URLField(verbose_name="QC URL",null=True,blank=True)
	ercc_r2	= models.FloatField(null=True,blank=True)
	ercc_mix = models.CharField(max_length=10,null=True,blank=True)
	ercc_dilution = models.FloatField(null=True,blank=True)
	reads_mapped_refseq = models.IntegerField(null=True,blank=True)
	reads_mapped_ercc = models.IntegerField(null=True,blank=True)
	reads_mapped_ercc_portion = models.FloatField(verbose_name="Reads Mapped ERCC (%)",null=True,blank=True)
	n = models.IntegerField(null=True,blank=True)
	ercc_url = models.URLField(verbose_name="ERCC URL",null=True,blank=True)
	library_alias = models.TextField(null=True,blank=True)
	reads_mapped_refseq = models.IntegerField(null=True,blank=True)
# 	pool_id
# 	lane_id
# 	tube_id
# 	ordered
# 	barcode_id
# 	portion_pool_(%)
	lld = models.IntegerField(null=True,blank=True)
	replicate = models.IntegerField(default=1)

class Tag(auto_model):
	libraries_group = models.ManyToManyField(Library, through='TagValues',through_fields=('tag','library'))

class TagValues(auto_model):
	tag = models.ForeignKey(Tag)
	library = models.ForeignKey(Library)
	tag_value = models.CharField(max_length=255)
	tag_number = models.IntegerField()

class Project(auto_model):
	libraries = models.ManyToManyField(Library)