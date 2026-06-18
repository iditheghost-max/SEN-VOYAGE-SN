import hashlib
import json
import os

def charger_utilisateurs(fichier='utilisateurs.json'):
    if os.path.exists(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def enregistrer_utilisateurs(utilisateurs, fichier='utilisateurs.json'):
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(utilisateurs, f, indent=2)

def creer_utilisateur(nom, mot_de_passe, fichier='utilisateurs.json'):
    utilisateurs = charger_utilisateurs(fichier)
    if nom in utilisateurs:
        print("Utilisateur déjà existant.")
        return False
    hash_mp = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    utilisateurs[nom] = hash_mp
    enregistrer_utilisateurs(utilisateurs, fichier)
    print("Utilisateur créé.")
    return True

def verifier_connexion(nom, mot_de_passe, fichier='utilisateurs.json'):
    utilisateurs = charger_utilisateurs(fichier)
    hash_mp = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    return utilisateurs.get(nom) == hash_mp

# Exemple d'utilisation
if __name__ == "__main__":
    creer_utilisateur('admin', 'motdepasse123')
    print(verifier_connexion('admin', 'motdepasse123'))
