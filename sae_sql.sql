DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS fusee;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE categorie (
    id_categorie INT AUTO_INCREMENT,
    libelle_categorie VARCHAR(255),
    PRIMARY KEY (id_categorie)
);

CREATE TABLE couleur (
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(255),
    PRIMARY KEY (id_couleur)
);

CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY (id_etat)
);

CREATE TABLE fusee (
    id_fusee INT AUTO_INCREMENT,
    nom_fusee VARCHAR(255),
    prix_fusee NUMERIC(15,2),
    stock_fusee INT,
    description_fusee VARCHAR(255),
    hauteur_explosion INT,
    duree_explosion INT,
    calibre_fusee INT NULL,
    distance_securite INT,
    niveau_sonore INT,
    image_fusee VARCHAR(255),
    certification VARCHAR(255),
    effet VARCHAR(255),
    pays VARCHAR(255),
    couleur_id INT NULL,
    categorie_id INT NOT NULL,
    PRIMARY KEY (id_fusee),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
    FOREIGN KEY (categorie_id) REFERENCES categorie(id_categorie)
);

CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255),
    est_actif tinyint(1),
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE ligne_panier (
    utilisateur_id_panier INT NOT NULL,
    fusee_id_panier INT NOT NULL,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id_panier, fusee_id_panier),
    FOREIGN KEY (utilisateur_id_panier) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (fusee_id_panier) REFERENCES fusee(id_fusee)
);

CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    etat_id INT NOT NULL,
    utilisateur_id_commande INT NOT NULL,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    FOREIGN KEY (utilisateur_id_commande) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande (
    commande_id INT NOT NULL,
    fusee_id_commande INT NOT NULL,
    prix NUMERIC(15,2),
    quantite INT,
    PRIMARY KEY (commande_id, fusee_id_commande),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (fusee_id_commande) REFERENCES fusee(id_fusee)
);

INSERT INTO couleur (libelle_couleur) VALUES
('Vert'),
('Jaune'),
('Orange'),
('Rouge'),
('Rose'),
('Violet'),
('Bleu'),
('Cyan');

INSERT INTO etat (libelle_etat) VALUES
('Préparation'),
('Expédié'),
('Livraison en cours'),
('Livré');

INSERT INTO categorie (libelle_categorie) VALUES
('Fusée'),
('Chandelle'),
('fumigène'),
('Compact'),
('feu artifice portable'),
('fontaine');

INSERT INTO utilisateur(login,email,password,role,nom,est_actif) VALUES
('admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin',1),
('client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client',1),
('client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2',1);

