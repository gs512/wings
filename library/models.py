# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django_extensions.db.fields import UUIDField
from datetime import datetime
from library.current_user import get_current_user,get_current_user_groups,get_current_user_is_super
from natsort import natsorted
import pprint
# Create your models here.

def modify_fields(**kwargs):
	def wrap(cls):
			for field, prop_dict in kwargs.items():
					for prop, val in prop_dict.items():
							setattr(cls._meta.get_field(field), prop, val)
			return cls
	return wrap



class auto_model(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User,default=get_current_user,editable=False)
	uuid = UUIDField(auto=True,editable=False)
	is_locked = models.BooleanField(editable=False,default=False)
	last_modified = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=255,null=True,blank=True,editable=True)


	def get_fields(self):
		f=[]
		if not get_current_user_is_super():
			for field in self._meta.fields:
				if field.verbose_name not in ['created at','is locked','Sequencer','lane','Libraries Pooled','uuid']:
					f.append([field.verbose_name,getattr(self,field.name)])
			f.append(["URI",mark_safe(("<a href='{}'>{}</a>").format(self.get_uuid_url(),"Direct Link"))])
		else:
			for field in self._meta.fields:
				if field.get_internal_type() == "ForeignKey" and getattr(self,field.name)!=None :
# 					print(field.related.parent_model,vars(field.related))
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
		if not get_current_user_is_super() and self.is_locked:return "#"
		return reverse((self.__class__.__name__+'_edit').lower(), kwargs={'pk': self.pk})
	def get_absolute_delete_url(self):
		if not get_current_user_is_super() and self.is_locked:return "#"
		return reverse((self.__class__.__name__+'_delete').lower(), kwargs={'pk': self.pk})
	def get_absolute_details_url(self):
		return reverse((self.__class__.__name__+'_details').lower(), kwargs={'pk': self.pk})
	def get_absolute_create_url(self):
		return reverse((self.__class__.__name__+'_new').lower())
	def get_absolute_list_url(self):
		return reverse((self.__class__.__name__+'_list').lower())
	def get_uuid_url(self):
		return reverse('uuid_details', kwargs={'uuid':self.uuid})
	@classmethod
	def is_user_editable(cls):return False

	@classmethod
	def get_add_link(cls):
		return reverse((str(cls._meta).split('.')[1]+'_new').lower())

	def is_user_owned(self):
		if self.created_by == get_current_user() : return True
		return False


	def has_status(self): return False
	def get_absolute_url(self):
		return self.get_absolute_edit_url()

	class Meta:
		abstract = True

@modify_fields(name={'verbose_name': 'Library ID'})
class Library(auto_model):
# 	library_id = models.CharField(max_length=255,verbose_name="Library ID")

	reads_type	= models.CharField(max_length=255,verbose_name="Reads Type",null=True)
	flowcell_id	= models.CharField(max_length=255,verbose_name="Flowcell Id",null=True,blank=True)
	determined_reads = models.IntegerField(verbose_name="Determined Reads #",null=True,blank=True)
	average_phred	 = models.CharField(max_length=255,verbose_name="Average Phred",null=True,blank=True)
	qc_report_url	= models.URLField(verbose_name="QC URL",null=True,blank=True)
	ercc_r2	= models.FloatField(null=True,blank=True)
	ercc_mix = models.CharField(max_length=10,null=True,blank=True)
	ercc_dilution = models.FloatField(null=True,blank=True)
	reads_mapped_refseq_portion = models.FloatField(null=True,blank=True)
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
	def get_status(self):
