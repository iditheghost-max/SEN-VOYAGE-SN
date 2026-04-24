import streamlit as st
import pandas as pd
import os

# Configuration
st.set_page_config(page_title="Global Travel Business", page_icon="🌍", layout="wide")

# 🌐 Gestion des langues
if 'lang' not in st.session_state:
    st.session_state.lang = 'Français'

# Sidebar - Langue
with st.sidebar:
    st.session_state.lang = st.selectbox(
        "🌐 Langue / Language",
        ["Français", "English", "Español", "العربية"]
    )

# Traductions
translations = {
    "Français": {
        "destinations": "Destinations phares",
        "offers": "Offres spéciales",
        "reservation": "Réservation en ligne",
        "full_name": "Nom complet",
        "email": "Adresse e-mail",
        "destination": "Destination",
        "message": "Message",
        "book": "Réserver",
        "thanks": "Merci",
        "reserved": "Votre demande a bien été enregistrée.",
        "contact_soon": "Nous vous contacterons sous peu.",
        "reservations_list": "Liste des réservations",
        "no_reservations": "Aucune réservation enregistrée.",
        "management": "Gestion & Comptabilité",
        "income": "Revenus",
        "expenses": "Dépenses",
        "clients": "Clients",
        "reports": "Rapports",
        "add_income": "Ajouter un revenu",
        "add_expense": "Ajouter une dépense",
        "add_client": "Ajouter le client",
        "date": "Date",
        "description": "Description",
        "amount": "Montant (FCFA)",
        "category": "Catégorie",
        "total_income": "Total des revenus",
        "total_expenses": "Total des dépenses",
        "net_profit": "Bénéfice Net",
        "export": "Exporter les données",
        "download": "Télécharger",
        "contact": "Contactez-nous sur WhatsApp | Suivez-nous sur Instagram",
        "patrimoine": "Patrimoine historique et culturel",
        "aventure": "Aventure et nature sauvage",
        "romance": "Romance et culture européenne",
        "promo": "Profitez de ces offres limitées en réservant dès maintenant !",
        "duration": "Durée",
        "days": "jours",
        "price": "Prix"
    },
    "English": {
        "destinations": "Top Destinations",
        "offers": "Special Offers",
        "reservation": "Online Reservation",
        "full_name": "Full Name",
        "email": "Email Address",
        "destination": "Destination",
        "message": "Message",
        "book": "Book Now",
        "thanks": "Thank you",
        "reserved": "Your request has been recorded.",
        "contact_soon": "We will contact you soon.",
        "reservations_list": "Reservations List",
        "no_reservations": "No reservations yet.",
        "management": "Management & Accounting",
        "income": "Income",
        "expenses": "Expenses",
        "clients": "Clients",
        "reports": "Reports",
        "add_income": "Add Income",
        "add_expense": "Add Expense",
        "add_client": "Add Client",
        "date": "Date",
        "description": "Description",
        "amount": "Amount (FCFA)",
        "category": "Category",
        "total_income": "Total Income",
        "total_expenses": "Total Expenses",
        "net_profit": "Net Profit",
        "export": "Export Data",
        "download": "Download",
        "contact": "Contact us on WhatsApp | Follow us on Instagram",
        "patrimoine": "Historical and cultural heritage",
        "aventure": "Adventure and wild nature",
        "romance": "Romance and European culture",
        "promo": "Take advantage of these limited offers by booking now!",
        "duration": "Duration",
        "days": "days",
        "price": "Price"
    },
    "Español": {
        "destinations": "Destinos Principales",
        "offers": "Ofertas Especiales",
        "reservation": "Reserva en Línea",
        "full_name": "Nombre Completo",
        "email": "Correo Electrónico",
        "destination": "Destino",
        "message": "Mensaje",
        "book": "Reservar",
        "thanks": "Gracias",
        "reserved": "Su solicitud ha sido registrada.",
        "contact_soon": "Le contactaremos pronto.",
        "reservations_list": "Lista de Reservas",
        "no_reservations": "No hay reservas registradas.",
        "management": "Gestión y Contabilidad",
        "income": "Ingresos",
        "expenses": "Gastos",
        "clients": "Clientes",
        "reports": "Informes",
        "add_income": "Agregar Ingreso",
        "add_expense": "Agregar Gasto",
        "add_client": "Agregar Cliente",
        "date": "Fecha",
        "description": "Descripción",
        "amount": "Monto (FCFA)",
        "category": "Categoría",
        "total_income": "Ingresos Totales",
        "total_expenses": "Gastos Totales",
        "net_profit": "Beneficio Neto",
        "export": "Exportar Datos",
        "download": "Descargar",
        "contact": "Contáctenos en WhatsApp | Síguenos en Instagram",
        "patrimoine": "Patrimonio histórico y cultural",
        "aventure": "Aventura y naturaleza salvaje",
        "romance": "Romance y cultura europea",
        "promo": "¡Aproveche estas ofertas limitadas reservando ahora!",
        "duration": "Duración",
        "days": "días",
        "price": "Precio"
    },
    "العربية": {
        "destinations": "أفضل الوجهات",
        "offers": "عروض خاصة",
        "reservation": "الحجز عبر الإنترنت",
        "full_name": "الاسم الكامل",
        "email": "البريد الإلكتروني",
        "destination": "الوجهة",
        "message": "الرسالة",
        "book": "احجز الآن",
        "thanks": "شكراً لك",
        "reserved": "تم تسجيل طلبك بنجاح.",
        "contact_soon": "سنقوم بالاتصال بك قريباً.",
        "reservations_list": "قائمة الحجوزات",
        "no_reservations": "لا توجد حجوزات مسجلة.",
        "management": "الإدارة والمحاسبة",
        "income": "الإيرادات",
        "expenses": "المصروفات",
        "clients": "العملاء",
        "reports": "التقارير",
        "add_income": "إضافة إيراد",
        "add_expense": "إضافة مصروف",
        "add_client": "إضافة عميل",
        "date": "التاريخ",
        "description": "الوصف",
        "amount": "المبلغ (ف CFA)",
        "category": "الفئة",
        "total_income": "إجمالي الإيرادات",
        "total_expenses": "إجمالي المصروفات",
        "net_profit": "صافي الربح",
        "export": "تصدير البيانات",
        "download": "تحميل",
        "contact": "اتصل بنا على واتساب | تابعنا على إنستغرام",
        "patrimoine": "التراث التاريخي والثقافي",
        "aventure": "المغامرة والطبيعة البرية",
        "romance": "الرومانسية والثقافة الأوروبية",
        "promo": "استفد من هذه العروض المحدودة بالحجز الآن!",
        "duration": "المدة",
        "days": "أيام",
        "price": "السعر"
    }
}

