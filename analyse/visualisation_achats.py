import pandas as pd
import matplotlib.pyplot as plt

def visualiser_achats(df):
    """
    Affiche un graphique de l'évolution des achats dans le temps.
    Args:
        df (pd.DataFrame): Données d'achats avec colonnes 'date' et 'montant'.
    """
    if 'date' not in df.columns or 'montant' not in df.columns:
        print("Les colonnes 'date' et 'montant' sont requises.")
        return
    df['date'] = pd.to_datetime(df['date'])
    df_grouped = df.groupby('date')['montant'].sum().reset_index()
    plt.figure(figsize=(10,5))
    plt.plot(df_grouped['date'], df_grouped['montant'], marker='o')
    plt.title("Évolution des achats dans le temps")
    plt.xlabel("Date")
    plt.ylabel("Montant total des achats")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        visualiser_achats(df)
