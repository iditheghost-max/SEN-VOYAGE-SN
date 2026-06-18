import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def prevoir_achats(df, jours=7):
    """
    Prédit le montant des achats pour les prochains jours avec une régression linéaire.
    Args:
        df (pd.DataFrame): Données avec colonnes 'date' et 'montant'.
        jours (int): Nombre de jours à prédire.
    Returns:
        list: Prédictions pour les prochains jours.
    """
    if 'date' not in df.columns or 'montant' not in df.columns:
        return []
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['jour'] = (df['date'] - df['date'].min()).dt.days
    X = df[['jour']]
    y = df['montant']
    model = LinearRegression()
    model.fit(X, y)
    jours_futurs = np.arange(df['jour'].max() + 1, df['jour'].max() + 1 + jours).reshape(-1, 1)
    predictions = model.predict(jours_futurs)
    return predictions.tolist()

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    print(prevoir_achats(df, 7))
