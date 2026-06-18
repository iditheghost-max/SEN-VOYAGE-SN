import pandas as pd
import numpy as np

def detecter_anomalies(df, seuil=2.5):
    """
    Détecte les anomalies dans la colonne 'montant' en utilisant l'écart-type.
    Args:
        df (pd.DataFrame): Données avec colonne 'montant'.
        seuil (float): Nombre d'écarts-types pour définir une anomalie.
    Returns:
        pd.DataFrame: Lignes considérées comme anomalies.
    """
    if 'montant' not in df.columns:
        return pd.DataFrame()
    moyenne = df['montant'].mean()
    ecart_type = df['montant'].std()
    anomalies = df[np.abs(df['montant'] - moyenne) > seuil * ecart_type]
    return anomalies

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    anomalies = detecter_anomalies(df)
    print(anomalies)
