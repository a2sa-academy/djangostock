from django.urls import path
from django.contrib.auth import login
from .views import ClientCreateView, ClientDetailView, ClientListView, ConnexionView, DashboardView, DeconnexionView, InscriptionView, ProduitDeleteView, ProduitListView, ProduitCreateView, ProduitUpdateView, ProduitDetailView,FournisseurCreateView, FournisseurListView,FournisseurDetailView,VenteCreateView,VenteDetailView,VenteListView,AchatCreateView,AchatDetailView,AchatListView, generate_stock_report_pdf, generate_vente_pdf, nouvelle_vente

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', DeconnexionView.as_view(), name='deconnexion'),
    #
    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produits/nouveau/', ProduitCreateView.as_view(), name='produit_create'),
    path('produits/<int:pk>/', ProduitDetailView.as_view(), name='produit_detail'),
    path('produits/modifier/<int:pk>/', ProduitUpdateView.as_view(), name='produit_update'),
    path('produits/supprimer/<int:pk>/', ProduitDeleteView.as_view(), name='produit_delete'),

    # Ajoutez Fournisseur
    path('fournisseurs/', FournisseurListView.as_view(), name='fournisseur_list'),
    path('fournisseurs/nouveau/', FournisseurCreateView.as_view(), name='fournisseur_create'),
    path('fournisseurs/<int:pk>/', FournisseurDetailView.as_view(), name='fournisseur_detail'),
    #clients
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/nouveau/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    #pour ventes
    path('nouvelle/', nouvelle_vente, name='nouvelle_vente'),
    path('<int:pk>/', VenteDetailView.as_view(), name='vente_detail'),
    path('ventes/', VenteListView.as_view(), name='vente_list'),
    #pdf
    path('generate_vente_pdf/<int:pk>/', generate_vente_pdf, name='generate_vente_pdf'),
    path('stock-report-pdf/', generate_stock_report_pdf, name='stock_report_pdf'),

]
