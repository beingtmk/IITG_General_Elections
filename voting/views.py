from django.shortcuts import render, HttpResponse

def siteindex(request):
	return HttpResponse("site index!")