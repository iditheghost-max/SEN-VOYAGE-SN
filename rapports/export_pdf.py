from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generer_pdf(stats, fichier_pdf):
    """
    Génère un rapport PDF simple à partir des statistiques.
    Args:
        stats (dict): Statistiques à inclure.
        fichier_pdf (str): Chemin du PDF à générer.
    """
    try:
        c = canvas.Canvas(fichier_pdf, pagesize=A4)
        c.setFont("Helvetica", 14)
        c.drawString(100, 800, "Rapport d'analyse des achats")
        c.setFont("Helvetica", 12)
        y = 760
        for cle, valeur in stats.items():
            c.drawString(100, y, f"{cle} : {valeur}")
            y -= 30
        c.save()
        print(f"PDF généré : {fichier_pdf}")
    except Exception as e:
        print(f"Erreur PDF : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    from analyse.analyse_achats import analyse_achats
    from importation_donnees.import_achats import importer_achats
    df = importer_achats('achats.csv')
    if df is not None:
        stats = analyse_achats(df)
        generer_pdf(stats, 'rapport_achats.pdf')
