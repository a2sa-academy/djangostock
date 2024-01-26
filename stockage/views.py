# views.py
import datetime
from decimal import Decimal
import html
from multiprocessing import AuthenticationError
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from num2words import num2words  # Import the num2words library
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Compte, LigneVente, Paiement, Produit, Client, Fournisseur, Vente, Achat
from .forms import ProduitForm, ClientForm, FournisseurForm, AchatForm, VenteForm,LigneVenteForm

class ProduitListView(View):
    template_name = 'produit_list.html'
    def get(self, request):
        produits = Produit.objects.all()
        return render(request, self.template_name, {'produits': produits})
def generate_stock_report_pdf(request):
    produits = Produit.objects.all()
    template_path = 'stock_report_template.html'
    context = {'produits': produits}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="stock_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', content_type='text/plain')

    return response      
class ProduitDetailView(View):
    template_name = 'produit_detail.html'
   
    def get(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        return render(request, self.template_name, {'produit': produit})

class ProduitCreateView(View):
    template_name = 'produit_form.html'
   
    def get(self, request):
        form = ProduitForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
        return render(request, self.template_name, {'form': form})

class ProduitUpdateView(View):
    template_name = 'produit_form.html'

    def get(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        form = ProduitForm(instance=produit)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
        return render(request, self.template_name, {'form': form})

class ProduitDeleteView(View):
    template_name = 'produit_confirm_delete.html'

    def get(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        return render(request, self.template_name, {'produit': produit})

    def post(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        produit.delete()
        return redirect('produit_list')

# Créez des vues similaires pour les autres modèles (Client, Fournisseur, Vente, Achat)
# views.py (suite)
# views.py (suite)

class ClientListView(View):
    template_name = 'client_list.html'
   
    def get(self, request):
        clients = Client.objects.all()
        return render(request, self.template_name, {'clients': clients})

class ClientDetailView(View):
    template_name = 'client_detail.html'

    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        return render(request, self.template_name, {'client': client})

class ClientCreateView(View):
    template_name = 'client_form.html'
   
    def get(self, request):
        form = ClientForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, self.template_name, {'form': form})

# Créez des vues similaires pour Fournisseur
class FournisseurListView(View):
    template_name = 'fournisseur_list.html'

    def get(self, request):
        fournisseurs = Fournisseur.objects.all()
        return render(request, self.template_name, {'fournisseurs': fournisseurs})

class FournisseurDetailView(View):
    template_name = 'fournisseur_detail.html'

    def get(self, request, pk):
        fournisseur = get_object_or_404(Fournisseur, pk=pk)
        return render(request, self.template_name, {'fournisseur': fournisseur})

class FournisseurCreateView(View):
    template_name = 'fournisseur_form.html'

    def get(self, request):
        form =FournisseurForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')
        return render(request, self.template_name, {'form': form})

# Créez des vues similaires pour Fournisseur, Vente et Achat en suivant le même modèle.

# , Vente et Achat en suivant le même modèle.

class VenteListView(View):
    template_name = 'vente_list.html'

    def get(self, request):
        ventes = Vente.objects.all()
        return render(request, self.template_name, {'ventes': ventes})

class VenteDetailView(View):
    template_name = 'vente_detail.html'

    def get(self, request, pk):
        vente = get_object_or_404(Vente, pk=pk)
        return render(request, self.template_name, {'vente': vente})

class VenteCreateView(View):
    template_name = 'vente_form.html'

    def get(self, request):
        form = VenteForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vente_list')
        return render(request, self.template_name, {'form': form})

# Créez des vues similaires pour le modèle Achat en suivant le même modèle.
# Ajout d'une vue pour suivre les comptes clients et fournisseurs
class CompteListView(View):
    template_name = 'compte_list.html'

    def get(self, request):
        comptes = Compte.objects.all()
        return render(request, self.template_name, {'comptes': comptes})

# Modification de la vue pour les détails d'un achat
class AchatDetailView(View):
    template_name = 'achat_detail.html'

    def get(self, request, pk):
        achat = get_object_or_404(Achat, pk=pk)
        paiements = achat.paiements.all()
        return render(request, self.template_name, {'achat': achat, 'paiements': paiements})

# Modification de la vue pour créer un achat avec la possibilité d'ajouter des paiements
class AchatCreateView(View):
    template_name = 'achat_form.html'

    def get(self, request):
        form = AchatForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save()
            
            # Ajout des paiements associés à l'achat
            montant_total = achat.montant_total()
            montant_paye = 0
            
            while montant_paye < montant_total:
                montant_paiement = Decimal(input(f"Entrez le montant du paiement (reste à payer: {montant_total - montant_paye}): "))
                
                # Vérification pour éviter les paiements excessifs
                if montant_paiement > montant_total - montant_paye:
                    print("Le montant du paiement est supérieur au montant restant. Veuillez réessayer.")
                else:
                    Paiement.objects.create(compte=achat.fournisseur.compte, montant=montant_paiement)
                    montant_paye += montant_paiement
            
            return redirect('achat_list')
        
        return render(request, self.template_name, {'form': form})

# Modification de la vue pour créer une vente avec la possibilité d'ajouter des paiements
class VenteCreateView(View):
    template_name = 'vente_form.html'

    def get(self, request):
        form = VenteForm()
        return render(request, self.template_name, {'form': form, 'produits': Produit.objects.all()})

    def post(self, request):
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()
            
            # Ajout des paiements associés à la vente
            montant_total = sum(ligne.quantite * ligne.produit.prix_unitaire for ligne in vente.lignevente_set.all())
            montant_paye = 0
            
            while montant_paye < montant_total:
                montant_paiement = Decimal(input(f"Entrez le montant du paiement (reste à payer: {montant_total - montant_paye}): "))
                
                # Vérification pour éviter les paiements excessifs
                if montant_paiement > montant_total - montant_paye:
                    print("Le montant du paiement est supérieur au montant restant. Veuillez réessayer.")
                else:
                    Paiement.objects.create(compte=vente.client.compte, montant=montant_paiement)
                    montant_paye += montant_paiement
            
            return redirect('vente_list')
        
        return render(request, self.template_name, {'form': form, 'produits': Produit.objects.all()})
# views.py (suite)
class AchatListView(View):
    template_name = 'achat_list.html'

    def get(self, request):
        achats = Achat.objects.all()
        return render(request, self.template_name, {'achats': achats})
    

##nouvelle facture
@login_required
def nouvelle_vente(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()

            # Ajouter les articles de la vente
            produits = request.POST.getlist('produits')
            quantite = request.POST.getlist('quantite')

            for produit_id, quantite_vendue in zip(produits, quantite):
                produit = Produit.objects.get(pk=produit_id)
                LigneVente.objects.create(
                    vente=vente,
                    produit=produit,
                    quantite=quantite_vendue
                )

                # Mise à jour de la quantité de produit
                produit.update_quantite(int(quantite_vendue))

            return redirect('vente_list')
    else:
        form = VenteForm()

    return render(request, 'nouvelle_vente.html', {'form': form, 'produits': Produit.objects.all()})

def vente_detail(request, pk):
    vente = Vente.objects.get(pk=pk)
    ligneventes =LigneVente.objects.filter(vente=vente)
    return render(request, 'vente_detail.html', {'vente': vente, 'ligneventes': ligneventes})
#Génération d'une facture pdf
def generate_vente_pdf(request,pk):
    # Récupérer l'objet vente à partir de la base de données
    vente = get_object_or_404(Vente, pk=pk)
    # Charger le template HTML pour la facture
    ligneventes= LigneVente.objects.filter(vente=vente)
     # Calculate the total for each lignevente
    for lignevente in ligneventes:
        lignevente.total = lignevente.quantite * lignevente.produit.prix_unitaire
    #pour la valeur du stock
    total_amount = sum(lignevente.total for lignevente in ligneventes)

    # Convert the total amount to words in French
    total_amount_in_words = num2words(total_amount, lang='fr').capitalize()
    template_path = 'pdf_template.html'
    context = {
        'vente': vente,
        'total_amount':total_amount,
        'total_amount_in_words':total_amount_in_words
               
               }
    template = get_template(template_path)
    html = template.render(context)

    # Créer un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={vente.date_vente}_vente.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)

    # Vérifier si la création du PDF s'est bien déroulée
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', content_type='text/plain')

    return response
#view pour authentification 
class InscriptionView(View):
    template_name = 'inscription.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class ConnexionView(View):
    template_name = 'connexion.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})
class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    
class DashboardView(View):
    def get(self, request):
        ligneventes = LigneVente.objects.all()
        produits = Produit.objects.all()
        total_ventes = sum(lingevente.total() for lingevente in ligneventes)
        total_amount = sum(lignevente.produit.prix_unitaire * lignevente.quantite for lignevente in ligneventes)
        # Convert the total amount to words in French
        valeur_totale_stock =sum(produi.totalprod() for produi in produits)
        valeurstock=sum(produi.valeurstock() for produi in produits)
        context = {
            'valeur_totale_stock': valeur_totale_stock,
            'total_ventes': total_ventes,
            'valeurstock':valeurstock,
        }
        return render(request, 'dashboard.html', context)
  