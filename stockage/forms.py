# gestion_stock/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import LigneVente, Produit, Client, Fournisseur, Vente, Achat, Compte, Paiement

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class LigneVenteForm(forms.ModelForm):
    class Meta:
        model = LigneVente
        fields = ['produit', 'quantite']
        # Ajoutez d'autres champs du formulaire article de facture au besoin

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['client']
        # Ajoutez d'autres champs du formulaire facture au besoin

    produits = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = '__all__'

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User

class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = '__all__'

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'
