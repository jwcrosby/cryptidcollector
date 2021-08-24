from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cryptid, Evidence, Photo
from .forms import SightingForm
import uuid
import boto3


S3_BASE_URL = "https://s3.us-west-1.amazonaws.com/"
BUCKET = 'cryptid-collector'


class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


@login_required
def cryptids_index(request):
    cryptids = Cryptid.objects.filter(user=request.user)
    return render(request, 'cryptids/index.html', {'cryptids': cryptids})


@login_required
def cryptids_detail(request, cryptid_id):
    cryptid = Cryptid.objects.get(id=cryptid_id)
    evidence_cryptid_doesnt_have = Evidence.objects.exclude(id__in = cryptid.evidence.all().values_list('id'))
    sighting_form = SightingForm()
    return render(request, 'cryptids/detail.html', {
        'cryptid': cryptid,
        'sighting_form': sighting_form,
        'evidence': evidence_cryptid_doesnt_have
    })


class CryptidCreate(LoginRequiredMixin, CreateView):
    model = Cryptid
    fields = ['name', 'other', 'description', 'location']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class CryptidUpdate(LoginRequiredMixin, UpdateView):
    model = Cryptid
    fields = ['other', 'description', 'location']


class CryptidDelete(LoginRequiredMixin, DeleteView):
    model = Cryptid
    success_url = '/cryptids/'


@login_required
def add_sighting(request, cryptid_id):
    form = SightingForm(request.POST)
    if form.is_valid():
        new_sighting = form.save(commit=False)
        new_sighting.cryptid_id = cryptid_id
        new_sighting.save()
    return redirect('cryptids_detail', cryptid_id=cryptid_id)


class EvidenceCreate(LoginRequiredMixin, CreateView):
    model = Evidence
    fields = '__all__'


class EvidenceList(LoginRequiredMixin, ListView):
    model = Evidence


class EvidenceDetail(LoginRequiredMixin, DetailView):
    model = Evidence


class EvidenceUpdate(LoginRequiredMixin, UpdateView):
    model = Evidence
    fields = ['evidence', 'color']


class EvidenceDelete(LoginRequiredMixin, DeleteView):
    model = Evidence
    success_url = '/evidence/'


@login_required
def assoc_evidence(request, cryptid_id, evidence_id):
    print(cryptid_id)
    Cryptid.objects.get(id=cryptid_id).evidence.add(evidence_id)
    return redirect('cryptids_detail', cryptid_id=cryptid_id)


@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cryptid_index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)