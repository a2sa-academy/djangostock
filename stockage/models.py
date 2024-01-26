# gestion_stock/models.py

from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(default=0)
    def update_quantite(self, quantite_vendue):
        self.quantite_stock -= quantite_vendue
        self.save()
    def totalprod(self):
        return self.quantite_stock 
    def valeurstock(self):
        return self.quantite_stock * self.prix_unitaire
    def __str__(self):
        return self.nom

class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit, through='LigneVente')
    date_vente = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Vente de  {self.produits} à {self.client} le {self.date_vente}"
class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    def total(self):
        return self.quantite * self.produit.prix_unitaire
    
    def total_amount(self):
        # Calculer le montant total de la facture en additionnant les montants des articles liés
        return sum(lignevente.total for lignevente in self.lignevente_set.all())

    def __str__(self):
        return f"{self.quantite} x {self.produit.prix_unitaire} - ${self.total()}"

class Compte(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Compte de {self.client} - Solde: {self.solde}"

class Paiement(models.Model):
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Paiement de {self.montant} sur le compte {self.compte} le {self.date_paiement}"

# Modification du modèle Achat pour inclure les paiements
class Achat(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_achat = models.DateField(auto_now_add=True)
    paiements = models.ManyToManyField(Paiement, blank=True)

    def montant_total(self):
        return self.produit.prix_unitaire * self.quantite

    def montant_paye(self):
        return sum(paiement.montant for paiement in self.paiements.all())

    def solde_restant(self):
        return self.montant_total() - self.montant_paye()
