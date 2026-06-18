import pandas as pd

def analyse_achats(df):
    """
    Analyse basique des achats : total, moyenne, nombre d'achats.
    Args:
        df (pd.DataFrame): Données d'achats.
    Returns:
        dict: Résultats de l'analyse.
    """
    resultats = {}
    if 'montant' in df.columns:
        resultats['total_achats'] = df['montant'].sum()
        resultats['moyenne_achats'] = df['montant'].mean()
        resultats['nombre_achats'] = df['montant'].count()
    else:
        print("La colonne 'montant' est manquante dans les données.")
    return resultats

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        stats = analyse_achats(df)
        print(stats)
