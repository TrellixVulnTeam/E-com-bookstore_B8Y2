from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cards
from cards.forms import CardsRegisterForm
# Create your views here.


@login_required
def cardregister(request):
    Cards.objects.all()
    #if request.method == 'POST':
    form = CardsRegisterForm(request.POST or None)
    if form.is_valid():
        fs = form.save(commit=False)
        fs.user = request.user
        fs.save()
        messages.success(
            request, f'Your card has been added! ')
        return redirect('cards-home')
    else:
        form = CardsRegisterForm()
    return render(request, 'cards/cards_form.html', {'form': form})


