#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   SELECT id_fusee AS id_article,
    prix_fusee AS prix, 
    stock_fusee AS stock,
    nom_fusee AS nom,
    image_fusee AS image, 
    categorie.libelle_categorie AS libelle
    FROM fusee
    JOIN categorie ON fusee.categorie_id = categorie.id_categorie;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    
    sql = 'SELECT libelle_categorie AS libelle FROM categorie'
    mycursor.execute(sql)
    libelle_articles = mycursor.fetchall()
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    #articles =[]


    # pour le filtre
    types_article = []

    sql = '''
        SELECT f.nom_fusee AS nom, 
               lp.quantite AS quantite, 
               f.prix_fusee AS prix, 
               f.id_fusee AS id_article,
               f.stock_fusee AS stock
               
        FROM ligne_panier lp
        JOIN fusee f ON lp.fusee_id_panier = f.id_fusee
        WHERE lp.utilisateur_id_panier = %s
    '''
    
    mycursor.execute(sql, (id_client,)) 
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
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           , libelle_articles=libelle_articles
                           )
