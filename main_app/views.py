from django.shortcuts import render
from django.http import HttpResponse

# Add the Cat class & list and view function below the imports
class Cryptid:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, other, description, location):
    self.name = name
    self.other = other
    self.description = description
    self.location = location

cryptids = [
  Cryptid('Lolo', 'tabby', 'Kinda rude.', 'newyork'),
  Cryptid('Sachi', 'tortoiseshell', 'Looks like a turtle.', 'themoon'),
  Cryptid('Fancy', 'bombay', 'Happy fluff ball.', 'paris'),
  Cryptid('Bonk', 'selkirk rex', 'Meows loudly.', 'mars')
]

def home(request):
  return HttpResponse('<h1>Hello Creep</h1>')

def about(request):
  return render(request, 'about.html')

def cryptids_index(request):
  return render(request, 'cryptids/index.html', { 'cryptids': cryptids })