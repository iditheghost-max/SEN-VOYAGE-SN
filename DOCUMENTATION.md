# Documentation récapitulative

## 1. Importation de données
- **importation_donnees/import_achats.py** : Importer les achats depuis un CSV.
- **importation_donnees/import_ventes.py** : Importer les ventes depuis un CSV.
- **importation_donnees/import_banque.py** : Importer un relevé bancaire.

## 2. Analyse et visualisation
- **analyse/analyse_achats.py** : Analyse basique des achats (total, moyenne, nombre).
- **analyse/visualisation_achats.py** : Graphique de l’évolution des achats.
- **analyse/alertes_achats.py** : Détection d’anomalies dans les achats.
- **analyse/previsions_achats.py** : Prévision des achats (régression linéaire).

## 3. Gestion des achats, ventes et stock
- **gestion_achats_ventes/gestion_achats.py** : Ajouter un achat.
- **gestion_achats_ventes/gestion_ventes.py** : Ajouter une vente.
- **gestion_achats_ventes/stock.py** : Suivi et mise à jour du stock.

## 4. Rapports et export
- **rapports/rapport_achats.py** : Générer un rapport texte.
- **rapports/export_excel.py** : Exporter les achats en Excel.
- **rapports/export_pdf.py** : Générer un rapport PDF.

## 5. Sécurité et multi-utilisateurs
- **gestion_achats_ventes/utilisateurs.py** : Gestion des utilisateurs (création, connexion).

## 6. Tableau de bord interactif
- **main_dashboard.py** : Interface web avec Streamlit pour visualiser achats et ventes.

## 7. Historique et audit
- **gestion_achats_ventes/historique.py** : Enregistrement des actions dans un fichier log.

---

### Lancement du tableau de bord
```bash
streamlit run main_dashboard.py
```

### Lancement du script principal
```bash
python main.py
```

### Dépendances principales
- pandas, numpy, matplotlib, streamlit, openpyxl, reportlab, scikit-learn

---

Chaque module contient un exemple d’utilisation en bas du fichier. Personnalisez selon vos besoins !
