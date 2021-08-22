from django.shortcuts import render
from django.http import HttpResponse

def home(request):
  return HttpResponse('<h1>Hello Creep</h1>')

def about(request):
  return HttpResponse('<h1>ABOUT THIS THING</h1>')