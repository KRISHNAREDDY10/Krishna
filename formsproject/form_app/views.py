from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

# Create your views here.
def home_view(request):
    return render(request, 'form_app/home.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact-success')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'form_app/contact.html', context)

def contact_success_view(request):
    return render(request, 'form_app/contact_success.html')

def contact_list_view(request):
    contacts = Contact.objects.all()  # Fetch all contacts from the database
    context = {'contacts': contacts}
    return render(request, 'form_app/contact_list.html', context)
