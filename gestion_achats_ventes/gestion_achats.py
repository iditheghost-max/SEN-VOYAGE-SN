import pandas as pd

def enregistrer_achat(df, nouvel_achat):
    """
    Ajoute un nouvel achat au DataFrame existant.
    Args:
        df (pd.DataFrame): Données d'achats existantes.
        nouvel_achat (dict): Détails du nouvel achat (ex: {'date': '2026-04-25', 'produit': 'PC', 'montant': 1200}).
    Returns:
        pd.DataFrame: DataFrame mis à jour.
    """
    return pd.concat([df, pd.DataFrame([nouvel_achat])], ignore_index=True)

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        nouvel_achat = {'date': '2026-04-25', 'produit': 'PC', 'montant': 1200}
        df = enregistrer_achat(df, nouvel_achat)
        print(df.tail())
        # Pour sauvegarder les modifications :
        df.to_csv('achats.csv', index=False)
