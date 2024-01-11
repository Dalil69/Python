import json
import csv
import smtplib
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ftplib


# Configuration SMTP
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 465
SENDER_EMAIL = 'your_email@example.com'
SENDER_PASSWORD = 'your_password'

class Distributeur:
    def __init__(self, fichier_boissons, fichier_stock):
        self.boissons = self.charger_boissons(fichier_boissons)
        self.stock_pieces, self.stock_boissons = self.charger_stock(fichier_stock)
        self.ventes = defaultdict(int)

    def charger_boissons(self, fichier):
        with open(fichier, 'r') as file:
            return json.load(file)

    def charger_stock(self, fichier):
        stock_pieces = {"5P": 0, "10P": 0, "20P": 0, "50P": 0}
        stock_boissons = {boisson: 10 for boisson in self.boissons}
        with open(fichier, 'r') as file:
            reader = csv.reader(file)
            for piece, quantite in reader:
                stock_pieces[piece] += int(quantite)
        return stock_pieces, stock_boissons

    def afficher_menu(self):
        for boisson, prix in self.boissons.items():
            print(f"{boisson}............... {prix} P")

    def traiter_achat(self, boisson, montant_paye):
        if boisson not in self.boissons:
            print("Boisson non disponible.")
            return False

        prix = self.boissons[boisson]
        if montant_paye < prix:
            print("Montant insuffisant.")
            return False

        # Mise à jour du stock et des ventes
        self.stock_boissons[boisson] -= 1
        self.ventes[boisson] += 1
        return True

    def rendre_monnaie(self, montant_paye, prix):
    a_rendre = montant_paye - prix
    monnaie_rendue = {}

    # Tri des pièces par valeur décroissante pour commencer par les plus grandes valeurs
    pieces_triees = sorted(self.stock_pieces.keys(), key=lambda x: int(x[:-1]), reverse=True)

    for piece in pieces_triees:
        valeur_piece = int(piece[:-1])  # Valeur numérique de la pièce (en ignorant le 'P')
        while a_rendre >= valeur_piece and self.stock_pieces[piece] > 0:
            a_rendre -= valeur_piece
            self.stock_pieces[piece] -= 1
            monnaie_rendue[piece] = monnaie_rendue.get(piece, 0) + 1

    if a_rendre > 0:
        # Si on ne peut pas rendre la monnaie exacte, afficher un message et réajuster le stock
        print("Désolé, je ne peux pas rendre la monnaie exacte.")
        # Réajuster le stock de pièces avec les pièces rendues
        for piece, quantite in monnaie_rendue.items():
            self.stock_pieces[piece] += quantite
        return {}

    return monnaie_rendue
 def telecharger_depuis_ftp(self, ftp_adresse, ftp_utilisateur, ftp_mot_de_passe, fichier_distant, fichier_local):
        with ftplib.FTP(ftp_adresse) as ftp:
            ftp.login(ftp_utilisateur, ftp_mot_de_passe)
            with open(fichier_local, 'wb') as file:
                ftp.retrbinary(f'RETR {fichier_distant}', file.write)

    def envoyer_vers_ftp(self, ftp_adresse, ftp_utilisateur, ftp_mot_de_passe, fichier_local, fichier_distant):
        with ftplib.FTP(ftp_adresse) as ftp:
            ftp.login(ftp_utilisateur, ftp_mot_de_passe)
            with open(fichier_local, 'rb') as file:
                ftp.storbinary(f'STOR {fichier_distant}', file)

    def verifier_stock_pieces(self):
        for piece, quantite in self.stock_pieces.items():
            if quantite == 0:
                self.envoyer_email_alerte(piece)

    def envoyer_email_alerte(self, piece):
    sender_email = "your_email@example.com"  # Remplacer par votre adresse e-mail
    receiver_email = "receiver@example.com"  # Remplacer par l'adresse e-mail du destinataire
    password = "your_password"  # Remplacer par votre mot de passe e-mail

    message = MIMEMultipart("alternative")
    message["Subject"] = "Alerte Distributeur"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Alerte Distributeur:
    Le stock de la pièce '{piece}' est épuisé."""
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.example.com', 465)  # Remplacer par votre serveur SMTP
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("E-mail envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail: {e}")
        pass

  def sauvegarder_ventes_yaml(self, fichier_yaml):
        with open(fichier_yaml, 'w') as file:
            yaml.dump(dict(self.ventes), file, default_flow_style=False)
        pass

# Utilisation du Distributeur
ftp_adresse = 'adresse_du_serveur_ftp'
ftp_utilisateur = 'utilisateur_ftp'
ftp_mot_de_passe = 'mot_de_passe_ftp'
fichier_distant = 'chemin/vers/boisson_sur_ftp.json'
fichier_local = 'chemin_vers_boisson.json'

distributeur = Distributeur(fichier_local, 'chemin_vers_stock.csv')
distributeur.telecharger_depuis_ftp(ftp_adresse, ftp_utilisateur, ftp_mot_de_passe, fichier_distant, fichier_local)
distributeur.afficher_menu()

# À la fermeture de l'application
fichier_ventes_local = 'chemin/vers/ventes.yaml'
fichier_ventes_distant = 'chemin/vers/ventes_sur_ftp.yaml'
distributeur.envoyer_vers_ftp(ftp_adresse, ftp_utilisateur, ftp_mot_de_passe, fichier_ventes_local, fichier_ventes_distant)