from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cryptid, Evidence, Photo
from .forms import SightingForm
import uuid
import boto3

S3_BASE_URL = "https://s3.us-west-1.amazonaws.com/"
BUCKET = 'cryptid-collector'


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


def assoc_evidence(request, cryptid_id, evidence_id):
    print(cryptid_id)
    Cryptid.objects.get(id=cryptid_id).evidence.add(evidence_id)
    return redirect('cryptids_detail', cryptid_id=cryptid_id)


def add_photo(request, cryptid_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        # uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
        # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
        key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cryptid_id or cryptid (if you have a cryptid object)
            photo = Photo(url=url, cryptid_id=cryptid_id)
            # Remove old photo if it exists
            cryptid_photo = Photo.objects.filter(cryptid_id=cryptid_id)
            if cryptid_photo.first():
                cryptid_photo.first().delete()
            photo.save()
        except Exception as err:
            print('An error occurred uploading file to S3: %s' % err)
    return redirect('cryptids_detail', cryptid_id=cryptid_id)