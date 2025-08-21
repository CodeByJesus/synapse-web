#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw

# Icono generado con Pillow (debe declararse después de importar PIL)
def _make_app_icon(size: int = 96) -> Image.Image:
    """Genera un ícono simple (sin emojis) para la app (barras tipo gráfico)."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Fondo blanco con borde gris
    draw.rectangle([0, 0, size-1, size-1], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255))
    # Barras estilo gráfico
    margin = int(size * 0.15)
    base_y = size - margin
    bar_w = int((size - 2 * margin) / 5)
    gap = int(bar_w * 0.4)
    heights = [0.35, 0.55, 0.25, 0.75, 0.5]
    x = margin
    for h in heights:
        top_y = base_y - int((size - 2 * margin) * h)
        draw.rectangle([x, top_y, x + bar_w, base_y], fill=(30, 136, 229, 255))
        x += bar_w + gap
    return img

# --- Traducciones simples (ES/EN) ---
LANG = {
    "es": {
        "title": "Synapse - Asistente de Datos",
        "subtitle": "Sube un archivo CSV o XLSX para explorar, analizar y visualizar tus datos.",
        "sidebar_load": "1) Carga de datos",
        "sidebar_file": "Archivo",
        "sidebar_use_example": "Usar archivo de ejemplo (test_large_file.csv)",
        "sidebar_sep": "Separador CSV (solo si es CSV)",
        "tab_overview": "Resumen",
        "tab_stats": "Estadísticas",
        "tab_plots": "Gráficas",
        "tab_data": "Datos",
        "info_file": "Información del archivo",
        "preview": "Vista previa",
        "dtypes": "Tipos de datos",
        "rows": "Filas",
        "cols": "Columnas",
        "nulls_total": "Nulos totales",
        "analysis_date": "Fecha de análisis",
        "desc_stats": "Estadísticas descriptivas",
        "no_cols_stats": "No hay columnas para calcular estadísticas.",
        "nulls_by_col": "Nulos por columna",
        "load_prompt": "Carga un archivo para comenzar. También puedes activar el ejemplo en la barra lateral.",
        "table_full": "Tabla completa",
        "lang_label": "Idioma / Language",
        "es_label": "Español",
        "en_label": "English",
    },
    "en": {
        "title": "Synapse - Data Assistant",
        "subtitle": "Upload a CSV or XLSX file to explore, analyze and visualize your data.",
        "sidebar_load": "1) Data load",
        "sidebar_file": "File",
        "sidebar_use_example": "Use example file (test_large_file.csv)",
        "sidebar_sep": "CSV separator (CSV only)",
        "tab_overview": "Overview",
        "tab_stats": "Statistics",
        "tab_plots": "Charts",
        "tab_data": "Data",
        "info_file": "File information",
        "preview": "Preview",
        "dtypes": "Data types",
        "rows": "Rows",
        "cols": "Columns",
        "nulls_total": "Total nulls",
        "analysis_date": "Analysis date",
        "desc_stats": "Descriptive statistics",
        "no_cols_stats": "There are no columns to compute statistics.",
        "nulls_by_col": "Nulls by column",
        "load_prompt": "Upload a file to begin. You can also use the example from the sidebar.",
        "table_full": "Full table",
        "lang_label": "Idioma / Language",
        "es_label": "Español",
        "en_label": "English",
    },
}

def t(key: str) -> str:
    lang = st.session_state.get("lang", "es")
    return LANG.get(lang, LANG["es"]).get(key, LANG["es"].get(key, key))

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
    st.subheader(t("info_file"))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("rows"), f"{len(df):,}")
    with col2:
        st.metric(t("cols"), f"{df.shape[1]:,}")
    with col3:
        st.metric(t("nulls_total"), f"{int(df.isna().sum().sum()):,}")
    with col4:
        st.metric(t("analysis_date"), datetime.now().strftime("%Y-%m-%d"))

    st.subheader(t("preview"))
    st.dataframe(df.head(50), use_container_width=True)

    with st.expander(t("dtypes")):
        dtypes_df = pd.DataFrame({"columna": df.columns, "dtype": df.dtypes.astype(str)})
        st.dataframe(dtypes_df, use_container_width=True)

def show_statistics(df: pd.DataFrame):
    """Estadísticas descriptivas y nulos por columna."""
    st.subheader(t("desc_stats"))
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
            st.info(t("no_cols_stats"))
    except Exception as e:
        st.warning(f"No se pudieron calcular las estadísticas: {e}")

    st.subheader(t("nulls_by_col"))
    nulls = df.isna().sum().sort_values(ascending=False)
    st.bar_chart(nulls)

def plot_section(df: pd.DataFrame):
    """Sección de gráficas con Matplotlib integrado en Streamlit."""
    st.subheader(t("tab_plots"))

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
            x = st.selectbox("Eje X (numérica)", numeric_cols, key="scatter_x")
            y = st.selectbox("Eje Y (numérica)", [c for c in numeric_cols if c != x], key="scatter_y")
            # Color por categoría (opcional)
            color_choice = "(ninguno)"
            if categorical_cols:
                color_choice = st.selectbox("Color por (opcional)", ["(ninguno)"] + categorical_cols, key="scatter_color")
            fig, ax = plt.subplots()
            if color_choice == "(ninguno)" or color_choice not in df.columns:
                ax.scatter(df[x], df[y], alpha=0.7)
            else:
                cats = df[color_choice].astype(str).fillna("NA").unique()[:10]
                for c in cats:
                    m = (df[color_choice].astype(str) == c)
                    ax.scatter(df.loc[m, x], df.loc[m, y], alpha=0.7, label=c)
                ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
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
            # Heatmap de correlación
            fig, ax = plt.subplots(figsize=(min(8, 1 + 0.5 * len(numeric_cols)), min(8, 1 + 0.5 * len(numeric_cols))))
            cax = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(numeric_cols)))
            ax.set_yticks(range(len(numeric_cols)))
            ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
            ax.set_yticklabels(numeric_cols)
            fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
            ax.set_title("Matriz de correlación")
            st.pyplot(fig)

    with tab_bar:
        if not categorical_cols:
            st.info("No hay columnas categóricas para graficar.")
        else:
            col = st.selectbox("Columna categórica", categorical_cols, key="bar_col")
            top_n = st.slider("Top categorías", 3, 50, 10)
            counts = df[col].astype(str).value_counts().head(top_n)
            st.bar_chart(counts)


def main():
    icon_img = _make_app_icon(96)
    st.set_page_config(
        page_title="Synapse - Asistente de Datos",
        page_icon=icon_img,
        layout="wide"
    )

    # Selector de idioma
    with st.sidebar:
        st.caption("")
        current = st.session_state.get("lang", "es")
        label = t("lang_label")
        option_labels = {"es": t("es_label"), "en": t("en_label")}
        lang_choice = st.selectbox(label, ["es", "en"], index=(0 if current=="es" else 1), format_func=lambda v: option_labels[v])
        st.session_state["lang"] = lang_choice

    # Título con icono a la izquierda
    title_col_icon, title_col_text = st.columns([0.08, 0.92])
    with title_col_icon:
        st.image(icon_img, width=28)
    with title_col_text:
        st.markdown(f"<h1 style='margin-bottom:0;'>{t('title')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#555;'>{t('subtitle')}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header(t("sidebar_load"))
        uploaded = st.file_uploader(t("sidebar_file"), type=["csv", "xlsx"], help="CSV, XLSX")
        use_example = st.checkbox(t("sidebar_use_example"))
        sep = st.text_input(t("sidebar_sep"), value=",")

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
        st.info(t("load_prompt"))
        return

    # Secciones principales
    tab_overview, tab_stats, tab_plots, tab_data = st.tabs([
        t("tab_overview"), t("tab_stats"), t("tab_plots"), t("tab_data")
    ])

    with tab_overview:
        dataframe_overview(df)

    with tab_stats:
        show_statistics(df)

    with tab_plots:
        plot_section(df)

    with tab_data:
        st.subheader(t("table_full"))
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
