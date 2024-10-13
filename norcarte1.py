import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Create columns for centering the image
col1, col2, col3 = st.columns([1, 2, 3])
options = ['Choisir une année', '2024', '2025', '2026']
optionn = ['Aucun choix', 'Avec directeur', 'Sans directeur']
WILAYAS = ['choisir une wilaya', 'ALGER', 'CONSTANTINE', 'ORAN', 'BISKRA', 'SÉTIF', 'CHLEF','BECHAR']

# Display the image in the central column
with col2:
    st.image("https://bnh.dz/img/logo13.png", width=400)
    st.title("Déploiement des agences de BNH")


    st.set_page_config(
          page_title="Emplacement Agences",
          page_icon="🌍",
          layout="wide",
          initial_sidebar_state="expanded"
           )

# Create a Folium map
m = folium.Map([35.7950980697429, 3.1787263226179263], zoom_start=6)

# Display the options in the left column
col1, col2 = st.columns([2, 3])  # Adjusted column widths for better layout

with col1:
    st.info('Sélectionner une année pour voir les agences existantes')
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

        # Clean column names
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

# Right column for displaying the map and options based on director presence

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

# Handle wilayas selection
choisir = st.selectbox('Choisir une wilaya', WILAYAS, key='wilaya_choice')

if choisir != 'choisir une wilaya':
    if choisir == 'ALGER':
        st.markdown("""La wilaya d'Alger contient deux agences : <span style='color:red;'><strong>Bab Ezzouar</strong></span> et <span style='color:red;'><strong>El Achour</strong></span>. Vous pouvez sélectionner un fichier pour calculer les taux.
                      """, unsafe_allow_html=True)

        # File uploader for Excel file
        uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])
    
        if uploaded_file is not None:
            # Load the uploaded Excel file
            df_uploaded = pd.read_excel(uploaded_file)
            st.write(df_uploaded)  # Display first few rows of the DataFrame
        
            try:
                total1 = df_uploaded.iloc[:6, 2].sum()
                total2 = df_uploaded.iloc[6:, 2].sum()
                total_ht = df_uploaded.iloc[:, 1].sum()
                st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
                st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
                total_total = total1 + total2           
                st.write(f"Le taux total est : {total_total:.4f}")
                st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
            except Exception as e:
                st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")
       
    else:
        if choisir == 'CONSTANTINE':
            uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])
    
            if uploaded_file is not None:
                # Load the uploaded Excel file
                df_uploaded = pd.read_excel(uploaded_file)
        
                try:
                    total1 = df_uploaded.iloc[:6, 2].sum()
                    total2 = df_uploaded.iloc[6:, 2].sum()
                    total_ht = df_uploaded.iloc[:, 1].sum()

                    st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
                    st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
                    total_total = total1 + total2
                    st.write(f"Le taux total est : {total_total:.4f}")
                    st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
                except Exception as e:
                    st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")

        if choisir == 'ORAN':
            uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])
    
            if uploaded_file is not None:
                # Load the uploaded Excel file
                df_uploaded = pd.read_excel(uploaded_file)
        
                try:
                    total1 = df_uploaded.iloc[:6, 2].sum()
                    total2 = df_uploaded.iloc[6:, 2].sum()
                    total_ht = df_uploaded.iloc[:, 1].sum()

                    st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
                    st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
                    total_total = total1 + total2
                    st.write(f"Le taux total est : {total_total:.4f}")
                    st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
                except Exception as e:
                    st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")

# Display the map with st_folium in the right column
with col3:
    # Afficher la carte avec st_folium
    st_folium(m, width=700, height=400)