# 		if ():
		return True
		return False
	def get_class_status(self):
		if self.get_status(): return "success"
		return "danger"
	def has_status(self): return True
	def has_etxra_list_fields(self): return True

	def get_extra_list_fields(self):
		row=""
		for fields in self.get_list_view_fields():
			row=row+("<td>{}</td>").format(fields)
		return mark_safe(row)

	def get_extra_list_fields_headers(self):
		header=""
		for fields in self.get_list_view_fields(True):
			header=header+("<th data-defaultsort='disabled'>{}</th>").format(fields)
		return mark_safe(header)

	def get_name(self):return self.name

	def get_list_view_fields(self,name=False):
		field_list=["reads_type","flowcell_id","determined_reads","average_phred","qc_report_url","ercc_r2","ercc_url"]
		f=[]
		for field in self._meta.fields:
			if field.name in field_list:
				if name:f.append(field.verbose_name)
				else :
					if "url" in field.name:
						f.append(("<a href='{}'>link</a>").format(getattr(self,field.name)))
					else :f.append(getattr(self,field.name))
		return f

class Project(auto_model):
	libraries = models.ManyToManyField(Library)

	def get_fields(self):
		f=super().get_fields()
		lib_list=self.get_lib_tag_table()
# 		lib_list=lib_list+"<ul>"
# 		for l in natsorted(self.libraries.all().values_list('library_alias','name','id')):
# 			lib_list+=("<li><a href='{}'>{} - {}</a></li>").format(Library.objects.get(pk=l[2]).get_absolute_details_url(),l[0],l[1])

		f.append(['libraries ',mark_safe(lib_list)])
		return f

	def get_lib_tag_table(self):
# 		for l in natsorted(self.libraries.all().values_list('library_alias','name','id')):
		table={}
		for t in Tag.objects.filter(project=self):
			tv=TagValues.objects.filter(tag=t)[0]
			table[tv.tag_number]={t.name:[]}
# 			print(tv.tag_number,t.name)
			tv_l=TagValues.objects.filter(tag_number=tv.tag_number).order_by().values_list('tag_value',flat=True).distinct()
			table[tv.tag_number][t.name]=tv_l

		ret=""
		tag_head="<td>#</td><td> Sample Name </td><td> Alias </td>"
		tag_head_value="<td></td><td></td><td></td>"
		html=""
		lib_line=""
		lib_list=""
		for k in table:
			for t in table[k]:
				tag_head+="<td colspan='{}'>{}</td>".format(len(table[k][t]),t)
				for tv in table[k][t]:tag_head_value+="<td>{}</td>".format(tv)
