from django.shortcuts import render
from django.http import HttpResponse

def main(request):
	return HttpResponse('<h1> Main </h1>')

def contactus(request):
	return render(request, 'main/contactus/contactus.html')

def aboutus(request):
	return render(request, 'main/aboutus/aboutus.html')

	

