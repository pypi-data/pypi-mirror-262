"""Streamlit container to study correlations between features."""

import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from phik import phik_matrix

from explore.io import read_df


def correlation_container(file_path: pathlib.Path, dvc_step_key: str, schema_dict: dict[str, str]):
    """Display the correlation container."""
    st.write("---")
    st.header("Correlation study")

    col1, col2 = st.columns([1, 1])

    # Initialize session states for button clicks
    if "corr_matrix_button_clicked" not in st.session_state:
        st.session_state.corr_matrix_button_clicked = False

    if "ranked_corr_button_clicked" not in st.session_state:
        st.session_state.ranked_corr_button_clicked = False

    with col1:
        with st.container(border=True):
            selectable_columns = [col for col, _ in schema_dict.items()]
            submitted, corr_matrix_fields = user_inputs_corr_matrix(dvc_step_key, columns=selectable_columns)

            st.write("Correlation matrix computed with the 𝜙k correlation coefficient.")
            if submitted:
                st.session_state.corr_matrix_fields = corr_matrix_fields
                st.session_state.corr_matrix_button_clicked = True  # Set the state to True when the button is clicked

            # Only display the matrix if the button has been clicked
            if st.session_state.corr_matrix_button_clicked:
                correlation_matrix_output_container(file_path, st.session_state.corr_matrix_fields)

    with col2:
        with st.container(border=True):
            submitted, feature = user_input_corr_table(dvc_step_key, columns=selectable_columns)

            st.write("Ranked correlations of each feature with the selected feature.")
            if submitted:
                st.session_state.selected_feature = feature
                st.session_state.ranked_corr_button_clicked = True  # Set the state to True when the button is clicked

            # Only display the table if the button has been clicked
            if st.session_state.ranked_corr_button_clicked:
                correlation_table_output_container(file_path, st.session_state.selected_feature)


def correlation_matrix_output_container(file_path: pathlib.Path, corr_matrix_fields: list[str]):
    """Display the 𝜙k correlation matrix."""
    df = read_df(file_path)
    correlations = df.phik_matrix(verbose=False, dropna=True)
    correlations = correlations.loc[corr_matrix_fields, corr_matrix_fields]

    # Plotly heatmap of the correlations
    fig = px.imshow(correlations)
    fig.update_layout(
        autosize=False,
        width=360,
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_colorbar=dict(orientation="h", x=0.5, xanchor="center", y=1.4, yanchor="top", len=1),
    )
    st.plotly_chart(fig)


def correlation_table_output_container(file_path: pathlib.Path, feature: str):
    """Display the correlation table for the selected feature."""
    df = read_df(file_path)
    corr_phik = df.phik_matrix(verbose=False, dropna=True)
    is_categorical = not np.issubdtype(df[feature].dtype, np.number)  # Check if feature is not numeric
    # Calculate Pearson correlation only for numeric data
    corr_pearson = None
    if not is_categorical:
        corr_pearson = df.corr(method="pearson", numeric_only=True)

    st.subheader(f"Ranked 𝜙k correlations of each feature with {feature}")
    feature_ranked_corr = corr_phik[feature].sort_values(ascending=False)
    feature_ranked_corr = feature_ranked_corr[feature_ranked_corr.index != feature]  # Remove correlation with itself

    feature_corr_pearson = []
    if corr_pearson is not None:
        for idx in feature_ranked_corr.index:
            if idx in corr_pearson[feature].index:
                feature_corr_pearson.append(round(corr_pearson[feature][idx], 4))
            else:
                feature_corr_pearson.append(np.nan)
    else:
        # Fill with NaNs if the feature is categorical
        feature_corr_pearson = [np.nan] * len(feature_ranked_corr)

    # Create a DataFrame to display
    correlation_table = pd.DataFrame(
        {
            "Feature": feature_ranked_corr.index,
            "𝜙k Correlation": feature_ranked_corr.values,
            "Pearson Correlation": feature_corr_pearson,
        }
    )

    st.dataframe(correlation_table)

    st.write(
        "- 𝜙k correlation coefficient: Suitable for all categorical, ordinal and continuous variables. Captures linear and non-linear relationships. The coefficient ranges from 0 to 1, where 0 indicates no association and 1 indicates a perfect association. https://arxiv.org/pdf/1811.11440.pdf"
    )
    st.write(
        "- Pearson correlation coefficient: Only suitable for continuous variables. Captures linear relationships. The coefficient ranges from -1 to 1, where -1 indicates a perfect negative linear relationship, 0 indicates no linear relationship, and 1 indicates a perfect positive linear relationship. https://pubmed.ncbi.nlm.nih.gov/29481436/"
    )


def user_inputs_corr_matrix(dvc_step_key: str, columns: list[str]) -> tuple[bool, list[str], list[str]]:
    """Display the user inputs form and return the submitted values."""
    st.subheader("Correlation matrix")
    form = st.form(key=f"corr_matrix_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        corr_matrix_fields = st.multiselect(
            "Select the features of interest:",
            options=options,
            default=options,
            key=f"y_corr_cols_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")
    return submitted, corr_matrix_fields


def user_input_corr_table(dvc_step_key: str, columns: list[str]) -> tuple[bool, list[str], list[str]]:
    """Display the user inputs form and return the submitted values."""
    st.subheader("Ranked correlation table for input feature")
    form = st.form(key=f"corr_table_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        selected_feature = st.selectbox(
            "Select a feature to display its ranked 𝜙k correlation with the other features.",
            options=options,
            index=0,
            key=f"y_corr_col_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")
    return submitted, selected_feature
