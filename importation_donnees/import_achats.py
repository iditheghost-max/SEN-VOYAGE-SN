import pandas as pd

def importer_achats(fichier_csv):
    """
    Importe les données d'achats depuis un fichier CSV.
    Args:
        fichier_csv (str): Chemin du fichier CSV à importer.
    Returns:
        pd.DataFrame: Données importées sous forme de DataFrame.
    """
    try:
        df = pd.read_csv(fichier_csv)
        print(f"{len(df)} lignes importées depuis {fichier_csv}")
        return df
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    # Remplacer 'achats.csv' par le chemin réel de votre fichier
    df_achats = importer_achats('achats.csv')
    if df_achats is not None:
        print(df_achats.head())