# 				ret+="<p>{} : {}</p>".format(t,str(table[k][t]))
		t_l=[]
		for k in table:
			for v in table[k]:
				for x in table[k][v]:t_l.append(x)
		cpt=1
		for l in natsorted(self.libraries.all().values_list('library_alias','name','id')):
			lib_list+=("<tr><td>{}</td><td><a href='{}'>{}</a></td><td><a href='{}'>{}</a></td>").format(cpt,Library.objects.get(pk=l[2]).get_absolute_details_url(),l[1],Library.objects.get(pk=l[2]).get_absolute_details_url(),l[0])
			tv=TagValues.objects.filter(library=Library.objects.get(pk=l[2])).values_list('tag_value',flat=True)
			flags=""
			cpt+=1
			for i in t_l:
				if i in tv:flags+="<td>X</td>"
				else: flags+="<td></td>"

			lib_list+=flags+"</tr>"

		tag_head=self.cmp_matrix()+"<table class='table table-bordered table-striped'><thead><tr>"+tag_head+"</tr><tr>"+tag_head_value+"</tr></thead><tbody>"+lib_list+"</tbody></table>"

		return tag_head

	def cmp_matrix(self):
		for t in Tag.objects.filter(project=self):
			v=TagValues.objects.filter(tag=t).values_list('tag_value',flat=True).distinct()
			if len(v)==2:
				horiz=TagValues.objects.filter(tag=t,tag_value=v[0]).values_list('library',flat=True)
				vert=TagValues.objects.filter(tag=t,tag_value=v[1]).values_list('library',flat=True)
				horiz=natsorted([x[:-1] for x in self.libraries.filter(replicate=1,pk__in=horiz).values_list('library_alias',flat=True)])
				vert=natsorted([x[:-1] for x in self.libraries.filter(replicate=1,pk__in=vert).values_list('library_alias',flat=True)])
				ret="</td><td>".join(horiz)
				bod=""
				for lib in vert:
					cnt=("<td>{}</td>").format(lib)
					for i in range(len(horiz)):
						cnt+=("<td>{}</td>").format('<input type="checkbox" value="'+lib+' '+horiz[i]+'">')
					bod+=("<tr>{}</tr>").format(cnt)

				main_table="<table id='cmp_table' class='table-bordered table-striped table'><thead><td><a href='#cmp_table' class='diag_check' start='0' id=''>Un/Check Diagonal</a><td/>"+ret[:-4]+"</td></thead><tbody>"+bod+"<tbody></table>"

				ret="</td><td>".join(horiz)
				bod=""
				cpt=0
				for lib in horiz:
					cnt=("<td>{}</td>").format(lib)
					for i in range(len(horiz)):
						if i>cpt:
							cnt+=("<td>{}</td>").format('<input type="checkbox" value="'+lib+' '+horiz[i]+'">')
						else:cnt+=("<td></td>")
					bod+=("<tr>{}</tr>").format(cnt)
					cpt+=1
				sec_table="<table id='2nd_table' class='table-bordered table-striped table'><thead><td><a href='#cmp_table' class='diag_check' id='' start='1' >Un/Check Diagonal</a><td/>"+ret[:-4]+"</td></thead><tbody>"+bod+"<tbody></table>"

				ret="</td><td>".join(vert)
				bod=""
				cpt=0
				for lib in vert:
					cnt=("<td>{}</td>").format(lib)
					for i in range(len(vert)):
						if i>cpt:
							cnt+=("<td>{}</td>").format('<input type="checkbox" value="'+lib+' '+vert[i]+'">')
						else:cnt+=("<td></td>")
					bod+=("<tr>{}</tr>").format(cnt)
					cpt+=1
				thi_table="<table id='3nd_table' class='table-bordered table-striped table'><thead><td><a href='#cmp_table' class='diag_check' id='' start='1'>Un/Check Diagonal</a><td/>"+ret[:-4]+"</td></thead><tbody>"+bod+"<tbody></table><a id='sub_cmp' href='#cmp_table'>Submit</a>"


				return(main_table+sec_table+thi_table)
		return ""



class Tag(auto_model):
	libraries_group = models.ManyToManyField(Library, through='TagValues',through_fields=('tag','library'))
	project = models.ForeignKey(Project,null=True,blank=True)

class TagValues(auto_model):
	tag = models.ForeignKey(Tag)
	library = models.ForeignKey(Library)
	tag_value = models.CharField(max_length=255)
	tag_number = models.IntegerField()


class Attachment(auto_model):
	file = models.FileField(upload_to='files/%Y/%m/%d')
	@classmethod
	def is_user_editable(cls):return True

class read_group_tracking(auto_model):
	project = models.ForeignKey(Project)
	tracking_id = models.CharField(max_length=100)
	condition = models.CharField(max_length=100)
	replicate = models.IntegerField(default=0)
	FPKM = models.FloatField(default=0)
	def __init__(self, *args, **kwargs):
		models.Model.__init__(self, *args, **kwargs)
		if self.id != None:
			self.name = u"{}_{}".format(self.condition,self.tracking_id)


class gene_exp(auto_model):
	test_id= models.CharField(max_length=100)
	sample_1= models.CharField(max_length=100)
	sample_2= models.CharField(max_length=100)
	p_value=models.FloatField(default=0)
	q_value=models.FloatField(default=0)
	FC=models.FloatField(default=0)
	SEM_1=models.FloatField(default=0)
	SEM_2	=models.FloatField(default=0)
	fpkm_1=models.FloatField(default=0)
	fpkm_2=models.FloatField(default=0)
	inf = models.BooleanField(editable=False,default=False)

class flag(auto_model):
	flag = models.BooleanField(editable=False,default=False)
	operation = models.CharField(max_length=100)
