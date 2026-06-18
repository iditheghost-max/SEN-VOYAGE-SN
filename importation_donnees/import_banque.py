import pandas as pd

def importer_releve_bancaire(fichier_csv):
    """
    Importe un relevé bancaire au format CSV.
    Args:
        fichier_csv (str): Chemin du fichier CSV à importer.
    Returns:
        pd.DataFrame: Données importées.
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
    df = importer_releve_bancaire('releve_bancaire.csv')
    if df is not None:
        print(df.head())
