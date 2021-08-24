from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Cryptid

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cryptids_index(request):
  cryptids = Cryptid.objects.all()
  return render(request, 'cryptids/index.html', { 'cryptids': cryptids })

def cryptids_detail(request, cryptid_id):
  cryptid = Cryptid.objects.get(id=cryptid_id)
  return render(request, 'cryptids/detail.html', { 'cryptid': cryptid })

class CryptidCreate(CreateView):
  model = Cryptid
  fields = '__all__'
  