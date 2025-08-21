#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime

@st.cache_data(show_spinner=False)
def load_data(uploaded_file, file_type: str) -> pd.DataFrame:
    """
    Carga un archivo CSV/XLSX en un DataFrame de pandas.
    """
    if uploaded_file is None:
        return pd.DataFrame()
    try:
        if file_type == "csv":
            return pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return pd.DataFrame()

def dataframe_overview(df: pd.DataFrame):
    """Muestra información general del DataFrame."""
    st.subheader("Información del archivo")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Filas", f"{len(df):,}")
    with col2:
        st.metric("Columnas", f"{df.shape[1]:,}")
    with col3:
        st.metric("Nulos totales", f"{int(df.isna().sum().sum()):,}")
    with col4:
        st.metric("Fecha de análisis", datetime.now().strftime("%Y-%m-%d"))

    st.subheader("Vista previa")
    st.dataframe(df.head(50), use_container_width=True)

    with st.expander("Tipos de datos"):
        dtypes_df = pd.DataFrame({"columna": df.columns, "dtype": df.dtypes.astype(str)})
        st.dataframe(dtypes_df, use_container_width=True)

def show_statistics(df: pd.DataFrame):
    """Estadísticas descriptivas y nulos por columna."""
    st.subheader("Estadísticas descriptivas")
    try:
        numeric_df = df.select_dtypes(include=[np.number])
        non_numeric_df = df.select_dtypes(exclude=[np.number])

        parts = []
        if not numeric_df.empty:
            parts.append(numeric_df.describe().transpose())
        if not non_numeric_df.empty:
            # describe() en no-numéricos devuelve count, unique, top, freq
            parts.append(non_numeric_df.describe().transpose())

        if parts:
            desc = pd.concat(parts, axis=0)
            st.dataframe(desc, use_container_width=True)
        else:
            st.info("No hay columnas para calcular estadísticas.")
    except Exception as e:
        st.warning(f"No se pudieron calcular las estadísticas: {e}")

    st.subheader("Nulos por columna")
    nulls = df.isna().sum().sort_values(ascending=False)
    st.bar_chart(nulls)

def plot_section(df: pd.DataFrame):
    """Sección de gráficas con Matplotlib integrado en Streamlit."""
    st.subheader("Gráficas")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    tab_hist, tab_box, tab_scatter, tab_corr, tab_bar = st.tabs([
        "Histograma", "Boxplot", "Dispersión", "Correlación", "Barras"
    ])

    with tab_hist:
        if not numeric_cols:
            st.info("No hay columnas numéricas para graficar.")
        else:
            col = st.selectbox("Columna numérica", numeric_cols, key="hist_col")
            bins = st.slider("Bins", 5, 100, 30)
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=bins, color="#4e79a7")
            ax.set_title(f"Histograma - {col}")
            st.pyplot(fig)

    with tab_box:
        if not numeric_cols:
            st.info("No hay columnas numéricas para graficar.")
        else:
            col = st.selectbox("Columna numérica", numeric_cols, key="box_col")
            fig, ax = plt.subplots()
            ax.boxplot(df[col].dropna(), vert=True)
            ax.set_title(f"Boxplot - {col}")
            st.pyplot(fig)

    with tab_scatter:
        if len(numeric_cols) < 2:
            st.info("Se requieren al menos 2 columnas numéricas para dispersión.")
        else:
            x = st.selectbox("X", numeric_cols, key="scatter_x")
            y = st.selectbox("Y", [c for c in numeric_cols if c != x], key="scatter_y")
            fig, ax = plt.subplots()
            ax.scatter(df[x], df[y], alpha=0.7)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"Dispersión - {x} vs {y}")
            st.pyplot(fig)

    with tab_corr:
        if len(numeric_cols) < 2:
            st.info("Se requieren al menos 2 columnas numéricas para correlación.")
        else:
            corr = df[numeric_cols].corr(numeric_only=True)
            st.dataframe(corr, use_container_width=True)

    with tab_bar:
        if not categorical_cols:
            st.info("No hay columnas categóricas para graficar.")
        else:
            col = st.selectbox("Columna categórica", categorical_cols, key="bar_col")
            top_n = st.slider("Top categorías", 3, 50, 10)
            counts = df[col].astype(str).value_counts().head(top_n)
            st.bar_chart(counts)

def main():
    st.set_page_config(
        page_title="Synapse - Asistente de Datos",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Synapse - Asistente de Datos")
    st.markdown("Sube un archivo CSV o XLSX para explorar, analizar y visualizar tus datos.")

    with st.sidebar:
        st.header("1) Carga de datos")
        uploaded = st.file_uploader("Archivo", type=["csv", "xlsx"], help="Formatos soportados: CSV, XLSX")
        use_example = st.checkbox("Usar archivo de ejemplo (test_large_file.csv)")
        sep = st.text_input("Separador CSV (solo si es CSV)", value=",")

    df = pd.DataFrame()
    file_type = None

    if use_example:
        try:
            df = pd.read_csv("test_large_file.csv")
            file_type = "csv"
        except Exception as e:
            st.error(f"No se pudo cargar el archivo de ejemplo: {e}")
    elif uploaded is not None:
        file_type = uploaded.name.split(".")[-1].lower()
        if file_type == "csv":
            # Respetar separador si el usuario lo cambió
            df = load_data(BytesIO(uploaded.read() if hasattr(uploaded, 'read') else uploaded), "csv")
            if not df.empty and sep != ",":
                uploaded.seek(0)
                df = pd.read_csv(uploaded, sep=sep)
        elif file_type in ("xlsx", "xls"):
            df = load_data(uploaded, "xlsx")
        else:
            st.warning("Formato no soportado. Usa CSV o XLSX.")

    if df is None or df.empty:
        st.info("Carga un archivo para comenzar. También puedes activar el ejemplo en la barra lateral.")
        return

    # Secciones principales
    tab_overview, tab_stats, tab_plots, tab_data = st.tabs([
        "Resumen", "Estadísticas", "Gráficas", "Datos"
    ])

    with tab_overview:
        dataframe_overview(df)

    with tab_stats:
        show_statistics(df)

    with tab_plots:
        plot_section(df)

    with tab_data:
        st.subheader("Tabla completa")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
