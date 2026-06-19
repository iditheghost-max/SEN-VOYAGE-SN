import streamlit as st
import pandas as pd
import os
from datetime import datetime
from gestion_achats_ventes.gestion_achats import enregistrer_achat
from gestion_achats_ventes.gestion_ventes import enregistrer_vente
from gestion_achats_ventes.stock import charger_stock, maj_stock, sauvegarder_stock
from gestion_achats_ventes.historique import enregistrer_log

DATA_FILES = {
    'achats': 'achats.csv',
    'ventes': 'ventes.csv',
    'stock': 'stock.csv'
}

DEFAULT_ACHATS_COLUMNS = ['date', 'produit', 'quantite', 'montant', 'fournisseur']
DEFAULT_VENTES_COLUMNS = ['date', 'produit', 'quantite', 'montant', 'client']


def charger_donnees(fichier, colonnes=None):
    if os.path.exists(fichier):
        try:
            df = pd.read_csv(fichier)
            if colonnes:
                for col in colonnes:
                    if col not in df.columns:
                        df[col] = ''
            return df
        except Exception:
            return pd.DataFrame(columns=colonnes or [])
    return pd.DataFrame(columns=colonnes or [])


def sauvegarder_donnees(df, fichier):
    df.to_csv(fichier, index=False)


def format_dates(df):
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        except Exception:
            pass
    return df


def initialiser_fichiers():
    if not os.path.exists(DATA_FILES['achats']):
        pd.DataFrame(columns=DEFAULT_ACHATS_COLUMNS).to_csv(DATA_FILES['achats'], index=False)
    if not os.path.exists(DATA_FILES['ventes']):
        pd.DataFrame(columns=DEFAULT_VENTES_COLUMNS).to_csv(DATA_FILES['ventes'], index=False)
    if not os.path.exists(DATA_FILES['stock']):
        charger_stock(DATA_FILES['stock']).to_csv(DATA_FILES['stock'], index=False)


def afficher_bilan(df_achats, df_ventes):
    recettes = df_ventes['montant'].sum() if not df_ventes.empty else 0
    depenses = df_achats['montant'].sum() if not df_achats.empty else 0
    resultat = recettes - depenses
    col1, col2, col3 = st.columns(3)
    col1.metric('Recettes', f"{recettes:.2f} FCFA")
    col2.metric('Dépenses', f"{depenses:.2f} FCFA")
    col3.metric('Résultat net', f"{resultat:.2f} FCFA")
    return recettes, depenses, resultat


