from django.shortcuts import render
from .models import Cryptid

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cryptids_index(request):
  cryptids = Cryptid.objects.all()
  return render(request, 'cryptids/index.html', { 'cryptids': cryptids })

def cryptid_detail(request, cryptid_id):
  cryptid = Cryptid.objects.get(id=cryptid_id)
  return render(request, 'cryptids/detail.html', { 'cryptid': cryptid })