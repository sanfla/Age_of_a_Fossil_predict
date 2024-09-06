import streamlit as st
import joblib
import pandas as pd
import requests
from io import BytesIO

page = st.sidebar.selectbox("Pilih Halaman", ["Pendahuluan", "Perhitungan Prediksi"])

model_url = "https://github.com/sanfla/Age_of_a_Fossil_predict/raw/main/regression.pkl"
response = requests.get(model_url)
model = joblib.load(BytesIO(response.content))

if page == "Pendahuluan":

    st.image('https://github.com/sanfla/Age_of_a_Fossil_predict/blob/main/AF_image.png?raw=true', use_column_width=True)

    st.title("Pendahuluan")

    data = pd.read_csv("https://raw.githubusercontent.com/sanfla/Age_of_a_Fossil_predict/main/Age%20_Fossil.csv")
    st.dataframe(data.head(5))

    st.write("""
    Dataset Fosil dibuat untuk memberikan dasar yang komprehensif dan realistis dalam melatih dan mengevaluasi model pembelajaran mesin yang bertujuan 
    untuk memprediksi usia fosil. Dataset ini memiliki tingkat kesulitan menengah dan mencakup berbagai atribut geologis, kimia, dan fisik yang signifikan 
    dalam studi pembentukan dan pelestarian fosil.

    Data awalnya bersumber terutama dari PaleoBioDB, dengan tambahan sumber pribadi yang berkontribusi pada dataset. Setelah membuat dataset kecil awal, 
    model pembelajaran mendalam digunakan untuk memperluas dan menghasilkan versi sintetis. Dataset sintetis ini mensimulasikan skenario yang realistis, 
    menjadikannya alat yang berharga bagi ilmuwan data dan peneliti di bidang ini.

    **Fitur**

    - **uranium_lead_ratio**: Rasio isotop uranium terhadap timbal dalam sampel fosil.
    - **carbon_14_ratio**: Rasio isotop karbon-14 yang ada dalam sampel fosil.
    - **radioactive_decay_series**: Pengukuran seri peluruhan dari isotop induk ke isotop anak.
    - **stratigraphic_layer_depth**: Kedalaman fosil dalam lapisan stratigrafi, dalam meter.
    - **isotopic_composition**: Proporsi berbagai isotop dalam sampel fosil.
    - **fossil_size**: Ukuran fosil, dalam sentimeter.
    - **fossil_weight**: Berat fosil, dalam gram.
    - **geological_period**: Periode geologis saat fosil terbentuk.
    - **surrounding_rock_type**: Jenis batuan yang mengelilingi fosil.
    - **paleomagnetic_data**: Data orientasi paleomagnetik dari lokasi fosil.
    - **stratigraphic_position**: Posisi fosil dalam kolom stratigrafi.
    - **age**: Usia fosil yang dihitung berdasarkan berbagai fitur, dalam tahun.
    """)


elif page == "Perhitungan Prediksi":

    st.image('https://github.com/sanfla/Age_of_a_Fossil_predict/blob/main/AF_image.png?raw=true', use_column_width=True)

    st.title("Prediksi Usia Fosil Berdasarkan Fitur Geologis")

    col1, col2, col3 = st.columns(3)

    with col1:
        uranium_lead_ratio = st.number_input('Rasio Uranium-Lead', min_value=0.0, max_value=1.0, value=0.5)
        carbon_14_ratio = st.number_input('Rasio Carbon-14', min_value=0.0, max_value=1.0, value=0.5)
        radioactive_decay_series = st.number_input('Seri Peluruhan Radioaktif', min_value=0.0, max_value=2.0, value=1.0)

    with col2:
        stratigraphic_layer_depth = st.number_input('Kedalaman Lapisan Stratigrafi', min_value=0.0, max_value=500.0, value=100.0)
        geological_period = st.selectbox('Periode Geologis', ['Cretaceous', 'Cambrian', 'Permian', 'Devonian', 'Jurassic', 'Neogene'])
        paleomagnetic_data = st.selectbox('Data Paleomagnetik', ['Normal polarity', 'Reversed polarity'])

    with col3:    
        inclusion_of_other_fossils = st.selectbox('Apakah Ada Fosil Lain?', [True, False])
        stratigraphic_position = st.selectbox('Posisi Stratigrafi', ['Top', 'Middle', 'Bottom'])
        fossil_size = st.number_input('Ukuran Fosil (cm)', min_value=0.0, max_value=200.0, value=50.0)

    if st.button('Prediksi Umur Fosil'):
        input_data = pd.DataFrame({
            'uranium_lead_ratio': [uranium_lead_ratio],
            'carbon_14_ratio': [carbon_14_ratio],
            'radioactive_decay_series': [radioactive_decay_series],
            'stratigraphic_layer_depth': [stratigraphic_layer_depth],
            'geological_period': [geological_period],
            'paleomagnetic_data': [paleomagnetic_data],
            'inclusion_of_other_fossils': [inclusion_of_other_fossils],
            'stratigraphic_position': [stratigraphic_position],
            'fossil_size': [fossil_size],
        })

        prediction = model.predict(input_data)

        st.success(f"Prediksi umur fosil: {prediction[0]:.2f} tahun")
