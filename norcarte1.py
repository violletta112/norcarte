import streamlit as st
import pandas as pd
import folium
import os
from streamlit_folium import st_folium
from io import BytesIO

st.set_page_config(
    page_title="Emplacement Agences",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create columns to center the image
col1, col2, col3 = st.columns([1, 2, 3])

# Display the image in the central column
with col2:
    st.image("https://bnh.dz/img/logo13.png", width=400)

st.title("Déploiement des agences de BNH")

options = ['Choisir une année', '2024', '2025', '2026']
optionn = ['Aucun choix', 'Avec directeur', 'Sans directeur']
WILAYAS = ['Choisir une wilaya', 'ALGER', 'CONSTANTINE', 'ORAN', 'BISKRA', 'SÉTIF', 'CHLEF', 'BECHAR']

# Create a Folium map
m = folium.Map([35.7950980697429, 3.1787263226179263], zoom_start=6)

# Display the map in the left column
col1, col2 = st.columns([3, 2])

with col1:
    choice = st.selectbox('Choisir une option:', options)

    if st.button('Refresh'):
        st.write(f"Recherche en cours pour : {choice}")

    # Load data based on selected option
    try:
        if choice == '2024':
            df = pd.read_excel('carte.graphique.xlsx')
        elif choice == '2025':
            df = pd.read_excel('carte.graphique2.xlsx')
        else:
            df = pd.read_excel('carte.graphique3.xlsx')

        df.columns = df.columns.str.strip()

        # Add yellow markers to the Folium map
        for index, row in df.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']],
                                radius=10,
                                color='yellow',
                                fill=True,
                                fill_color='red').add_to(m)
            folium.Marker([row['latitude'], row['longitude']],
                          popup=f"<b>Emplacement:</b> {row['name']}, <br><b>Latitude:</b> {row['latitude']}, <br><b>Longitude:</b> {row['longitude']}").add_to(m)

    except FileNotFoundError as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
    except KeyError as e:
        st.error(f"Erreur : La colonne {e} n'existe pas dans le DataFrame.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")

# Display the table in the right column
with col2:
    choix = st.selectbox('Choisir une option:', optionn)

    if choix != 'Aucun choix':
        try:
            df_filtered = df[df.iloc[:, 3].str.strip() == ('oui' if choix == 'Avec directeur' else 'non')]
            for index, row in df_filtered.iterrows():
                color = 'green' if choix == 'Avec directeur' else 'red'
                folium.CircleMarker([row['latitude'], row['longitude']],
                                    radius=10,
                                    color=color,
                                    fill=True,
                                    fill_color=color).add_to(m)
                folium.Marker([row['latitude'], row['longitude']],
                              popup=f"<b>Emplacement:</b> {row['name']}, <br><b>Latitude:</b> {row['latitude']}, <br><b>Longitude:</b> {row['longitude']}").add_to(m)

            st.write("Données filtrées:")
            st.write(df_filtered.iloc[:, [0, 3]])
        except Exception as e:
            st.error(f"Erreur lors du filtrage des données : {e}")

# Manage wilayas (similar to your original code)
choisir = st.selectbox('Choisir une wilaya', WILAYAS, key='wilaya_choice')

if choisir == 'ALGER':
    # Show additional options when ALGER is selected
    additional_options = ['bbz', 'achour']
    selected_additional_option = st.selectbox('Choisir une option supplémentaire:', additional_options)
    
    # Logic for uploading Excel file based on selection
    if selected_additional_option in ['bbz', 'achour']:
        # Show file uploader after selecting bbz or achour
        file_path = st.file_uploader("Télécharger le fichier Excel", type="xlsx")

        if file_path is not None:
            try:
                df_upload = pd.read_excel(file_path)
                
                # Create an Excel file in memory for download
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_upload.to_excel(writer, index=False, sheet_name=selected_additional_option)
                
                output.seek(0)  # Move to the beginning of the BytesIO buffer
                
                # Provide a download button for the corresponding file
                st.download_button(
                    label=f"Télécharger le fichier pour {selected_additional_option}",
                    data=output.getvalue(),
                    file_name=f"{selected_additional_option}_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier Excel : {e}")

elif choisir != 'Choisir une wilaya':
    try:
        df_wilaya = pd.read_excel('recapitulation.alger.xlsx', sheet_name=choisir.strip())
        st.write(df_wilaya)

        total1 = df_wilaya.iloc[:6, 2].sum()
        total2 = df_wilaya.iloc[6:, 2].sum()
        total_ht = df_wilaya.iloc[:, 1].sum()

        st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
        st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
        total_total = total1 + total2
        st.write(f"Le taux total est : {total_total:.4f}")
        st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")
else:
    st.write("Veuillez sélectionner une WILAYA pour afficher les données.")

# Display the map with st_folium
st_folium(m, width=600, height=300)
