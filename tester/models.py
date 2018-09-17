# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=50)
	access_token = models.CharField(max_length=2048)
	refresh_token = models.CharField(max_length=2048)
	
	def __unicode__(self): 
		return self.name
	
	class Meta:
		ordering = ('name',)