from django import forms
from .models import Cards

class CardsRegisterForm(forms.ModelForm):
    #class meta renders the the form as exactly is displayed in admin django web page

    class Meta:
        model = Cards
        fields = ['card_type', 'name_on_card', 'card_number','exp_month', 'exp_year', 'ccv_code']
