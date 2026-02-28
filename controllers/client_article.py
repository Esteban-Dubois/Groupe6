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

    # recupere filtre pour session
    word = session.get('filter_word', '')
    prix_min = session.get('filter_prix_min', '')
    prix_max = session.get('filter_prix_max', '')
    types = session.get('filter_types', [])

    # sql pour les articles
    sql = '''   
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
    params = []

    if word:
        sql += " AND nom_fusee LIKE %s"
        params.append(f"%{word}%")
    if prix_min:
        sql += " AND prix_fusee >= %s"
        params.append(prix_min)
    if prix_max:
        sql += " AND prix_fusee <= %s"
        params.append(prix_max)
    if types:
        placeholders = ', '.join(['%s'] * len(types))
        sql += f" AND fusee.categorie_id IN ({placeholders})"
        params.extend(types)

    mycursor.execute(sql, tuple(params))
    articles = mycursor.fetchall()
    
    # 3. SQL des types sans doublon pour le filtre
    sql_types_filtre = '''
        SELECT DISTINCT id_categorie AS id_type_article, 
                        libelle_categorie AS libelle 
        FROM categorie
        ORDER BY libelle ASC
    '''
    mycursor.execute(sql_types_filtre)
    types_article = mycursor.fetchall() 

    # sql du panier
    sql_panier = '''
        SELECT fusee.nom_fusee AS nom, 
               ligne_panier.quantite AS quantite, 
               fusee.prix_fusee AS prix, 
               fusee.id_fusee AS id_article,
               fusee.stock_fusee AS stock
        FROM ligne_panier 
        JOIN fusee ON ligne_panier.fusee_id_panier = fusee.id_fusee
        WHERE ligne_panier.utilisateur_id_panier = %s
    '''
    mycursor.execute(sql_panier, (id_client,)) 
    articles_panier = mycursor.fetchall()

    # calcul prix total du panier
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

    
    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article,
                           libelle_articles=[]          
                           )
