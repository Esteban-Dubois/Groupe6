#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''   
    SELECT commande.id_commande, commande.etat_id, utilisateur.login, commande.date_achat, SUM(ligne_commande.quantite) AS nbr_articles, SUM(ligne_commande.prix*ligne_commande.quantite) AS prix_total, etat.libelle_etat AS libelle FROM commande
    JOIN utilisateur ON utilisateur.id_utilisateur = commande.utilisateur_id_commande
    JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
    JOIN etat ON etat.id_etat = commande.etat_id
    GROUP BY commande.id_commande, utilisateur.login, commande.date_achat, etat.libelle_etat
    ORDER BY commande.date_achat DESC;
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    #commandes=[]

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''
        SELECT fusee.nom_fusee AS nom, ligne_commande.quantite, ligne_commande.prix,
        ligne_commande.quantite * ligne_commande.prix AS prix_ligne
        FROM ligne_commande
        JOIN fusee ON fusee.id_fusee = ligne_commande.fusee_id_commande
        WHERE ligne_commande.commande_id = %s;
        '''
        
        mycursor.execute(sql,(id_commande,))
        articles_commande = mycursor.fetchall()
        commande_adresses = []
        
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
        
        
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande
            SET etat_id = 2 
            WHERE id_commande = %s;
            '''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')
