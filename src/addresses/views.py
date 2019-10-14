from django.shortcuts import render, redirect
from django.contrib import messages
from addresses.forms import AddressRegisterForm, AddressUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Address
from django.forms.models import model_to_dict

# Create your views here.



def addressregister(request):
    data = Address.objects.all()
    #if request.method == 'POST':
    form = AddressRegisterForm(request.POST or None )
    if form.is_valid():
        fs=form.save(commit = False)
        fs.user = request.user
        fs.save()
        messages.success(
            request, f'Your address has been created! ')
        return redirect('address-home')
    else:
        form = AddressRegisterForm()
    context = {
        
        'form': form,
        'data': data,
    }
    return render(request, 'addresses/address_form.html', context)


