# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import requests
import jwt

from .models import *

# Create your views here.
def index(request):
	user_list = User.objects.all()
	return render(request, 'tester/index.html', {
		'user_list': user_list
	})
	
def login(request):
	try:
		tan = request.POST['tan_field']
	except (KeyError):
		# Redisplay the question voting form.
		return render(request, 'tester/index.html', {
			'error_message': "You didn't provide a TAN.",
		})
	else:
		# do something here
		url = 'https://test-auth.365farmnet.com/auth/realms/Farmnet/protocol/openid-connect/token'
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		data = ('grant_type=password&client_id=iot-app&username=iot-tan&password=%s&scope=offline_access' % tan)
		response = requests.post(url, data=data, headers=headers)
		response.encoding = 'utf-8'
		
		if(response.ok):		
			dict = response.json()
			
			user = User()
			user.name = "user"
			user.access_token = dict["access_token"]
			user.refresh_token = dict["refresh_token"]
			user.save()
			#print dict
			#print "access_token: %s" % dict["access_token"]
			#print "refresh_token: %s" % dict["refresh_token"]
			#jwt.decode(response.content, 'access_token')
		
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('tester:index'))
		else:
			# Redisplay the question voting form.
			return render(request, 'tester/index.html', {
				'error_message': "Server responded with: %d - %s" % (response.status_code, response.content)
			})
			
def refresh(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	try:
		refresh_token = request.POST['refresh_token']
	except (KeyError.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'tester/index.html', {
			'error_message': "You didn't provide a refresh_token.",
		})
	else:
		# do something here
		url = 'https://test-auth.365farmnet.com/auth/realms/Farmnet/protocol/openid-connect/token'
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		data = ('grant_type=refresh_token&client_id=iot-app&refresh_token=%s' % refresh_token)
		response = requests.post(url, data=data, headers=headers)
		response.encoding = 'utf-8'
		
		if(response.ok):		
			dict = response.json()
			
			user.access_token = dict["access_token"]
			user.refresh_token = dict["refresh_token"]
			user.save()
			print 'updated'
		
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('tester:index'))
		else:
			# Redisplay the question voting form.
			return render(request, 'tester/index.html', {
				'error_message': "Server responded with: %d - %s" % (response.status_code, response.content)
			})
			
def status(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	try:
		refresh_token = request.POST['refresh_token']
	except (KeyError.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'tester/index.html', {
			'error_message': "You didn't provide a refresh_token.",
		})
	else:
		# do something here
		url = 'https://testotc-connect.365farmnet.com/farmnet/v1/iot/account/status/device'
		headers = { "Content-Type": "application/json", "Authorization": "Bearer %s" % user.access_token }
		response = requests.get(url, headers=headers)
		response.encoding = 'utf-8'
		
		if(response.ok):		
			dict = response.json()
			
			user.access_token = dict["access_token"]
			user.refresh_token = dict["refresh_token"]
			user.save()
			print 'updated'
		
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('tester:index'))
		else:
			# Redisplay the question voting form.
			return render(request, 'tester/index.html', {
				'error_message': "Server responded with: %d - %s" % (response.status_code, response.content)
			})
	
	