INSERT INTO fusee (prix_fusee, nom_fusee, stock_fusee, description_fusee, hauteur_explosion, duree_explosion, calibre_fusee, distance_securite, niveau_sonore, image_fusee, certification, effet, pays, couleur_id, categorie_id) VALUES
(12.50, 'Assortiment 10 fusées electron', 150, 'assortiment 10 fusées electron', 20, 0, 15, 8, 90, 'feu_artifice1.png', 'CE F2', 'Étoiles néon', 'Chine', 4, 1),
(45.00, 'Fire images', 30, 'fire images', 25, 20, 20, 8, 105, 'feu_artifice2.png', 'CE F2', 'Pluie d\'or et d\'argent', 'Pologne', 2, 4),
(8.90, 'Assortiment 10 fusées cannon ball power pro', 200, 'assortiment 10 fusées cannon ball power pro', 40, 0, 30, 25, 115, 'feu_artifice3.png', 'CE F3', 'Grosses pivoines', 'Chine', 3, 1),
(19.99, 'Compact magic power', 80, 'compact magic power', 30, 25, 20, 8, 105, 'feu_artifice4.png', 'CE F2', 'Palmiers scintillants', 'Chine', 7, 4),
(5.50, 'Feu d''artifice portable bouquet or et argent prestige', 500, 'feu d''artifice portable bouquet or et argent prestige', 35, 35, 30, 25, 118, 'feu_artifice5.png', 'CE F3', 'Pluie de comètes', 'Chine', 1, 5),
(2.50, 'Compact tempete australe', 1000, 'compact tempete australe', 18, 60, 15, 8, 95, 'feu_artifice6.png', 'CE F2', 'Feu nourri', 'Chine', 3, 4),
(59.90, 'Detonator', 20, 'detonator', 40, 30, 30, 25, 120, 'feu_artifice7.png', 'CE F3', 'Effets Brocarts', 'Chine', 6, 4),
(14.00, 'Asian human', 120, 'asian human', 25, 25, 20, 8, 105, 'feu_artifice8.png', 'CE F2', 'Pivoines classiques', 'Chine', 1, 4),
(3.00, 'Giant maniax', 300, 'giant maniax', 20, 70, 15, 8, 100, 'feu_artifice9.png', 'CE F2', 'Rafales rapides', 'Chine', 4, 4),
(22.50, 'Showbox fascination 5mn', 60, 'showbox fascination 5mn', 30, 300, 20, 25, 110, 'feu_artifice10.png', 'CE F3', 'Spectacle complet', 'Chine', 2, 5),
(19.95, 'Vésuve magnum Argent ardi', 100, 'vésuve magnum Argent ardi', 5, 45, Null, 8, 80, 'feu_artifice11.png', 'CE F2', 'Fontaine conique', 'Chine', 8, 6),
(1.75, 'Fontaine viper', 40, 'fontaine viper', 3, 30, Null, 8, 85, 'feu_artifice12.png', 'CE F2', 'Fontaine tubulaire', 'France', 7, 6),
(4.50, 'Fusée Sifflet Infernal', 150, 'Fusée Sifflet Infernal', 30, 0, 15, 25, 110, 'feu_artifice13.png', 'CE F2', 'Bouquets aériens', 'Chine', 3, 1),
(95.00, 'Panaché de 24 fusées de 50 mm', 10, 'panaché de 24 fusées de 50 mm', 50, 0, 50, 25, 120, 'feu_artifice14.png', 'CE F3', 'Effets variés', 'Chine', 5, 1),
(3.50, '3 chandelles 20 effets', 250, '3 chandelles 20 effets', 15, 25, 10, 15, 95, 'feu_artifice15.png', 'CE F2', 'Succession de comètes', 'Chine', 4, 2),
(7.15, 'sachet de 3 chandelles monocoup intermezzo', 55, 'sachet de 3 chandelles monocoup intermezzo', 25, 5, 28, 15, 115, 'feu_artifice16.png', 'CE F2', 'Monocoup puissant', 'Chine', 5, 2),
(5.50, 'Ardi Scène Argent', 110, 'Ardi Scène Argent', 2, 40, Null, 2, 50, 'feu_artifice17.png', 'CE T1', 'Gerbe froide', 'Chine', 8, 6),
(5.50, 'Ardi Scène Or', 75, 'Ardi Scène Or', 2, 25, Null, 2, 50, 'feu_artifice18.png', 'CE T1', 'Gerbe froide', 'Chine', 2, 6),
(4.8, 'Pot fumigène 1mn Orange', 15, 'pot fumigène 1mn Orange', 0, 60, Null, 8, 20, 'feu_artifice19.png', 'CE P1', 'Nuage opaque', 'Chine', 4, 3),
(4.8, 'Pot de fumigène 1mn Rose', 400, 'pot de fumigène 1mn Rose', 0, 60, Null, 8, 20, 'feu_artifice20.png', 'CE P1', 'Nuage opaque', 'Chine', 8, 3);

INSERT INTO commande (date_achat, etat_id, utilisateur_id_commande) VALUES
('2025-04-08', 4, 2),
('2026-01-25', 1, 3),
('2025-12-20', 3, 2);

INSERT INTO ligne_commande (commande_id, fusee_id_commande, prix, quantite) VALUES
(1, 1, 25, 2),
(1, 2, 135, 3),
(2, 5, 22, 4),
(3, 3, 8.90, 1),
(3, 12, 3.5, 2),
(3, 14, 95, 1);