t = translations[st.session_state.lang]

# 🎨 Style voyage & détente
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
.stApp {
    background: linear-gradient(180deg, #E8F4FD 0%, #B8E0F0 50%, #87CEEB 100%);
    color: #1A365D;
    font-family: 'Poppins', sans-serif;
}
/* Header professionnel */
.header-container {
    background: linear-gradient(135deg, #0077B6 0%, #00B4D8 50%, #90E0EF 100%);
    padding: 30px;
    border-radius: 15px;
    border: 2px solid #FFFFFF;
    box-shadow: 0 10px 30px rgba(0,119,182,0.3);
    margin-bottom: 20px;
}
.header-title {
    font-size: 48px;
    font-weight: 700;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
.header-subtitle {
    font-size: 18px;
    color: #FFFFFF;
    text-align: center;
    letter-spacing: 3px;
    font-weight: 500;
}
.header-slogan {
    font-size: 20px;
    color: #FFD700;
    text-align: center;
    font-style: italic;
    margin-top: 10px;
    font-weight: 600;
}
.header-contact {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 15px;
    font-size: 14px;
}
.header-contact span {
    color: #FFFFFF;
    background: rgba(255,255,255,0.2);
    padding: 5px 15px;
    border-radius: 20px;
}
.card {
    background: linear-gradient(145deg, #FFFFFF 0%, #E8F4FD 100%);
    border: 2px solid #00B4D8;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    color: #1A365D;
    box-shadow: 0 8px 20px rgba(0,119,182,0.15);
    transition: all 0.4s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,180,216,0.3);
    border-color: #0077B6;
}
.card img {
    border-radius: 10px;
    width: 100%;
    height: 200px;
    object-fit: cover;
}
hr {
    border: 2px solid #00B4D8;
    margin: 20px 0;
}
.section-title {
    font-size: 28px;
    font-weight: 600;
    color: #0077B6;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 3px solid #00B4D8;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🛫 Header professionnel
st.markdown("""
<div class="header-container">
    <div class="header-title">🌍 Global Travel Business</div>
    <div class="header-subtitle">AGENCE DE VOYAGES INTERNATIONALE</div>
    <div class="header-slogan">Votre Satisfaction, Notre Devoir</div>
    <div class="header-contact">
        <span>📞 +221 77 123 45 67</span>
        <span>✉️ contact@globaltravel.com</span>
        <span>📍 Dakar, Sénégal</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 📍 Destinations
st.markdown(f"## ✨ {t['destinations']}")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://copilot.microsoft.com/th/id/BCO.96665664-85f0-4896-b229-8cde6dd9572c.png", caption="Île de Gorée - Sénégal")
    st.write(t['patrimoine'])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://copilot.microsoft.com/th/id/BCO.65cc51bf-567d-434e-a9ad-27ef44b7553f.png", caption="Safari au Kenya")
    st.write(t['aventure'])
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://copilot.microsoft.com/th/id/BCO.d4e22f58-5b28-4ef3-a466-b2250dc188cf.png", caption="Paris - France")
    st.write(t['romance'])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 🎁 Offres spéciales harmonisées
st.markdown("## 🎁 Offres spéciales")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1586861203927-800a5acdcc4d?w=400", caption="Zanzibar - Tanzanie", width="stretch")
    st.markdown("<h3 style='color:#0077B6;'>Durée : 4 jours</h3>", unsafe_allow_html=True)
    st.markdown("<p>Prix : <b>350 000 FCFA</b> — <span style='color:#00FF00;'>-10% Promo</span></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=400", caption="Marrakech - Maroc", width="stretch")
    st.markdown("<h3 style='color:#0077B6;'>Durée : 3 jours</h3>", unsafe_allow_html=True)
    st.markdown("<p>Prix : <b>280 000 FCFA</b> — <span style='color:#FF5733;'>-15% Promo</span></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400", caption="Bali - Indonésie", width="stretch")
    st.markdown("<h3 style='color:#0077B6;'>Durée : 6 jours</h3>", unsafe_allow_html=True)
    st.markdown("<p>Prix : <b>520 000 FCFA</b> — <span style='color:#3498DB;'>-5% Promo</span></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.info("✨ Profitez de ces offres limitées en réservant dès maintenant !")

# 📝 Formulaire de réservation (dans la barre latérale)
st.sidebar.markdown("## 📝 Réservation en ligne")
with st.sidebar.form("reservation_form"):
    nom = st.text_input("Nom complet")
    email = st.text_input("Adresse e-mail")
    destination = st.selectbox("Destination", ["Île de Gorée - Sénégal", "Safari au Kenya", "Paris - France"])
    message = st.text_area("Message")
    envoyer = st.form_submit_button("Réserver")

    if envoyer:
        reservation = {"Nom": nom, "Email": email, "Destination": destination, "Message": message}
        fichier = "reservations.csv"

        if os.path.exists(fichier):
            df = pd.read_csv(fichier)
            df = pd.concat([df, pd.DataFrame([reservation])], ignore_index=True)
        else:
            df = pd.DataFrame([reservation])

        df.to_csv(fichier, index=False)
        st.success(f"Merci {nom} !")

st.markdown("<hr>", unsafe_allow_html=True)

# 📋 Liste des réservations (sans graphique)
st.markdown("## 📋 Liste des réservations")
fichier = "reservations.csv"
if os.path.exists(fichier):
    df = pd.read_csv(fichier)
    st.dataframe(df)
else:
    st.warning("⚠️ Aucune réservation enregistrée pour le moment.")

# 📊 Section Gestion et Comptabilité
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Gestion & Comptabilité")

# Onglets pour les différentes fonctionnalités
onglet1, onglet2, onglet3, onglet4 = st.tabs(["💰 Revenus", "📤 Dépenses", "👥 Clients", "📈 Rapports"])

# 💰 Gestion des revenus
with onglet1:
    st.markdown("### 💰 Suivi des revenus")
    
    with st.form("ajout_revenu"):
        date_rev = st.date_input("Date")
        description_rev = st.text_input("Description")
        montant_rev = st.number_input("Montant (FCFA)", min_value=0, step=1000)
        valider_rev = st.form_submit_button("Ajouter un revenu")
        
        if valider_rev and description_rev and montant_rev > 0:
            revenu = {"Date": str(date_rev), "Description": description_rev, "Montant": montant_rev, "Type": "Revenu"}
            fichier_rev = "revenus.csv"
            if os.path.exists(fichier_rev):
                df_rev = pd.read_csv(fichier_rev)
                df_rev = pd.concat([df_rev, pd.DataFrame([revenu])], ignore_index=True)
            else:
                df_rev = pd.DataFrame([revenu])
            df_rev.to_csv(fichier_rev, index=False)
            st.success("Revenu ajouté avec succès !")
    
    # Afficher les revenus
    fichier_rev = "revenus.csv"
    if os.path.exists(fichier_rev):
        df_rev = pd.read_csv(fichier_rev)
        st.dataframe(df_rev)
        total_rev = df_rev["Montant"].sum()
        st.metric("Total des revenus", f"{total_rev:,} FCFA")
    else:
        st.info("Aucun revenu enregistré.")

# 📤 Gestion des dépenses
with onglet2:
    st.markdown("### 📤 Suivi des dépenses")
    
    with st.form("ajout_depense"):
        date_dep = st.date_input("Date", key="date_dep")
        description_dep = st.text_input("Description", key="desc_dep")
        montant_dep = st.number_input("Montant (FCFA)", min_value=0, step=1000, key="mont_dep")
        categorie = st.selectbox("Catégorie", ["Transport", "Hébergement", "Marketing", "Salaires", "Fournitures", "Autre"])
        valider_dep = st.form_submit_button("Ajouter une dépense")
        
        if valider_dep and description_dep and montant_dep > 0:
            depense = {"Date": str(date_dep), "Description": description_dep, "Montant": montant_dep, "Catégorie": categorie, "Type": "Dépense"}
            fichier_dep = "depenses.csv"
            if os.path.exists(fichier_dep):
                df_dep = pd.read_csv(fichier_dep)
                df_dep = pd.concat([df_dep, pd.DataFrame([depense])], ignore_index=True)
            else:
                df_dep = pd.DataFrame([depense])
            df_dep.to_csv(fichier_dep, index=False)
            st.success("Dépense ajoutée avec succès !")
    
    # Afficher les dépenses
    fichier_dep = "depenses.csv"
    if os.path.exists(fichier_dep):
        df_dep = pd.read_csv(fichier_dep)
        st.dataframe(df_dep)
        total_dep = df_dep["Montant"].sum()
        st.metric("Total des dépenses", f"{total_dep:,} FCFA")
    else:
        st.info("Aucune dépense enregistrée.")

# 👥 Gestion des clients
with onglet3:
    st.markdown("### 👥 Gestion des clients")
    
    with st.form("ajout_client"):
        nom_client = st.text_input("Nom du client")
        email_client = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        adresse = st.text_input("Adresse")
        valider_client = st.form_submit_button("Ajouter le client")
        
        if valider_client and nom_client:
            client = {"Nom": nom_client, "Email": email_client, "Téléphone": telephone, "Adresse": adresse}
            fichier_clients = "clients.csv"
            if os.path.exists(fichier_clients):
                df_clients = pd.read_csv(fichier_clients)
                df_clients = pd.concat([df_clients, pd.DataFrame([client])], ignore_index=True)
            else:
                df_clients = pd.DataFrame([client])
            df_clients.to_csv(fichier_clients, index=False)
            st.success("Client ajouté avec succès !")
    
    # Afficher les clients
    fichier_clients = "clients.csv"
    if os.path.exists(fichier_clients):
        df_clients = pd.read_csv(fichier_clients)
        st.dataframe(df_clients)
        st.metric("Nombre de clients", len(df_clients))
    else:
        st.info("Aucun client enregistré.")

# 📈 Rapports financiers
with onglet4:
    st.markdown("### 📈 Rapports financiers")
    
    # Calculer les totaux
    total_rev = 0
    total_dep = 0
    
    if os.path.exists("revenus.csv"):
        df_rev = pd.read_csv("revenus.csv")
        total_rev = df_rev["Montant"].sum()
    
    if os.path.exists("depenses.csv"):
        df_dep = pd.read_csv("depenses.csv")
        total_dep = df_dep["Montant"].sum()
    
    benefice = total_rev - total_dep
    
    # Afficher les KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenus", f"{total_rev:,} FCFA", delta_color="normal")
    with col2:
        st.metric("Total Dépenses", f"{total_dep:,} FCFA", delta_color="inverse")
    with col3:
        st.metric("Bénéfice Net", f"{benefice:,} FCFA", delta_color="normal" if benefice >= 0 else "inverse")
    
    # Graphique simple
    if total_rev > 0 or total_dep > 0:
        st.markdown("#### 📊 Répartition Revenus vs Dépenses")
        data = pd.DataFrame({
            "Type": ["Revenus", "Dépenses"],
            "Montant": [total_rev, total_dep]
        })
        st.bar_chart(data.set_index("Type"))
    
    # Export des données
    st.markdown("### 📥 Exporter les données")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("revenus.csv"):
            df_rev = pd.read_csv("revenus.csv")
            csv_rev = df_rev.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Télécharger revenus.csv", csv_rev, "revenus.csv", "text/csv")
    with col2:
        if os.path.exists("depenses.csv"):
            df_dep = pd.read_csv("depenses.csv")
            csv_dep = df_dep.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Télécharger depenses.csv", csv_dep, "depenses.csv", "text/csv")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>📞 Contactez-nous sur WhatsApp | 🌐 Suivez-nous sur Instagram</p>", unsafe_allow_html=True)