def main():
    st.set_page_config(page_title='Gestion & Comptabilité', page_icon='💼', layout='wide')
    st.title('Plateforme de gestion et comptabilité')

    initialiser_fichiers()

    menu = st.sidebar.selectbox('Section', ['Tableau de bord', 'Achats', 'Ventes', 'Stock', 'Bilan'])

    df_achats = format_dates(charger_donnees(DATA_FILES['achats'], DEFAULT_ACHATS_COLUMNS))
    df_ventes = format_dates(charger_donnees(DATA_FILES['ventes'], DEFAULT_VENTES_COLUMNS))
    df_stock = charger_stock(DATA_FILES['stock'])

    if menu == 'Tableau de bord':
        st.header('Résumé rapide')
        recettes, depenses, resultat = afficher_bilan(df_achats, df_ventes)
        st.markdown('### Graphiques')
        if not df_achats.empty and 'date' in df_achats.columns:
            st.subheader('Dépenses par date')
            st.line_chart(df_achats.groupby('date')['montant'].sum())
        if not df_ventes.empty and 'date' in df_ventes.columns:
            st.subheader('Recettes par date')
            st.line_chart(df_ventes.groupby('date')['montant'].sum())

    elif menu == 'Achats':
        st.header('Gestion des achats')
        st.dataframe(df_achats)
        with st.form('form_achat'):
            st.subheader('Ajouter un achat')
            date = st.date_input('Date', datetime.today())
            produit = st.text_input('Produit')
            quantite = st.number_input('Quantité', min_value=1, value=1)
            montant = st.number_input('Montant (FCFA)', min_value=0.0, value=0.0)
            fournisseur = st.text_input('Fournisseur')
            enregistrer = st.form_submit_button('Enregistrer l’achat')
            if enregistrer:
                nouvel_achat = {
                    'date': date.strftime('%Y-%m-%d'),
                    'produit': produit,
                    'quantite': quantite,
                    'montant': montant,
                    'fournisseur': fournisseur
                }
                df_achats = enregistrer_achat(df_achats, nouvel_achat)
                sauvegarder_donnees(df_achats, DATA_FILES['achats'])
                df_stock = maj_stock(df_stock, {'produit': produit, 'quantite': quantite, 'type': 'entree'})
                sauvegarder_stock(df_stock, DATA_FILES['stock'])
                enregistrer_log('ajout_achat', f"{quantite} x {produit} pour {montant} FCFA, fournisseur {fournisseur}")
                st.success('Achat enregistré avec succès.')
                st.rerun()

    elif menu == 'Ventes':
        st.header('Gestion des ventes')
        st.dataframe(df_ventes)
        with st.form('form_vente'):
            st.subheader('Ajouter une vente')
            date = st.date_input('Date', datetime.today())
            produit = st.text_input('Produit', key='vente_produit')
            quantite = st.number_input('Quantité', min_value=1, value=1, key='vente_quantite')
            montant = st.number_input('Montant (FCFA)', min_value=0.0, value=0.0, key='vente_montant')
            client = st.text_input('Client')
            enregistrer = st.form_submit_button('Enregistrer la vente')
            if enregistrer:
                nouvelle_vente = {
                    'date': date.strftime('%Y-%m-%d'),
                    'produit': produit,
                    'quantite': quantite,
                    'montant': montant,
                    'client': client
                }
                df_ventes = enregistrer_vente(df_ventes, nouvelle_vente)
                sauvegarder_donnees(df_ventes, DATA_FILES['ventes'])
                df_stock = maj_stock(df_stock, {'produit': produit, 'quantite': quantite, 'type': 'sortie'})
                sauvegarder_stock(df_stock, DATA_FILES['stock'])
                enregistrer_log('ajout_vente', f"{quantite} x {produit} pour {montant} FCFA, client {client}")
                st.success('Vente enregistrée avec succès.')
                st.rerun()

    elif menu == 'Stock':
        st.header('Suivi du stock')
        st.dataframe(df_stock)
        with st.form('form_stock'):
            st.subheader('Mettre à jour le stock')
            produit = st.text_input('Produit', key='stock_produit')
            quantite = st.number_input('Quantité', min_value=1, value=1, key='stock_quantite')
            type_mouvement = st.selectbox('Type de mouvement', ['entree', 'sortie'])
            appliquer = st.form_submit_button('Appliquer le mouvement')
            if appliquer:
                df_stock = maj_stock(df_stock, {'produit': produit, 'quantite': quantite, 'type': type_mouvement})
                sauvegarder_stock(df_stock, DATA_FILES['stock'])
                enregistrer_log('maj_stock', f"{type_mouvement} de {quantite} sur {produit}")
                st.success('Stock mis à jour.')
                st.rerun()

    elif menu == 'Bilan':
        st.header('Bilan comptable')
        recettes, depenses, resultat = afficher_bilan(df_achats, df_ventes)
        st.markdown('### Détails des opérations')
        st.subheader('Achats')
        st.dataframe(df_achats)
        st.subheader('Ventes')
        st.dataframe(df_ventes)
        if not df_ventes.empty and not df_achats.empty:
            st.subheader('Marge par produit')
            marge = df_ventes.groupby('produit')['montant'].sum().subtract(df_achats.groupby('produit')['montant'].sum(), fill_value=0)
            st.dataframe(marge.reset_index(name='marge'))

if __name__ == '__main__':
    main()
