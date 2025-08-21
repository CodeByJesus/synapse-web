#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


# --- Traducciones simples (ES/EN) ---
LANG = {
    "es": {
        "title": "Synapse - Asistente de Datos",
        "subtitle": "Sube un archivo CSV o XLSX para explorar, analizar y visualizar tus datos.",
        "sidebar_load": "1) Carga de datos",
        "sidebar_file": "Archivo",
        "sidebar_use_example": "Usar archivo de ejemplo (test_large_file.csv)",
        "sidebar_examples": "Ejemplos",
        "example_none": "(ninguno)",
        "example_superstore": "Superstore (pérdida por producto)",
        "example_attrition": "Employee Attrition (rotación)",
        "example_house": "House Prices (precio)",
        "sidebar_sep": "Separador CSV (solo si es CSV)",
        "tab_overview": "Resumen",
        "tab_stats": "Estadísticas",
        "tab_plots": "Gráficas",
        "plot_tab_hist": "Histograma",
        "plot_tab_box": "Boxplot",
        "plot_tab_scatter": "Dispersión",
        "plot_tab_corr": "Correlación",
        "plot_tab_bar": "Barras",
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
        "no_numeric_for_plot": "No hay columnas numéricas para graficar.",
        "need_two_numeric": "Se requieren al menos 2 columnas numéricas para esta gráfica.",
        "numeric_column": "Columna numérica",
        "bins": "Bins",
        "x_axis_numeric": "Eje X (numérica)",
        "y_axis_numeric": "Eje Y (numérica)",
        "color_by_optional": "Color por (opcional)",
        "none_option": "(ninguno)",
        "corr_heatmap_title": "Matriz de correlación",
        "category_column": "Columna categórica",
        "count": "Conteo",
        "download_report_pdf": "Descargar reporte (PDF)",
        "analysis_date": "Fecha de análisis",
        "kpis_title": "KPIs",
        "insights_title": "Insights",
        "nulls_by_col": "Nulos por columna (top 5)",
        "dataset_label": "Conjunto de datos",
        "figure_word": "Figura",
        "load_prompt": "Sube un archivo para comenzar. También puedes usar el ejemplo desde la barra lateral.",
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
        "sidebar_examples": "Examples",
        "example_none": "(none)",
        "example_superstore": "Superstore (loss by product)",
        "example_attrition": "Employee Attrition (attrition)",
        "example_house": "House Prices (price)",
        "sidebar_sep": "CSV separator (CSV only)",
        "tab_overview": "Overview",
        "tab_stats": "Statistics",
        "tab_plots": "Charts",
        "plot_tab_hist": "Histogram",
        "plot_tab_box": "Boxplot",
        "plot_tab_scatter": "Scatter",
        "plot_tab_corr": "Correlation",
        "plot_tab_bar": "Bar",
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
        "no_numeric_for_plot": "There are no numeric columns to plot.",
        "need_two_numeric": "At least 2 numeric columns are required for this chart.",
        "numeric_column": "Numeric column",
        "bins": "Bins",
        "x_axis_numeric": "X axis (numeric)",
        "y_axis_numeric": "Y axis (numeric)",
        "color_by_optional": "Color by (optional)",
        "none_option": "(none)",
        "corr_heatmap_title": "Correlation matrix",
        "category_column": "Categorical column",
        "count": "Count",
        "download_report_pdf": "Download report (PDF)",
        "analysis_date": "Analysis date",
        "kpis_title": "KPIs",
        "insights_title": "Insights",
        "nulls_by_col": "Nulls by column (top 5)",
        "dataset_label": "Dataset",
        "figure_word": "Figure",
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
        t("plot_tab_hist"), t("plot_tab_box"), t("plot_tab_scatter"), t("plot_tab_corr"), t("plot_tab_bar")
    ])

    with tab_hist:
        if not numeric_cols:
            st.info(t("no_numeric_for_plot"))
        else:
            col = st.selectbox(t("numeric_column"), numeric_cols, key="hist_col")
            bins = st.slider(t("bins"), 5, 100, 30)
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=bins, color="#4e79a7")
            ax.set_title(f"{t('plot_tab_hist')} - {col}")
            st.pyplot(fig)

    with tab_box:
        if not numeric_cols:
            st.info(t("no_numeric_for_plot"))
        else:
            col = st.selectbox(t("numeric_column"), numeric_cols, key="box_col")
            fig, ax = plt.subplots()
            ax.boxplot(df[col].dropna(), vert=True)
            ax.set_title(f"{t('plot_tab_box')} - {col}")
            st.pyplot(fig)

    with tab_scatter:
        if len(numeric_cols) < 2:
            st.info(t("need_two_numeric"))
        else:
            x = st.selectbox(t("x_axis_numeric"), numeric_cols, key="scatter_x")
            y = st.selectbox(t("y_axis_numeric"), [c for c in numeric_cols if c != x], key="scatter_y")
            # Color por categoría (opcional)
            color_choice = t("none_option")
            if categorical_cols:
                color_choice = st.selectbox(t("color_by_optional"), [t("none_option")] + categorical_cols, key="scatter_color")
            fig, ax = plt.subplots()
            if color_choice == t("none_option") or color_choice not in df.columns:
                ax.scatter(df[x], df[y], alpha=0.7)
            else:
                cats = df[color_choice].astype(str).fillna("NA").unique()[:10]
                for c in cats:
                    m = (df[color_choice].astype(str) == c)
                    ax.scatter(df.loc[m, x], df.loc[m, y], alpha=0.7, label=c)
                ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"{t('plot_tab_scatter')} - {x} vs {y}")
            st.pyplot(fig)

    with tab_corr:
        if len(numeric_cols) < 2:
            st.info(t("need_two_numeric"))
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
            ax.set_title(t("corr_heatmap_title"))
            fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
            st.pyplot(fig)

    with tab_bar:
        if not categorical_cols:
            st.info(t("category_column") + ": -")
        else:
            cat_col = st.selectbox(t("category_column"), categorical_cols, key="bar_cat_col")
            counts = df[cat_col].astype(str).fillna("NA").value_counts().head(20)
            fig, ax = plt.subplots()
            counts.plot(kind='bar', ax=ax, color="#59a14f")
            ax.set_title(f"{t('plot_tab_bar')} - {cat_col}")
            ax.set_xlabel(cat_col)
            ax.set_ylabel(t("count"))
            st.pyplot(fig)

