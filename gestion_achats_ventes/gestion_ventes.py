import pandas as pd

def enregistrer_vente(df, nouvelle_vente):
    """
    Ajoute une nouvelle vente au DataFrame existant.
    Args:
        df (pd.DataFrame): Données de ventes existantes.
        nouvelle_vente (dict): Détails de la vente (ex: {'date': '2026-04-25', 'produit': 'PC', 'montant': 1500}).
    Returns:
        pd.DataFrame: DataFrame mis à jour.
    """
    return pd.concat([df, pd.DataFrame([nouvelle_vente])], ignore_index=True)

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_ventes import importer_ventes
    df = importer_ventes('ventes.csv')
    if df is not None:
        nouvelle_vente = {'date': '2026-04-25', 'produit': 'PC', 'montant': 1500}
        df = enregistrer_vente(df, nouvelle_vente)
        print(df.tail())
        # Pour sauvegarder les modifications :
        df.to_csv('ventes.csv', index=False)
