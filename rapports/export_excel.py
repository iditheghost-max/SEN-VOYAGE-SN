import pandas as pd

def exporter_achats_excel(df, fichier_excel):
    """
    Exporte les données d'achats au format Excel.
    Args:
        df (pd.DataFrame): Données à exporter.
        fichier_excel (str): Chemin du fichier Excel à générer.
    """
    try:
        df.to_excel(fichier_excel, index=False)
        print(f"Export Excel réussi : {fichier_excel}")
    except Exception as e:
        print(f"Erreur export Excel : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        exporter_achats_excel(df, 'achats_export.xlsx')