def main():
    st.set_page_config(
        page_title="Synapse - Asistente de Datos",
        layout="wide"
    )

    # Encabezado con selector de idioma compacto a la derecha
    header_left, header_right = st.columns([0.75, 0.25])
    with header_left:
        st.markdown(f"<h1 style='margin-bottom:0;'>{t('title')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#555;'>{t('subtitle')}</div>", unsafe_allow_html=True)
    with header_right:
        current = st.session_state.get("lang", "es")
        default_lbl = "ES" if current == "es" else "EN"
        choice_lbl = st.segmented_control(
            t("lang_label"),
            options=["ES", "EN"],
            default=default_lbl,
            label_visibility="collapsed",
            key="lang_selector_top"
        )
        new_lang = "es" if choice_lbl == "ES" else "en"
        if new_lang != current:
            st.session_state["lang"] = new_lang
            st.rerun()

    with st.sidebar:
        st.header(t("sidebar_load"))
        uploaded = st.file_uploader(t("sidebar_file"), type=["csv", "xlsx"], help="CSV, XLSX")
        sep = st.text_input(t("sidebar_sep"), value=",")

    df = pd.DataFrame()
    file_type = None

    if uploaded is not None:
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

    # Descarga de reporte PDF mejorado con KPIs, insights y gráficos
    def _build_pdf_report(data: pd.DataFrame, dataset_label: str) -> bytes:
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        width, height = letter

        def draw_footer():
            c.setFont("Helvetica", 9)
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.drawRightString(width - 36, 24, f"{t('title')} — Pg {c.getPageNumber()}")
            c.setFillColorRGB(0, 0, 0)

        def hline(y):
            c.setLineWidth(0.5)
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.line(36, y, width - 36, y)
            c.setStrokeColorRGB(0, 0, 0)

        # Portada
        c.setFont("Helvetica-Bold", 18)
        c.drawString(72, height - 72, t("title"))
        c.setFont("Helvetica", 11)
        c.drawString(72, height - 92, f"{t('analysis_date')}: {datetime.now().strftime('%Y-%m-%d')}")
        if dataset_label:
            c.drawString(72, height - 110, f"Dataset: {dataset_label}")
        hline(height - 118)
        draw_footer()
        # KPIs
        kpi_y = height - 150
        kpis = [
            (t("rows"), f"{len(data):,}"),
            (t("cols"), f"{data.shape[1]:,}"),
            (t("nulls_total"), f"{int(data.isna().sum().sum()):,}")
        ]
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, kpi_y, "KPIs")
        c.setFont("Helvetica", 11)
        for i, (k, v) in enumerate(kpis):
            c.drawString(72, kpi_y - 18 * (i + 1), f"• {k}: {v}")

        # Insights rápidos
        y = kpi_y - 18 * (len(kpis) + 1) - 6
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, "Insights")
        y -= 18
        # Top correlaciones (si aplica)
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            corr = data[numeric_cols].corr(numeric_only=True).abs()
            pairs = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    a, b = numeric_cols[i], numeric_cols[j]
                    val = corr.loc[a, b]
                    if pd.notna(val):
                        pairs.append((val, a, b))
            pairs.sort(reverse=True)
            top = pairs[:5]
            c.setFont("Helvetica", 11)
            for val, a, b in top:
                c.drawString(72, y, f"• corr({a}, {b}) = {val:.2f}")
                y -= 16

        # Top nulos por columna
        null_counts = data.isna().sum().sort_values(ascending=False)
        top_nulls = [(col, int(cnt), (cnt/len(data))*100 if len(data) else 0) for col, cnt in null_counts.head(5).items() if cnt > 0]
        if top_nulls:
            y -= 6
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, y, t("nulls_by_col"))
            y -= 18
            c.setFont("Helvetica", 11)
            for col, cnt, pct in top_nulls:
                c.drawString(72, y, f"• {col}: {cnt} ({pct:.1f}%)")
                y -= 16

        draw_footer()
        c.showPage()

        # Figura 1: Heatmap de correlación (si hay columnas numéricas)
        if len(numeric_cols) >= 2:
            corr = data[numeric_cols].corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(6, 6))
            cax = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(numeric_cols)))
            ax.set_yticks(range(len(numeric_cols)))
            ax.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=8)
            ax.set_yticklabels(numeric_cols, fontsize=8)
            ax.set_title(t("corr_heatmap_title"))
            fig.colorbar(cax)
            img_buf = BytesIO()
            fig.tight_layout()
            fig.savefig(img_buf, format='png', dpi=150)
            plt.close(fig)
            img_buf.seek(0)
            img = ImageReader(img_buf)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, height - 72, t("corr_heatmap_title"))
            hline(height - 80)
            c.drawImage(img, 72, 120, width=width-144, height=width-180, preserveAspectRatio=True, anchor='sw')
            c.setFont("Helvetica", 10)
            c.drawString(72, 96, f"Figura 1. {t('corr_heatmap_title')}")
            draw_footer()
            c.showPage()

        # Figura 2: Barras top categorías (si hay categóricas)
        categorical_cols = data.select_dtypes(exclude=[np.number]).columns.tolist()
        if categorical_cols:
            cat_col = categorical_cols[0]
            counts = data[cat_col].astype(str).fillna("NA").value_counts().head(20)
            fig, ax = plt.subplots(figsize=(7.5, 5))
            counts.plot(kind='bar', ax=ax, color="#59a14f")
            ax.set_title(f"{t('plot_tab_bar')} - {cat_col}")
            ax.set_xlabel(cat_col)
            ax.set_ylabel(t("count"))
            fig.tight_layout()
            img_buf = BytesIO()
            fig.savefig(img_buf, format='png', dpi=150)
            plt.close(fig)
            img_buf.seek(0)
            img = ImageReader(img_buf)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, height - 72, f"{t('plot_tab_bar')} - {cat_col}")
            hline(height - 80)
            c.drawImage(img, 72, 120, width=width-144, height=height-190, preserveAspectRatio=True, anchor='sw')
            c.setFont("Helvetica", 10)
            c.drawString(72, 96, f"Figura 2. {t('plot_tab_bar')} — {cat_col}")
            draw_footer()
            c.showPage()

        c.save()
        buf.seek(0)
        return buf.read()

    # Etiqueta descriptiva del dataset para el PDF
    dataset_label = None
    if uploaded is not None:
        dataset_label = getattr(uploaded, 'name', 'uploaded_file')

    with st.sidebar:
        pdf_bytes = _build_pdf_report(df, dataset_label or "")
        st.download_button(
            label=t("download_report_pdf"),
            data=pdf_bytes,
            file_name=f"synapse_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
