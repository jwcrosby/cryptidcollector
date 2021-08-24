from django.shortcuts import render

# Add the Cat class & list and view function below the imports
class Cryptid:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, other, description, location):
    self.name = name
    self.other = other
    self.description = description
    self.location = location

cryptids = [
  Cryptid('Bigfoot', 'tabby', 'Kinda rude.', 'newyork'),
  Cryptid('Loch Ness', 'tortoiseshell', 'Looks like a turtle.', 'themoon'),
  Cryptid('Chupacabra', 'bombay', 'Happy fluff ball.', 'paris'),
  Cryptid('Liz', 'selkirk rex', 'Meows loudly.', 'mars')
]

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cryptids_index(request):
  return render(request, 'cryptids/index.html', { 'cryptids': cryptids })