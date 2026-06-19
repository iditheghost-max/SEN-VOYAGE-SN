import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime, timedelta
from gestion_achats_ventes.gestion_achats import enregistrer_achat
from gestion_achats_ventes.gestion_ventes import enregistrer_vente
from gestion_achats_ventes.stock import charger_stock, maj_stock, sauvegarder_stock
from gestion_achats_ventes.historique import enregistrer_log

# Configuration
DATA_FILES = {
    'achats': 'achats.csv',
    'ventes': 'ventes.csv',
    'stock': 'stock.csv'
}

DEFAULT_ACHATS_COLUMNS = ['date', 'produit', 'quantite', 'montant', 'fournisseur']
DEFAULT_VENTES_COLUMNS = ['date', 'produit', 'quantite', 'montant', 'client']


# Fonctions utilitaires
def charger_donnees(fichier, colonnes=None):
    """Charger les données avec validation des colonnes"""
    if os.path.exists(fichier):
        try:
            df = pd.read_csv(fichier)
            if colonnes:
                for col in colonnes:
                    if col not in df.columns:
                        df[col] = ''
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement de {fichier}: {str(e)}")
            return pd.DataFrame(columns=colonnes or [])
    return pd.DataFrame(columns=colonnes or [])


def sauvegarder_donnees(df, fichier):
    """Sauvegarder les données avec vérification"""
    try:
        df.to_csv(fichier, index=False)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde: {str(e)}")
        return False


def format_dates(df):
    """Convertir les colonnes date en datetime"""
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        except Exception:
            pass
    return df


def initialiser_fichiers():
    """Initialiser les fichiers CSV s'ils n'existent pas"""
    if not os.path.exists(DATA_FILES['achats']):
        pd.DataFrame(columns=DEFAULT_ACHATS_COLUMNS).to_csv(DATA_FILES['achats'], index=False)
    if not os.path.exists(DATA_FILES['ventes']):
        pd.DataFrame(columns=DEFAULT_VENTES_COLUMNS).to_csv(DATA_FILES['ventes'], index=False)
    if not os.path.exists(DATA_FILES['stock']):
        charger_stock(DATA_FILES['stock']).to_csv(DATA_FILES['stock'], index=False)


def afficher_kpis(df_achats, df_ventes):
    """Afficher les KPIs principaux"""
    recettes = df_ventes['montant'].sum() if not df_ventes.empty else 0
    depenses = df_achats['montant'].sum() if not df_achats.empty else 0
    resultat = recettes - depenses
    
    marge = ((recettes - depenses) / recettes * 100) if recettes > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        '💰 Recettes',
        f"{recettes:.0f} FCFA",
        delta=f"{len(df_ventes)} ventes" if not df_ventes.empty else None
    )
    col2.metric(
        '💸 Dépenses',
        f"{depenses:.0f} FCFA",
        delta=f"{len(df_achats)} achats" if not df_achats.empty else None
    )
    col3.metric(
        '📊 Résultat net',
        f"{resultat:.0f} FCFA",
        delta=f"{marge:.1f}% marge" if marge > 0 else None,
        delta_color="inverse" if resultat < 0 else "normal"
    )
    col4.metric(
        '📈 Transactions',
        len(df_ventes) + len(df_achats),
        delta=f"{len(df_achats) + len(df_ventes)} total" if not df_achats.empty or not df_ventes.empty else None
    )
    
    return recettes, depenses, resultat


def filtrer_par_dates(df, date_debut, date_fin):
    """Filtrer un dataframe par plage de dates"""
    if df.empty or 'date' not in df.columns:
        return df
    
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], errors='coerce')
    return df_copy[(df_copy['date'] >= pd.Timestamp(date_debut)) & (df_copy['date'] <= pd.Timestamp(date_fin))]


def create_pie_chart(df, label_col, value_col, title):
    """Créer un graphique en camembert"""
    if df.empty:
        return None
    
    data = df.groupby(label_col)[value_col].sum().reset_index()
    fig = px.pie(data, names=label_col, values=value_col, title=title)
    return fig


