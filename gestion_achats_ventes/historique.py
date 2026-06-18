import datetime

def enregistrer_log(action, details, fichier='historique.log'):
    """
    Enregistre une action dans le fichier d'historique.
    Args:
        action (str): Type d'action (ex: 'ajout_achat').
        details (str): Détails de l'action.
        fichier (str): Chemin du fichier log.
    """
    with open(fichier, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now().isoformat()} | {action} | {details}\n")

# Exemple d'utilisation
if __name__ == "__main__":
    enregistrer_log('ajout_achat', 'Achat de 5 PC à 1200€ chacun')
