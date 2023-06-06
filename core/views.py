from django.shortcuts import render
from core.forms import ContactForm 
from core.models import Contact
import csv
from django.http import HttpResponse, JsonResponse


# Create your views here.

def download_contact_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact_list.csv"'

    contacts = Contact.objects.all()  

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number'])  

    for contact in contacts:
        writer.writerow([contact.name, contact.phone_number])

    return response



def index(request) :
    context = {'form': ContactForm(), 'contacts': Contact.objects.all() }

    return render(request, 'index.html', context) 

def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            contact = form.save()
            context = {'contact': contact}
            return render(request, 'partials/contact.html', context)

    return render(request, 'partials/form.html', {'form': ContactForm()})



def delete_contact(request, pk):
    if request.method == "POST":
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        context = {'form': ContactForm(), 'contacts': Contact.objects.all() }
        return render(request, 'partials/contact.html', context)

    
