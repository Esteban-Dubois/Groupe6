#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # 1. Récupération des filtres depuis la session
    word = session.get('filter_word', '')
    p_min = session.get('filter_prix_min', '')
    p_max = session.get('filter_prix_max', '')
    types = session.get('filter_types', [])

    # 2. SQL des articles (Catalogue)
    sql_articles = '''   
        SELECT id_fusee AS id_article,
               prix_fusee AS prix, 
               stock_fusee AS stock,
               nom_fusee AS nom,
               image_fusee AS image, 
               categorie.libelle_categorie AS libelle
        FROM fusee
        JOIN categorie ON fusee.categorie_id = categorie.id_categorie
        WHERE 1=1 
    '''
    params_articles = []

    if word:
        sql_articles += " AND nom_fusee LIKE %s"
        params_articles.append(f"%{word}%")
    if p_min:
        sql_articles += " AND prix_fusee >= %s"
        params_articles.append(p_min)
    if p_max:
        sql_articles += " AND prix_fusee <= %s"
        params_articles.append(p_max)
    if types:
        placeholders = ', '.join(['%s'] * len(types))
        sql_articles += f" AND fusee.categorie_id IN ({placeholders})"
        params_articles.extend(types)

    mycursor.execute(sql_articles, tuple(params_articles))
    articles = mycursor.fetchall()
    
    # 3. SQL des types UNIQUE (SANS DOUBLONS)
    sql_types_filtre = '''
        SELECT DISTINCT id_categorie AS id_type_article, 
                        libelle_categorie AS libelle 
        FROM categorie
        ORDER BY libelle ASC
    '''
    mycursor.execute(sql_types_filtre)
    types_article = mycursor.fetchall() 

    # 4. SQL du panier
    sql_panier = '''
        SELECT f.nom_fusee AS nom, 
               lp.quantite AS quantite, 
               f.prix_fusee AS prix, 
               f.id_fusee AS id_article,
               f.stock_fusee AS stock
        FROM ligne_panier lp
        JOIN fusee f ON lp.fusee_id_panier = f.id_fusee
        WHERE lp.utilisateur_id_panier = %s
    '''
    mycursor.execute(sql_panier, (id_client,)) 
    articles_panier = mycursor.fetchall()

    # 5. Calcul du total
    if len(articles_panier) >= 1:
        sql_total = ''' 
            SELECT SUM(ligne_panier.quantite * fusee.prix_fusee) AS total
            FROM fusee
            JOIN ligne_panier ON fusee.id_fusee = ligne_panier.fusee_id_panier
            WHERE ligne_panier.utilisateur_id_panier = %s
        '''
        mycursor.execute(sql_total, (id_client,))
        res_total = mycursor.fetchone()
        prix_total = res_total['total'] if res_total else 0
    else:
        prix_total = None

    # --- LA CORRECTION POUR LES DOUBLONS ---
    # Ton HTML a deux boucles. On en "neutralise" une en envoyant une liste vide.
    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article, # Cette liste sera affichée
                           libelle_articles=[]          # On envoie du vide ici pour supprimer le doublon
                           )
