import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import base64
from io import StringIO
import plotly.express as px  # For 3D scatter plot

# Function to get clean data
def get_clean_data():
    data = pd.read_csv("../data/data.csv")
    data = data.drop(['Unnamed: 32', 'id'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data

# Function to add sidebar sliders
def add_sidebar():
    st.sidebar.header("Cell Nuclei Details")
    data = get_clean_data()

    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(0),
            max_value=float(data[key].max()),
            value=float(data[key].mean()),
            help=f"Adjust the {label} value"
        )

    return input_dict

# Function to scale input values
def get_scaled_values(input_dict):
    data = get_clean_data()
    x = data.drop(['diagnosis'], axis=1)
    scaled_dict = {}

    for key, value in input_dict.items():
        max_value = x[key].max()
        min_value = x[key].min()
        scaled_value = (value - min_value) / (max_value - min_value)
        scaled_dict[key] = scaled_value

    return scaled_dict

# Function to generate radar chart
def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave points', 'Symmetry', 'Fractal dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
            input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
            input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
            input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'],
            input_data['area_se'], input_data['smoothness_se'], input_data['compactness_se'],
            input_data['concavity_se'], input_data['concave points_se'], input_data['symmetry_se'],
            input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
            input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
            input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
            input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

# Function to add predictions
def add_predictions(input_data):
    model = pickle.load(open("../model/model.pkl", "rb"))
    scalar = pickle.load(open("../model/scalar.pkl", "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scalar.transform(input_array)
    prediction = model.predict(input_array_scaled)

    st.subheader("Cell Cluster Prediction")

    if prediction[0] == 0:
        st.success("**Benign**")
    else:
        st.error("**Malignant**")

    st.write("**Probability of being Benign:**", model.predict_proba(input_array_scaled)[0][0])
    st.write("**Probability of being Malignant:**", model.predict_proba(input_array_scaled)[0][1])

    # Return prediction results for download
    results = {
        "Prediction": "Benign" if prediction[0] == 0 else "Malignant",
        "Probability Benign": model.predict_proba(input_array_scaled)[0][0],
        "Probability Malignant": model.predict_proba(input_array_scaled)[0][1]
    }
    return results

# Function to create a downloadable CSV
def create_downloadable_csv(results):
    df = pd.DataFrame([results])
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction_results.csv">Download Prediction Results as CSV</a>'
    return href

# Function to create 3D scatter plot
def plot_3d_scatter():
    data = get_clean_data()
    fig = px.scatter_3d(
        data,
        x='radius_mean',
        y='texture_mean',
        z='perimeter_mean',
        color='diagnosis',
        labels={'diagnosis': 'Diagnosis (0: Benign, 1: Malignant)'},
        title="3D Scatter Plot of Cell Nuclei Features"
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    st.plotly_chart(fig, use_container_width=True)

# Main function
def main():
    st.set_page_config(
        page_title="Breast Cancer Prediction App",
        page_icon=":female-doctor:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with open("../assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("Breast Cancer Prediction")
    st.write("This app uses machine learning to predict whether a breast cancer tumor is benign or malignant based on cell nuclei measurements.")

    input_data = add_sidebar()

    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader("Radar Chart of Cell Nuclei Features")
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart, use_container_width=True)

    with col2:
        results = add_predictions(input_data)

    # Add download button for prediction results
    st.markdown(create_downloadable_csv(results), unsafe_allow_html=True)

    # Add 3D scatter plot
    st.subheader("3D Scatter Plot of Cell Nuclei Features")
    plot_3d_scatter()

    st.markdown("---")
    st.write("**Disclaimer:** This app is for educational purposes only and should not be used as a substitute for professional medical advice.")


if __name__ == '__main__':
    main()