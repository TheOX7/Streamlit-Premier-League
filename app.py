import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import math
import csv
import joblib
import sklearn
import pickle
from PIL import Image
from lorem_text import lorem
import os

st.set_page_config(
    page_title="Premier League 2022/23",
    layout='wide'
)

st.title('Premier League 2022/23 Summary')
url_editor = "https://www.linkedin.com/in/marselius-agus-dhion-374106226/"
st.markdown(f'Streamlit App by [Marselius Agus Dhion]({url_editor})', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['Summary Information', 'Player Stats', 'Club Stats', 'Predict Match Result'])

# Tab Pertama
with tab1 : 
    opening = lorem.paragraphs(2)
    opening_1 = "Musim Premier League 2022/2023 sudah berakhir dan telah memberikan beberapa hal-hal yang tidak terduga. Salah satu momen atau hal yang tidak terduga adalah ketika Arsenal mampu memberikan persaingan yang sengit kepada Manchester City dalam perebutan gelar juara Liga Inggris. Dimana Arsenal berhasil menduduki puncak klasemen Liga Inggris selama (…) pekan. Namun, Arsenal gagal dalam menjaga kekonsistenannya hingga akhir musim, beberapa alasannya seperti adanya cedera pada beberapa pemain kunci, dan kekonsistenan performa Manchester City ketika performa Arsenal sedang tidak konsisten. Pada akhirnya, Manchester City berhasil menduduki posisi pertama sampai dengan gamewwk terakhir. Tak hanya itu, kejutan lainnya datang dari tim yang ditangani oleh Eddie Howe, yaitu Newcastle United. Terakhir kali Newcastle berhasil masuk ke dalam top four adalah pada musim 2003/2024,  dimana pada saat itu Newcastle dipimpin oleh Alan Shearer sebagai captain tim tersebut, pada akhirnya Newcastle berhasil menduduki posisi keempat. Selain itu, Manchester United juga berhasil memastikan diri mereka mendapatkan tiket untuk bermain pada Liga Champions."
    opening_2_1 = "Selain Manchester City, Arsenal, Manchester City, dan Newcastle City yang berhasil mendapatkan jatah bermain pada Champions League untuk musim depan. Terdapat empat tim lainnya lagi yang berhasil mendapatkan jatah untuk bermain diluar Premier League. Pada posisi kelima dan keenam ditempati oleh Liverpool dan Brighton & Hove Albion, dimana kedua tim ini berhasil mendapatkan jatah untuk bermain di Europa League. Selain itu pada posisi ketujuh ditempati oleh Aston Villa, dimana Aston Villa dapat bermain pada Conference League untuk musim depan. Tim terakhir yang ‘surprisingly’ berhasil mendapatkan jatah bermain pada Europa League adalah West Ham. West Ham dapat bermain pada Europa League dikarenakan mereka berhasil menjuarai Conference League, setelah mengalahkan Fiorentina dengan skor 2-1."    
    opening_2_2 = "Selain ke-delapan tim tersebut yang berhasil bermain pada liga Eropa, terdapat dua tim yang kurang bermain baik pada musim ini, yaitu Tottenham dan Chelsea. Tottenham sendiri pada awal-awal musim konsisten berada dalam top four. Sedangkan Chelsea sendiri sudah menggelontorkan dana yang banyak, namun performa mereka kurang baik, salah satunya dikarenakan jumlah pemain yang terlalu banyak dan membuat tidak adanya line-up yang pasti bagi tim ini."
    opening_3 = "Setiap musimnya pasti terdapat tiga tim yang mengalami degradasi. Musim ini tiga tim tersebut adalah juara Premier League musim 2015/2016 yaitu Leicester City, Leeds United, dan Southampton. Pada gameweek ke-38 atau match terakhir terdapat empat tim yang mempunyai kemungkinan degradasi, satu tim lainnya adalah Everton. Everton sendiri dapat terhindar dari degradasi dikarenakan kemenangan mereka atas Bournemouth dengan skor 1-0, padahal saat itu juga Leicester memenangkan laga melawan West Ham dengan skor akhir 2-1. Namun pada akhirnya Leicester yang terdegradasi. Pada gameweek terakhir Southampton juga menjadi laga yang menarik, dikarenakan mereka imbang melawan Liverpool dengan skor yang cukup besar yaitu 4-4."
    justify_text = """
    <style>
    .text-justify {
        text-align: justify;
        text-justify: inter-word;
    }
    </style>
    """
    

    
    st.header('Premier League 2022/23 Overview')
    # Opening (Pemenangnya siapa, kedua, ketiga, keempat)
    col1_1, col1_2 = st.columns([3,1])
    with col1_1 : 
        st.markdown(justify_text, unsafe_allow_html=True)
        st.markdown(f'<div class="text-justify">{opening_1}</div>', unsafe_allow_html=True)
    with col1_2 :
        man_city_img = Image.open('man-city.jpeg')
        st.image(man_city_img, caption='Man City Players Lifting PL Trophy',  use_column_width=True)
    
    # Opening2 (Posisi ke-5,6,7, dan West Ham)
    col2_1, col2_2 = st.columns([1,3])
    with col2_1 : 
        west_ham_img = Image.open('west-ham-conf-league.jpeg')
        st.image(west_ham_img, caption='Declan Rice with Conference League Trophy', use_column_width=True)
    with col2_2 : 
        st.markdown(justify_text, unsafe_allow_html=True)
        st.markdown(f'<div class="text-justify">{opening_2_1}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="text-justify">{opening_2_2}</div>', unsafe_allow_html=True)
       
    col3_1, col3_2 = st.columns([3,1])
    with col3_1 : 
        st.markdown(justify_text, unsafe_allow_html=True)
        st.markdown(f'<div class="text-justify">{opening_3}</div>', unsafe_allow_html=True)
    with col3_2 :
        lei_city_img = Image.open('lei-relegated.jpg')
        st.image(lei_city_img, caption='Leicester City players after getting relegated', use_column_width=True)
    
    # Center the content
    # st.markdown('<div class="center-content"></div>', unsafe_allow_html=True)
    st.write('____________')

    # Membaca file CSV
    data = pd.read_csv('Position per Gameweek.csv')
    pl_standings = pd.read_csv('PL 22-23 Standings.csv', index_col=0)

    st.header('Final Standings')
    # Membuat fungsi untuk memberikan warna pada baris
    def highlight_row(row):
        if row.name in [1, 2, 3, 4]:
            return ['background-color: #2940D3'] * len(row)  # Light blue
        elif row.name in [5, 6]:
            return ['background-color: #DC5F00'] * len(row)  # Light orange
        elif row.name == 7:
            return ['background-color: #1C7947'] * len(row)  # Light green
        elif row.name >= 18:
            return ['background-color: #CF0A0A'] * len(row)  # Light red
        else:
            return [''] * len(row)
        
    # Menampilkan DataFrame dengan warna pada baris
    st.dataframe(pl_standings.drop('Image_club', axis=1).style.apply(highlight_row, axis=1), use_container_width=True)

    # Legend
    legend = {
        'Label': ['Champions League', 'Europa League', 'Conference League', 'Relegation'],
        'Warna': ['#2940D3', '#DC5F00', '#1C7947', '#CF0A0A']
    }

    df_legend = pd.DataFrame(legend)

    # Tampilkan legenda
    st.subheader('Legend : ')

    legenda_html = ""
    for i in range(len(df_legend)):
        label = df_legend.loc[i, 'Label']
        color = df_legend.loc[i, 'Warna']
        legenda_html += f'<span style="color:{color}">■</span> {label} &nbsp;&nbsp;'

    st.markdown(f'<div style="white-space: nowrap;">{legenda_html}</div>', unsafe_allow_html=True)
    
    # col1, col2 = st.columns([5, 2])
    st.write('________________')
    st.header('Performance Chart')

    # ====================================================== #
    with st.container() : 
        # Membuat select box untuk memilih klub
        clubs = data['Club'].unique()
        selected_clubs = st.multiselect('Choose Club (One or More Than One Club)', clubs)

        # Memfilter data berdasarkan klub yang dipilih
        club_data = data[data['Club'].isin(selected_clubs)]

        # Membuat line chart menggunakan Altair
        chart = alt.Chart(club_data).mark_line().encode(
            x=alt.X('Gameweek:Q', scale=alt.Scale(domain=[1, 38]), axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Position:Q', scale=alt.Scale(domain=[1, 20], reverse=True), title='Position'),
            color='Club:N',
            tooltip=['Gameweek', 'Position']
        ).properties(
            width=600,
            height=400,
            title='Position Changes'
        )

        # Menambahkan titik/dot pada setiap datapoint
        chart += alt.Chart(club_data).mark_circle(size=100).encode(
            x='Gameweek',
            y='Position',
            color='Club:N',
            tooltip=['Gameweek', 'Position']
        )

        # Mengatur langkah nilai pada sumbu y
        chart = chart.configure_axisY(
            tickMinStep=1
        )

        # Menampilkan line chart pada Streamlit
        st.altair_chart(chart, use_container_width=True)


             
    # ======== Dataframe list top players Start ======== #

# Tab Kedua
with tab2 :     
    st.markdown(
        """
        <style>
        .text-right {
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.header("Top Scorer")
    col_scorer, col_scorer_img = st.columns([2,1])

    st.markdown('<h2 class="text-right">Top Assist</h2>', unsafe_allow_html=True)
    col_assist_img, col_assist = st.columns([1,2])

    st.header("Top Clean Sheet")
    col_cleansheet, col_cleansheet_img = st.columns([2,1])

    df_top_assist = pd.read_csv('Top Asissts.csv', index_col=0)
    df_top_cleansheet = pd.read_csv('Top Clean Sheet.csv', index_col=0)
    df_top_scorer = pd.read_csv('Top Scorers.csv', index_col=0)

    # Players Image
    golden_boot_img = Image.open('golden-boot.jpg')
    golden_glove_img = Image.open('golden-glove.jpg')
    pots_img = Image.open('playmaker-of-the-season.jpg')

    # Polygon Plotting 
    def normalize_log(data):
        normalized_data = [math.log(x + 1) for x in data]  # Menggunakan logaritma natural dengan penambahan 1 untuk menghindari log(0)
        return normalized_data

    def plot_polygon_with_feature_values(selected_indices, feature_names, feature_values):
        n = len(selected_indices)  # Jumlah sisi poligon yang dipilih
        angles = [i * 360 / float(n) for i in range(n)]  # Menghitung sudut untuk setiap sisi dalam derajat

        # Normalisasi feature_values
        feature_values_normalized = normalize_log(feature_values)

        # Menambahkan satu elemen tambahan untuk memastikan kesimetrisan poligon
        feature_values_normalized += [feature_values_normalized[0]]
        feature_names += [feature_names[0]]
        angles += [angles[0] + 360]

        # Membuat plotly figure
        fig = go.Figure()

        # Menambahkan trace untuk poligon
        fig.add_trace(go.Scatterpolar(
            r=feature_values_normalized,
            theta=angles,
            fill='toself',
            fillcolor='rgba(0, 123, 255, 0.2)',
            line=dict(color='rgb(0, 123, 255)'),
            hovertemplate='Nilai (Normalized): %{r:.2f}<br>Nilai (Original): %{text}<extra></extra>',
            text=feature_values        
        ))

        # Mengatur tampilan sumbu sudut
        fig.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=False, ticks=''),
                angularaxis=dict(showticklabels=True, tickmode='array', tickvals=angles, ticktext=feature_names)
            ),
            title='Poligon dengan Fitur Pemain Bola',  # Judul plot
        )

        # Mengatur ukuran plot
        fig.update_layout(width=500, height=500)

        # Menampilkan plot menggunakan Streamlit
        st.plotly_chart(fig)

    with st.container(): 
        with col_scorer :
            st.dataframe(df_top_scorer, use_container_width=True)
                    
        with col_scorer_img :
            st.image(golden_boot_img, caption='Erling Braut Halaand')
            with st.expander('Player Stats') : 
                feature_names = ['Headed Goals', 'Goals with right foot', 'Goals with left foot', 'Penalties Scored', 'Shots accuracy (%)', 'Big chances missed']  # Nama-nama fitur
                feature_values = [7, 6, 23, 7, 49, 28]  # Nilai fitur pada setiap sisi poligon
                selected_features = st.multiselect('Pilih Fitur', feature_names, default=feature_names)
                selected_indices = [feature_names.index(feature) for feature in selected_features]
                selected_values = [feature_values[i] for i in selected_indices]
                plot_polygon_with_feature_values(selected_indices, selected_features, selected_values)
                st.write('Source : Premier League')
                
        with col_assist :
            st.dataframe(df_top_assist, use_container_width=True)
        with col_assist_img : 
            st.image(pots_img, caption='Kevin de Bruyne', use_column_width=True)
            with st.expander('Player Stats') :
                feature_names = ['Passes', 'Passes/nper match', 'Big chances created', 'Cross accuracy (%)', 'Through balls', 'Accurate long balls']  # Nama-nama fitur
                feature_values = [1357, 42.41, 31, 29, 28, 81]  # Nilai fitur pada setiap sisi poligon
                selected_features = st.multiselect('Pilih Fitur', feature_names, default=feature_names)
                selected_indices = [feature_names.index(feature) for feature in selected_features]
                selected_values = [feature_values[i] for i in selected_indices]
                plot_polygon_with_feature_values(selected_indices, selected_features, selected_values)
                st.write('Source : Premier League')

        with col_cleansheet :
            st.dataframe(df_top_cleansheet, use_container_width=True)
        with col_cleansheet_img:
            st.image(golden_glove_img, caption='David de Gea')
            with st.expander('Player Stats') :
                feature_names = ['Saves', 'Penalties Saved', 'Goal Conceded', 'Erros leading to goal', 'Own goals', 'Accurate long balls', 'Punches', 'High Claims', 'Catches']  # Nama-nama fitur
                feature_values = [101, 1, 43, 2, 0, 187, 12, 14, 5]  # Nilai fitur pada setiap sisi poligon
                selected_features = st.multiselect('Pilih Fitur', feature_names, default=feature_names)
                selected_indices = [feature_names.index(feature) for feature in selected_features]
                selected_values = [feature_values[i] for i in selected_indices]
                plot_polygon_with_feature_values(selected_indices, selected_features, selected_values)
                st.write('Source : Premier League')
    
    source_data2 = "https://www.premierleague.com/stats/top/players/goals?se=489"
    st.markdown(f'Source : [Players Stats]({source_data2})', unsafe_allow_html=True)

    # ======== Dataframe list top players End ======== #

def plot_club_polygon_with_feature_values(clubs_data):
    n = len(clubs_data)  # Jumlah klub yang dipilih
    n_features = len(clubs_data[0]['values'])  # Jumlah fitur

    # Normalisasi nilai fitur untuk setiap klub
    for club_data in clubs_data:
        club_data['values_normalized'] = normalize_log(club_data['values'])

    # Menambahkan satu elemen tambahan untuk memastikan kesimetrisan poligon
    for club_data in clubs_data:
        club_data['values_normalized'].append(club_data['values_normalized'][0])
        club_data['values'].append(club_data['values'][0])

    # Mengatur sudut untuk setiap sisi poligon
    angles = [i * 360 / float(n_features) for i in range(n_features)]
    angles += [angles[0] + 360]

    # Membuat plotly figure
    fig = go.Figure()

    # Menambahkan trace untuk setiap klub
    for club_data in clubs_data:
        fig.add_trace(go.Scatterpolar(
            r=club_data['values_normalized'],
            theta=angles,
            fill='toself',
            name=club_data['name'],
            hovertemplate='Club: %{name}<br>Nilai (Normalized): %{r:.2f}<br>Nilai (Original): %{text}<extra></extra>',
            text=club_data['values'],
            customdata=angles[:-1]  # Menambahkan data kustom berupa sudut
        ))

    # Mengatur tampilan sumbu sudut
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=''),
            angularaxis=dict(showticklabels=True, tickmode='array', tickvals=angles, ticktext=feature_names)
        ),
        title='Club Attributes Polygon Plot',  # Judul plot
    )

    # Mengatur ukuran plot
    fig.update_layout(width=500, height=500)

    # Menampilkan plot menggunakan Streamlit
    st.plotly_chart(fig)
    
with tab3 :   
    st.subheader('Attack Attributes')
    
    # Membaca file 'attack.csv' menggunakan pd.read_csv()
    attack_file_path = r'attack.csv'
    df_attack = pd.read_csv(attack_file_path)
    df_attack = df_attack.drop('Goals Free Kick', axis=1)

    # Menggunakan Streamlit untuk memilih klub-klub yang ingin dibandingkan
    with st.expander('Choose Club Here'):
        club_options = df_attack['Club'].unique().tolist()
        selected_clubs = st.multiselect('Available Clubs', club_options)
        clubs_data = []

        # Mengambil data klub yang dipilih
        for club in selected_clubs:
            club_data = {
                'name': club,
                'values': df_attack[df_attack['Club'] == club].values.flatten()[2:].astype(float).tolist()
            }
            clubs_data.append(club_data)

        # Menampilkan poligon untuk klub-klub yang dipilih
        if len(clubs_data) > 0:
            plot_club_polygon_with_feature_values(clubs_data)
                
    defence_file_path = r'defence.csv'
    df_defence = pd.read_csv(defence_file_path)

    st.write('_____')

    st.subheader('Defence Attributes')
    # Menggunakan Streamlit untuk memilih klub-klub yang ingin dibandingkan
    with st.expander('Choose Club Here'):
        club_options = df_defence['Club'].unique().tolist()
        selected_clubs = st.multiselect('Available Clubs', club_options)
        clubs_data = []

        # Mengambil data klub yang dipilih
        for club in selected_clubs:
            club_data = {
                'name': club,
                'values': df_defence[df_defence['Club'] == club].values.flatten()[2:].astype(float).tolist()
            }
            clubs_data.append(club_data)

        # Menampilkan poligon untuk klub-klub yang dipilih
        if len(clubs_data) > 0:
            plot_club_polygon_with_feature_values(clubs_data)
            
    teamplay_file_path = r'team_play.csv'
    df_teamplay = pd.read_csv(teamplay_file_path)

    st.write('_____')
    st.subheader('Team Play Attributes')
    # Menggunakan Streamlit untuk memilih klub-klub yang ingin dibandingkan
    with st.expander('Choose Club Here'):
        club_options = df_teamplay['Club'].unique().tolist()
        selected_clubs = st.multiselect('Available Clubs', club_options)
        clubs_data = []

        # Mengambil data klub yang dipilih
        for club in selected_clubs:
            club_data = {
                'name': club,
                'values': df_teamplay[df_teamplay['Club'] == club].values.flatten()[2:].astype(float).tolist()
            }
            clubs_data.append(club_data)

        # Menampilkan poligon untuk klub-klub yang dipilih
        if len(clubs_data) > 0:
            plot_club_polygon_with_feature_values(clubs_data)
    
    source_data3 = "https://www.premierleague.com/stats/top/clubs/wins?se=489"
    st.markdown(f'Source : [Premier League Club Stats]({source_data3})', unsafe_allow_html=True)

    
with tab4 :         
    model_path = "model_result.pkl"
    pickle_in = open(model_path, "rb")
    model = pickle.load(pickle_in)
    
    st.header('Predicting Premier League Match Result')
    
    # Membuat sebuah list
    list_items = ["Arsenal : 0", "Aston Villa : 1", "Bournemouth : 6", "Brentford : 7", "Brighton & Hove Albion : 8",
                  "Burnley : 9", "Chelsea : 12", "Crystal Palace : 13", "Everton : 15", "Fulham : 16", "Liverpool : 21",
                  "Luton Town : X", "Man. City : 22", "Man. United : 23", "Newcastle United : 26", "Nott'm Forrst : 28",
                  "Sheffield United : 32", "Tottenham Hostpur : 37", "West Ham United : 40", "Wolves : 42"]

    # Menampilkan expander di sidebar
    with st.expander("Home | Away Teams Code Numbers Information"):
        col_club1, col_club2 = st.columns(2)
        # Menampilkan setiap elemen list menggunakan st.markdown
        with col_club1 : 
            for item in list_items[:10]:
                st.markdown(f"- {item}")
        with col_club2 :
            for item in list_items[10:]:
                st.markdown(f"- {item}")
        st.write("Ket : X -> Memprediksi hasil akhir dengan club tersebut belum bisa diprediksi")
                    
    cols_home, cols_penengah, cols_away = st.columns([4,1,4])

    no_team_options = [0,1,6,7,8,9,12,13,15,16,
                       21,22,23,26,28,32,37,40,42]

    with cols_home:
        home_team = st.selectbox('Home Team', options=no_team_options)
        ht_home_score = st.text_input('Half Time Home Scored', value=0)
        home_possesion = st.slider('Home Team Possesion',1, 100, value=0)
        home_SoT = st.text_input('Home Shots on Target', value=0)
        home_shots = st.text_input('Home Shots', value=0)
        home_touches = st.text_input('Home Touches', value=0)
        home_passes = st.text_input('Home Passes', value=0)
        home_tackles = st.text_input('Home Tackles', value=0)
        home_clearances = st.text_input('Home Clearances', value=0)
        home_corners = st.text_input('Home Corners', value=0)
        home_offsides = st.text_input('Home Offsides', value=0)
        home_yellow_card = st.text_input('Home Yellow Card', value=0)
        home_red_card = st.text_input('Home Red Card', value=0)
        home_fouls = st.text_input('Home Fouls', value=0)

    with cols_away:
        away_team = st.selectbox('Away Team', options=no_team_options)
        ht_away_score = st.text_input('Half Time Away Scored', value=0)
        away_possesion = st.slider('Away Team Possesion',1, 100, value=100-home_possesion)
        awat_SoT = st.text_input('Away Shots on Target', value=0)
        awat_shots = st.text_input('Away Shots', value=0)
        away_touches = st.text_input('Away Touches', value=0)
        away_passes = st.text_input('Away Passes', value=0)
        away_tackles = st.text_input('Away Tackles', value=0)
        away_clearances = st.text_input('Away Clearances', value=0)
        away_corners = st.text_input('Away Corners', value=0)
        away_offsides = st.text_input('Away Offsides', value=0)
        away_yellow_card = st.text_input('Away Yellow Card', value=0)
        away_red_card = st.text_input('Away Red Card', value=0)
        away_fouls = st.text_input('Away Fouls', value=0)

    result_prediction = model.predict([[home_team, away_team, ht_home_score, ht_away_score,
                                        home_possesion, away_possesion,
                                        home_SoT, awat_SoT, home_shots, awat_shots, 
                                        home_touches, away_touches, home_passes, away_passes,
                                        home_tackles, away_tackles, home_clearances, away_clearances,
                                        home_corners, away_corners, home_offsides, away_offsides,
                                        home_yellow_card, away_yellow_card, home_red_card, away_red_card,
                                        home_fouls, away_fouls
                                        ]])
    result_match = ''
    
    if st.button('PREDICT', use_container_width=True) : 
        if(result_prediction[0] == 'W') : result_match = 'Home Team Will Win' 
        elif(result_prediction[0] == 'L') : result_match = 'Home Team Will Lost' 
        elif(result_prediction[0] == 'D') : result_match = 'Home Team Will Draw' 
        st.success(result_match)
    
