#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  
    SELECT
    fusee.id_fusee AS id_article,
    fusee.nom_fusee AS nom,
    fusee.categorie_id AS type_article_id,
    fusee.prix_fusee AS prix,
    fusee.stock_fusee AS stock,
    fusee.image_fusee AS image,
    categorie.libelle_categorie AS libelle
    FROM fusee
    JOIN categorie ON categorie.id_categorie = fusee.categorie_id;
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = '''
    SELECT
    id_categorie AS id_type_article,
    libelle_categorie AS libelle
    FROM categorie;
    '''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()

    return render_template('admin/article/add_article.html'
                           ,types_article=type_article#,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = ''' INSERT INTO fusee (nom_fusee, image_fusee, prix_fusee, categorie_id, description_fusee) VALUES (%s, %s, %s, %s, %s); '''

    tuple_add = (nom, filename, prix, type_article_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = "SELECT COUNT(*) AS nb_declinaison FROM ligne_panier WHERE fusee_id_panier = %s;"
    mycursor.execute(sql, (id_article,))
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = "SELECT image_fusee AS image FROM fusee WHERE id_fusee = %s;"
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = "DELETE FROM fusee WHERE id_fusee = %s;"
        mycursor.execute(sql, (id_article,))
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT 
    id_fusee AS id_article, 
    nom_fusee AS nom, 
    prix_fusee AS prix, 
    categorie_id AS type_article_id, 
    description_fusee AS description, 
    image_fusee AS image
    FROM fusee 
    WHERE id_fusee = %s;
    '''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    print(article)
    sql = '''
    SELECT 
    id_categorie AS id_type_article, 
    libelle_categorie AS libelle 
    FROM categorie;
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_article)
    # declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                         #  ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       SELECT image_fusee AS image FROM fusee WHERE id_fusee = %s;
       '''
    mycursor.execute(sql, (id_article,))
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  
    UPDATE fusee 
    SET 
    nom_fusee = %s, 
    image_fusee = %s, 
    prix_fusee = %s, 
    categorie_id = %s, 
    description_fusee = %s 
    WHERE id_fusee = %s; 
    '''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
