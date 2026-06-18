import streamlit as st
import pandas as pd
import os

def charger_donnees(fichier):
    if os.path.exists(fichier):
        return pd.read_csv(fichier)
    return pd.DataFrame()

def main():
    st.title("Tableau de bord - Commerce")
    onglet = st.sidebar.selectbox("Section", ["Achats", "Ventes"])
    if onglet == "Achats":
        df = charger_donnees('achats.csv')
        st.header("Données d'achats")
        st.dataframe(df)
        if not df.empty and 'montant' in df.columns:
            st.line_chart(df.groupby('date')['montant'].sum())
    elif onglet == "Ventes":
        df = charger_donnees('ventes.csv')
        st.header("Données de ventes")
        st.dataframe(df)
        if not df.empty and 'montant' in df.columns:
            st.line_chart(df.groupby('date')['montant'].sum())

if __name__ == "__main__":
    main()
