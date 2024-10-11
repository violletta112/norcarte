import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

st.set_page_config(
    page_title="Emplacement Agences",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Créer des colonnes pour centrer l'image
col1, col2, col3 = st.columns([1, 2, 3])

# Afficher l'image dans la colonne centrale
with col2:
    st.image("https://bnh.dz/img/logo13.png", width=400)

st.title("Déploiement des agences de BNH")

options = ['choisir une année', '2024', '2025', '2026']
optionn = ['aucun choix', 'directeur oui', 'directeur non']
WILAYAS = ['choisir une wilaya', 'ADRAR', 'ALGER', 'BOUIRA', 'BLIDA', 'MEDIA']

# Créer une carte Folium
m = folium.Map([35.7950980697429, 3.1787263226179263], zoom_start=6)

# Afficher la carte et les options dans la colonne de gauche
col1, col2 = st.columns([3, 2])

with col1:
    choice = st.selectbox('Choisir une option:', options)
    
    if st.button('Refresh'):
        st.write(f"Recherche en cours pour : {choice}")

    # Charger les données en fonction de l'option sélectionnée
    try:
        if choice == '2024':
            df = pd.read_excel('carte.graphique.xlsx')
        elif choice == '2025':
            df = pd.read_excel('carte.graphique2.xlsx')
        elif choice == '2026':
            df = pd.read_excel('carte.graphique3.xlsx')
        else:
            df = pd.DataFrame()  # Empty DataFrame if no valid choice

        # Ajouter des marqueurs à la carte Folium
        for index, row in df.iterrows():
            folium.CircleMarker(
                [row['latitude'], row['longitude']],
                radius=10,
                color='yellow',
                fill=True,
                fill_color='red'
            ).add_to(m)
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=f"<b>Emplacement:</b> {row['name']}, <br><b>Latitude:</b> {row['latitude']}, <br><b>Longitude:</b> {row['longitude']}"
            ).add_to(m)

    except FileNotFoundError as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")

with col2:
    choix = st.selectbox('Choisir une option:', optionn)

    # Filtrer et afficher les données selon le choix
    if choix != 'aucun choix':
        try:
            df_filtered = df[df.iloc[:, 3].str.strip() == ('oui' if choix == 'directeur oui' else 'non')]
            for index, row in df_filtered.iterrows():
                color = 'green' if choix == 'directeur oui' else 'red'
                folium.CircleMarker(
                    [row['latitude'], row['longitude']],
                    radius=10,
                    color=color,
                    fill=True,
                    fill_color=color
                ).add_to(m)
                folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=f"<b>Emplacement:</b> {row['name']}, <br><b>Latitude:</b> {row['latitude']}, <br><b>Longitude:</b> {row['longitude']}"
                ).add_to(m)

            st.write("Données filtrées:")
            st.write(df_filtered.iloc[:, [0, 3]])
        except Exception as e:
            st.error(f"Erreur lors du filtrage des données : {e}")

# Afficher la carte
folium_static(m, width=600, height=300)

# Gestion des wilayas
choisir = st.selectbox('Choisir une wilaya', WILAYAS, key='wilaya_choice')

if choisir != 'choisir une wilaya':
    try:
        df_wilaya = pd.read_excel('recapitulation.alger.xlsx', sheet_name=choisir.strip())
        st.write(df_wilaya)

        total1 = df_wilaya.iloc[:6, 2].sum()
        total2 = df_wilaya.iloc[6:, 2].sum()
        total_ht = df_wilaya.iloc[:, 1].sum()

        st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
        st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
        st.write(f"Le taux total est : {total1 + total2:.4f}")
        st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")
else:
    st.write("Veuillez sélectionner une WILAYA pour afficher les données.")