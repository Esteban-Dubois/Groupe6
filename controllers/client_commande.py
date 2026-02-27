#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id_panier = %s
    '''
    mycursor.execute(sql,(id_client, ))
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(ligne_panier.quantite * fusee.prix_fusee) AS total
                  FROM fusee
                  JOIN ligne_panier ON fusee.id_fusee = ligne_panier.fusee_id_panier
                  WHERE ligne_panier.utilisateur_id_panier = %s
        '''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()['total']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id_panier = %s '''
    mycursor.execute(sql,(id_client, ))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
         return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = ''' creation de la commande '''

    sql = '''SELECT last_insert_id() as last_insert_id'''
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' suppression d'une ligne de panier '''
        sql = "  ajout d'une ligne de commande'"

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  
    SELECT utilisateur.login, commande.id_commande, commande.etat_id,  commande.date_achat, SUM(ligne_commande.quantite) AS nbr_articles, SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total, etat.libelle_etat AS libelle FROM commande
    JOIN utilisateur ON utilisateur.id_utilisateur = commande.utilisateur_id_commande
    JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
    JOIN etat ON etat.id_etat = commande.etat_id
    WHERE utilisateur.id_utilisateur = %s
    GROUP BY commande.id_commande, utilisateur.login, commande.date_achat, etat.libelle_etat
    ORDER BY etat.libelle_etat, commande.date_achat DESC;
    '''
    mycursor.execute(sql,(id_client,))
    commandes = mycursor.fetchall()

    #commandes = []

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' 
        SELECT fusee.nom_fusee AS nom, ligne_commande.quantite, ligne_commande.prix,
        ligne_commande.quantite * ligne_commande.prix AS prix_ligne
        FROM ligne_commande
        JOIN fusee ON fusee.id_fusee = ligne_commande.fusee_id_commande
        JOIN commande ON commande.id_commande = ligne_commande.commande_id
        WHERE ligne_commande.commande_id = %s AND commande.utilisateur_id_commande = %s;
        '''
        
        mycursor.execute(sql,(id_commande,id_client))
        articles_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' 
        SELECT 
        adresse_facturer.nom_adresse AS nom_facturation,
        adresse_facturer.rue AS rue_facturation,
        adresse_facturer.code_postal AS code_postal_facturation,
        adresse_facturer.ville AS ville_facturation,
        adresse_livrer.nom_adresse AS nom_livraison,
        adresse_livrer.rue AS rue_livraison,
        adresse_livrer.code_postal AS code_postal_livraison,
        adresse_livrer.ville AS ville_livraison
        FROM commande
        JOIN adresse AS adresse_facturer ON adresse_facturer.id_adresse = commande.adresse_id_facturer
        JOIN adresse AS adresse_livrer ON adresse_livrer.id_adresse = commande.adresse_id_livrer
        WHERE commande.id_commande = %s;
        '''
        
        mycursor.execute(sql,(id_commande,))
        commande_adresses = mycursor.fetchone()

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

