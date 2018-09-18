# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import requests
import jwt

# Create your views here.
def index(request):
	return render(request, 'tester/index.html')
	
#@csrf_exempt
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
		
			print dict
			print "access_token: %s" % dict["access_token"]
			print "refresh_token: %s" % dict["refresh_token"]
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