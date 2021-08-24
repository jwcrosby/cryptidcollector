from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cryptid, Evidence
from .forms import SightingForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def cryptids_index(request):
    cryptids = Cryptid.objects.all()
    return render(request, 'cryptids/index.html', {'cryptids': cryptids})


def cryptids_detail(request, cryptid_id):
    cryptid = Cryptid.objects.get(id=cryptid_id)
    evidence_cryptid_doesnt_have = Evidence.objects.exclude(id__in = cryptid.evidence.all().values_list('id'))
    sighting_form = SightingForm()
    return render(request, 'cryptids/detail.html', {
        'cryptid': cryptid,
        'sighting_form': sighting_form,
        'evidence': evidence_cryptid_doesnt_have
    })


class CryptidCreate(CreateView):
    model = Cryptid
    fields = ['name', 'other', 'description', 'location']


class CryptidUpdate(UpdateView):
    model = Cryptid
    fields = ['other', 'description', 'location']


class CryptidDelete(DeleteView):
    model = Cryptid
    success_url = '/cryptids/'

def add_sighting(request, cryptid_id):
    form = SightingForm(request.POST)
    if form.is_valid():
        new_sighting = form.save(commit=False)
        new_sighting.cryptid_id = cryptid_id
        new_sighting.save()
    return redirect('cryptids_detail', cryptid_id=cryptid_id)

class EvidenceCreate(CreateView):
    model = Evidence
    fields = '__all__'

class EvidenceList(ListView):
    model = Evidence

class EvidenceDetail(DetailView):
    model = Evidence

class EvidenceUpdate(UpdateView):
    model = Evidence
    fields = ['evidence', 'color']

class EvidenceDelete(DeleteView):
    model = Evidence
    success_url = '/evidence/'