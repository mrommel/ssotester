# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import jwt
from datetime import datetime

# Create your models here.

"""
	class that keeps the keycloak user object
"""
class User(models.Model):

	name = models.CharField(max_length=50)
	access_token = models.CharField(max_length=2048)
	refresh_token = models.CharField(max_length=2048)
	
	def access_token_expiry(self):
		dict = jwt.decode(self.access_token, verify=False)
		return datetime.fromtimestamp(dict['exp'])
		
	def access_token_valid(self):
		return self.access_token_expiry() > datetime.now()
		
	def device(self):
		devices = Device.objects.filter(user=self)
		
		if devices is None or len(devices) == 0:
			return None
			
		return devices[0]
	
	def __unicode__(self): 
		return self.name
	
	class Meta:
		ordering = ('name',)
		
"""
	class that keeps the IOT device
"""
class Device(models.Model):
	
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	category = models.CharField(max_length=50)
	resourceId = models.CharField(max_length=50)
	deviceId = models.CharField(max_length=50)
	
	def __unicode__(self): 
		return self.name
	
	class Meta:
		ordering = ('name',)