def create_bar_chart(df, x_col, y_col, title):
    """Créer un diagramme en barres"""
    if df.empty:
        return None
    
    data = df.groupby(x_col)[y_col].sum().reset_index()
    fig = px.bar(data, x=x_col, y=y_col, title=title, color=y_col, 
                 color_continuous_scale='Blues')
    return fig


def exporter_donnees(df, nom_fichier):
    """Exporter les données en CSV"""
    csv = df.to_csv(index=False)
    return csv


# Configuration de la page
st.set_page_config(
    page_title='💼 Gestion & Comptabilité',
    page_icon='💼',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Style personnalisé
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre principal
st.title('💼 Plateforme de gestion et comptabilité')
st.markdown('---')

# Initialisation
initialiser_fichiers()

# Charger les données
df_achats = format_dates(charger_donnees(DATA_FILES['achats'], DEFAULT_ACHATS_COLUMNS))
df_ventes = format_dates(charger_donnees(DATA_FILES['ventes'], DEFAULT_VENTES_COLUMNS))
df_stock = charger_stock(DATA_FILES['stock'])

# Menu principal avec tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(['📊 Tableau de bord', '🛍️ Achats', '💳 Ventes', '📦 Stock', '📈 Bilan'])

# ==========================
# TAB 1: TABLEAU DE BORD
# ==========================
with tab1:
    st.header('📊 Tableau de bord')
    
    # KPIs
    afficher_kpis(df_achats, df_ventes)
    
    st.markdown('---')
    
    # Filtres de dates
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        date_debut = st.date_input('Date de début', datetime.now() - timedelta(days=30))
    with col_filter2:
        date_fin = st.date_input('Date de fin', datetime.now())
    
    # Filtrer les données
    df_achats_filtered = filtrer_par_dates(df_achats, date_debut, date_fin)
    df_ventes_filtered = filtrer_par_dates(df_ventes, date_debut, date_fin)
    
    st.markdown('---')
    
    # Graphiques principaux
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        if not df_achats_filtered.empty and 'date' in df_achats_filtered.columns:
            data_achats = df_achats_filtered.groupby(df_achats_filtered['date'].dt.date)['montant'].sum()
            fig_achats = go.Figure(data=go.Scatter(x=data_achats.index, y=data_achats.values, 
                                                    mode='lines+markers', name='Dépenses'))
            fig_achats.update_layout(title='📉 Dépenses par jour', height=400)
            st.plotly_chart(fig_achats, use_container_width=True)
    
    with col_graph2:
        if not df_ventes_filtered.empty and 'date' in df_ventes_filtered.columns:
            data_ventes = df_ventes_filtered.groupby(df_ventes_filtered['date'].dt.date)['montant'].sum()
            fig_ventes = go.Figure(data=go.Scatter(x=data_ventes.index, y=data_ventes.values,
                                                    mode='lines+markers', name='Recettes', 
                                                    line=dict(color='green')))
            fig_ventes.update_layout(title='📈 Recettes par jour', height=400)
            st.plotly_chart(fig_ventes, use_container_width=True)
    
    # Camemberts
    col_pie1, col_pie2 = st.columns(2)
    
    with col_pie1:
        if not df_achats_filtered.empty:
            fig_achats_pie = create_pie_chart(df_achats_filtered, 'fournisseur', 'montant', 
                                              '🏭 Achats par fournisseur')
            if fig_achats_pie:
                st.plotly_chart(fig_achats_pie, use_container_width=True)
    
    with col_pie2:
        if not df_ventes_filtered.empty:
            fig_ventes_pie = create_pie_chart(df_ventes_filtered, 'client', 'montant',
                                              '👥 Ventes par client')
            if fig_ventes_pie:
                st.plotly_chart(fig_ventes_pie, use_container_width=True)


# ==========================
# TAB 2: ACHATS
# ==========================
with tab2:
    st.header('🛍️ Gestion des achats')
    
    tab_achats1, tab_achats2 = st.tabs(['📋 Données', '➕ Ajouter'])
    
    with tab_achats1:
        if not df_achats.empty:
            st.subheader('Liste des achats')
            st.dataframe(df_achats, use_container_width=True)
            
            # Statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric('Total des achats', f"{df_achats['montant'].sum():.0f} FCFA")
            with col_stat2:
                st.metric('Nombre d\'achats', len(df_achats))
            with col_stat3:
                st.metric('Achat moyen', f"{df_achats['montant'].mean():.0f} FCFA")
            
            # Export
            csv = exporter_donnees(df_achats, 'achats')
            st.download_button(
                label='📥 Télécharger en CSV',
                data=csv,
                file_name=f'achats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        else:
            st.info('Aucun achat enregistré pour le moment.')
    
    with tab_achats2:
        st.subheader('Ajouter un nouvel achat')
        with st.form('form_achat'):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                date_achat = st.date_input('📅 Date', datetime.today(), key='achat_date')
                produit_achat = st.text_input('📦 Produit', key='achat_produit', placeholder='Ex: Riz')
                fournisseur_achat = st.text_input('🏭 Fournisseur', key='achat_fournisseur', placeholder='Ex: Fournisseur ABC')
            
            with col_form2:
                quantite_achat = st.number_input('📊 Quantité', min_value=1, value=1, key='achat_quantite')
                montant_achat = st.number_input('💰 Montant (FCFA)', min_value=0.0, value=0.0, 
                                               step=100.0, key='achat_montant')
            
            enregistrer_achat_btn = st.form_submit_button('✅ Enregistrer l\'achat', use_container_width=True)
            
            if enregistrer_achat_btn:
                if not produit_achat or montant_achat <= 0:
                    st.error('❌ Veuillez remplir tous les champs correctement')
                else:
                    nouvel_achat = {
                        'date': date_achat.strftime('%Y-%m-%d'),
                        'produit': produit_achat,
                        'quantite': quantite_achat,
                        'montant': montant_achat,
                        'fournisseur': fournisseur_achat
                    }
                    df_achats = enregistrer_achat(df_achats, nouvel_achat)
                    if sauvegarder_donnees(df_achats, DATA_FILES['achats']):
                        df_stock = maj_stock(df_stock, {'produit': produit_achat, 'quantite': quantite_achat, 'type': 'entree'})
                        sauvegarder_stock(df_stock, DATA_FILES['stock'])
                        enregistrer_log('ajout_achat', f"{quantite_achat} x {produit_achat} pour {montant_achat} FCFA")
                        st.success('✅ Achat enregistré avec succès!')
                        st.rerun()


# ==========================
# TAB 3: VENTES
# ==========================
with tab3:
    st.header('💳 Gestion des ventes')
    
    tab_ventes1, tab_ventes2 = st.tabs(['📋 Données', '➕ Ajouter'])
    
    with tab_ventes1:
        if not df_ventes.empty:
            st.subheader('Liste des ventes')
            st.dataframe(df_ventes, use_container_width=True)
            
            # Statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric('Total des ventes', f"{df_ventes['montant'].sum():.0f} FCFA")
            with col_stat2:
                st.metric('Nombre de ventes', len(df_ventes))
            with col_stat3:
                st.metric('Vente moyenne', f"{df_ventes['montant'].mean():.0f} FCFA")
            
            # Export
            csv = exporter_donnees(df_ventes, 'ventes')
            st.download_button(
                label='📥 Télécharger en CSV',
                data=csv,
                file_name=f'ventes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        else:
            st.info('Aucune vente enregistrée pour le moment.')
    
    with tab_ventes2:
        st.subheader('Ajouter une nouvelle vente')
        with st.form('form_vente'):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                date_vente = st.date_input('📅 Date', datetime.today(), key='vente_date')
                produit_vente = st.text_input('📦 Produit', key='vente_produit', placeholder='Ex: Riz')
                client_vente = st.text_input('👥 Client', key='vente_client', placeholder='Ex: Client XYZ')
            
            with col_form2:
                quantite_vente = st.number_input('📊 Quantité', min_value=1, value=1, key='vente_quantite')
                montant_vente = st.number_input('💰 Montant (FCFA)', min_value=0.0, value=0.0,
                                               step=100.0, key='vente_montant')
            
            enregistrer_vente_btn = st.form_submit_button('✅ Enregistrer la vente', use_container_width=True)
            
            if enregistrer_vente_btn:
                if not produit_vente or montant_vente <= 0:
                    st.error('❌ Veuillez remplir tous les champs correctement')
                else:
                    nouvelle_vente = {
                        'date': date_vente.strftime('%Y-%m-%d'),
                        'produit': produit_vente,
                        'quantite': quantite_vente,
                        'montant': montant_vente,
                        'client': client_vente
                    }
                    df_ventes = enregistrer_vente(df_ventes, nouvelle_vente)
                    if sauvegarder_donnees(df_ventes, DATA_FILES['ventes']):
                        df_stock = maj_stock(df_stock, {'produit': produit_vente, 'quantite': quantite_vente, 'type': 'sortie'})
                        sauvegarder_stock(df_stock, DATA_FILES['stock'])
                        enregistrer_log('ajout_vente', f"{quantite_vente} x {produit_vente} pour {montant_vente} FCFA")
                        st.success('✅ Vente enregistrée avec succès!')
                        st.rerun()


# ==========================
# TAB 4: STOCK
# ==========================
with tab4:
    st.header('📦 Suivi du stock')
    
    tab_stock1, tab_stock2 = st.tabs(['📋 Données', '⚙️ Modifier'])
    
    with tab_stock1:
        if not df_stock.empty:
            st.subheader('État du stock')
            st.dataframe(df_stock, use_container_width=True)
            
            # Statistiques
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric('Produits en stock', len(df_stock))
            with col_stat2:
                st.metric('Valeur totale', f"{df_stock['quantite'].sum() if 'quantite' in df_stock.columns else 0:.0f} unités")
        else:
            st.info('Aucun stock enregistré pour le moment.')
    
    with tab_stock2:
        st.subheader('Mettre à jour le stock')
        with st.form('form_stock'):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                produit_stock = st.text_input('📦 Produit', key='stock_produit', placeholder='Ex: Riz')
                type_mouvement = st.selectbox('Type de mouvement', ['📥 Entrée', '📤 Sortie'])
            
            with col_form2:
                quantite_stock = st.number_input('📊 Quantité', min_value=1, value=1, key='stock_quantite')
            
            appliquer_btn = st.form_submit_button('✅ Appliquer le mouvement', use_container_width=True)
            
            if appliquer_btn:
                if not produit_stock or quantite_stock <= 0:
                    st.error('❌ Veuillez remplir tous les champs correctement')
                else:
                    type_mvt = type_mouvement.split()[-1].lower()
                    df_stock = maj_stock(df_stock, {'produit': produit_stock, 'quantite': quantite_stock, 'type': type_mvt})
                    if sauvegarder_stock(df_stock, DATA_FILES['stock']):
                        enregistrer_log('maj_stock', f"{type_mvt} de {quantite_stock} sur {produit_stock}")
                        st.success(f'✅ Stock mis à jour!')
                        st.rerun()


# ==========================
# TAB 5: BILAN
# ==========================
with tab5:
    st.header('📈 Bilan comptable détaillé')
    
    # KPIs résumé
    recettes_total, depenses_total, resultat_total = afficher_kpis(df_achats, df_ventes)
    
    st.markdown('---')
    
    # Tabs du bilan
    tab_bilan1, tab_bilan2, tab_bilan3 = st.tabs(['📊 Vue d\'ensemble', '🏭 Analyse des achats', '👥 Analyse des ventes'])
    
    with tab_bilan1:
        st.subheader('Vue d\'ensemble')
        
        col_overview1, col_overview2 = st.columns(2)
        
        with col_overview1:
            if not df_achats.empty and not df_ventes.empty:
                fig_overview = go.Figure(data=[
                    go.Bar(name='Dépenses', x=['Résumé'], y=[depenses_total]),
                    go.Bar(name='Recettes', x=['Résumé'], y=[recettes_total])
                ])
                fig_overview.update_layout(title='Recettes vs Dépenses', height=400)
                st.plotly_chart(fig_overview, use_container_width=True)
        
        with col_overview2:
            if recettes_total > 0:
                fig_marge = go.Figure(data=[
                    go.Pie(labels=['Profit', 'Dépenses'], values=[resultat_total, depenses_total])
                ])
                fig_marge.update_layout(title='Distribution du budget', height=400)
                st.plotly_chart(fig_marge, use_container_width=True)
        
        # Dataframes détaillés
        col_detail1, col_detail2 = st.columns(2)
        
        with col_detail1:
            st.subheader('📋 Détails des achats')
            if not df_achats.empty:
                st.dataframe(df_achats, use_container_width=True)
            else:
                st.info('Aucun achat enregistré')
        
        with col_detail2:
            st.subheader('📋 Détails des ventes')
            if not df_ventes.empty:
                st.dataframe(df_ventes, use_container_width=True)
            else:
                st.info('Aucune vente enregistrée')
    
    with tab_bilan2:
        st.subheader('🏭 Analyse des achats')
        
        if not df_achats.empty:
            col_analyse1, col_analyse2 = st.columns(2)
            
            with col_analyse1:
                fig_produits = create_bar_chart(df_achats, 'produit', 'montant', 
                                               '📦 Montant des achats par produit')
                if fig_produits:
                    st.plotly_chart(fig_produits, use_container_width=True)
            
            with col_analyse2:
                fig_fournisseurs = create_pie_chart(df_achats, 'fournisseur', 'montant',
                                                    '🏭 Distribution par fournisseur')
                if fig_fournisseurs:
                    st.plotly_chart(fig_fournisseurs, use_container_width=True)
            
            # Statistiques détaillées
            st.subheader('Statistiques')
            col_stat_a1, col_stat_a2, col_stat_a3, col_stat_a4 = st.columns(4)
            with col_stat_a1:
                st.metric('Montant total', f"{df_achats['montant'].sum():.0f} FCFA")
            with col_stat_a2:
                st.metric('Montant moyen', f"{df_achats['montant'].mean():.0f} FCFA")
            with col_stat_a3:
                st.metric('Quantité totale', int(df_achats['quantite'].sum()) if 'quantite' in df_achats.columns else 0)
            with col_stat_a4:
                st.metric('Fournisseurs uniques', df_achats['fournisseur'].nunique())
        else:
            st.info('Aucun achat enregistré pour l\'analyse')
    
    with tab_bilan3:
        st.subheader('👥 Analyse des ventes')
        
        if not df_ventes.empty:
            col_analyse1, col_analyse2 = st.columns(2)
            
            with col_analyse1:
                fig_produits_v = create_bar_chart(df_ventes, 'produit', 'montant',
                                                 '📦 Montant des ventes par produit')
                if fig_produits_v:
                    st.plotly_chart(fig_produits_v, use_container_width=True)
            
            with col_analyse2:
                fig_clients = create_pie_chart(df_ventes, 'client', 'montant',
                                              '👥 Distribution par client')
                if fig_clients:
                    st.plotly_chart(fig_clients, use_container_width=True)
            
            # Statistiques détaillées
            st.subheader('Statistiques')
            col_stat_v1, col_stat_v2, col_stat_v3, col_stat_v4 = st.columns(4)
            with col_stat_v1:
                st.metric('Montant total', f"{df_ventes['montant'].sum():.0f} FCFA")
            with col_stat_v2:
                st.metric('Montant moyen', f"{df_ventes['montant'].mean():.0f} FCFA")
            with col_stat_v3:
                st.metric('Quantité totale', int(df_ventes['quantite'].sum()) if 'quantite' in df_ventes.columns else 0)
            with col_stat_v4:
                st.metric('Clients uniques', df_ventes['client'].nunique())
        else:
            st.info('Aucune vente enregistrée pour l\'analyse')

# Footer
st.markdown('---')
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    💼 Plateforme de gestion et comptabilité | Version améliorée
    </div>
    """, unsafe_allow_html=True)
