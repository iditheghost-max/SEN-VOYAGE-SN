import pandas as pd

def generer_rapport_achats(stats, fichier_rapport):
    """
    Génère un rapport texte simple à partir des statistiques d'achats.
    Args:
        stats (dict): Statistiques calculées sur les achats.
        fichier_rapport (str): Chemin du fichier de rapport à générer.
    """
    try:
        with open(fichier_rapport, 'w', encoding='utf-8') as f:
            f.write("Rapport d'analyse des achats\n")
            f.write("============================\n")
            for cle, valeur in stats.items():
                f.write(f"{cle} : {valeur}\n")
        print(f"Rapport généré : {fichier_rapport}")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    from analyse.analyse_achats import analyse_achats
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        stats = analyse_achats(df)
        generer_rapport_achats(stats, 'rapport_achats.txt')
