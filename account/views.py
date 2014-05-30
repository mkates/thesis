from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

def signin(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect('/visual')
	else:
		return render_to_response('login.html',{},context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
	
def loginrequest(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/visual')
	else:
		email = request.POST.get('email','')
		password = request.POST.get('password','')
		user = authenticate(username=email,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/visual')
		else:
			return render_to_response('login.html',{'error':'Your email and/or password was incorrect'},context_instance=RequestContext(request))
