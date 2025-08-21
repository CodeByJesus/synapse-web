#!/usr/bin/env python3
import streamlit as st
import PyPDF2
import re

def extract_pdf_text(uploaded_file):
    """Extraer texto del PDF"""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error leyendo PDF: {e}")
        return ""

def analyze_translations(text):
    """Analizar qué secciones están en inglés vs español"""
    results = {
        'sections_found': [],
        'sections_missing': [],
        'english_texts': set(),
        'spanish_texts': set(),
        'translation_quality': 'Buena'  # Por defecto asumimos buena calidad
    }
    
    # Secciones a buscar
    sections = [
        "SYNAPSE DATA ANALYSIS REPORT", "EXECUTIVE SUMMARY", "TABLE OF CONTENTS",
        "FILE INFORMATION", "MISSING VALUES", "FINAL DATA TABLE", "DESCRIPTIVE STATISTICS",
        "CORRELATION ANALYSIS", "CATEGORICAL FREQUENCIES", "CUSTOM CHART",
        "DATA QUALITY INSIGHTS", "CLEANING NOTES", "OBSERVATIONS AND RECOMMENDATIONS"
    ]
    
    # Patrones en inglés
    english_patterns = [
        r"Data Quality Score", r"Total missing values", r"Column.*Mean.*Median.*Std Dev",
        r"Value.*Frequency", r"Examples of rows with incomplete data", r"Row \d+: Missing",
        r"Available data", r"Applied strategy", r"Removed rows with missing values",
        r"Filled missing values with", r"High variability detected", r"Potential outliers detected",
        r"Data shows skewness", r"High cardinality", r"Imbalanced categories",
        r"Small sample size", r"Missing values detected", r"Mixed data types detected",
        r"Duplicate values detected", r"Critical.*Warning.*Information",
        r"Bar Chart", r"Line Chart", r"Scatter Plot", r"Unsupported chart type"
    ]
    
    # Patrones en español
    spanish_patterns = [
        r"REPORTE DE ANÁLISIS DE DATOS SYNAPSE", r"RESUMEN EJECUTIVO",
        r"INFORMACIÓN DEL ARCHIVO", r"VALORES FALTANTES", r"ESTADÍSTICAS DESCRIPTIVAS",
        r"FRECUENCIAS CATEGÓRICAS", r"OBSERVACIONES Y RECOMENDACIONES",
        r"Total de valores faltantes", r"Nombre del archivo", r"Número de filas",
        r"Número de columnas", r"Fecha de análisis", r"Columna", r"Media",
        r"Mediana", r"Desv\. Est\.", r"Mín", r"Máx", r"Valor", r"Frecuencia",
        r"Porcentaje"
    ]
    
    # Verificar secciones
    for section in sections:
        if section in text:
            results['sections_found'].append(section)
        else:
            results['sections_missing'].append(section)
    
    # Buscar textos en inglés
    for pattern in english_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results['english_texts'].update(matches)
    
    # Buscar textos en español
    for pattern in spanish_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results['spanish_texts'].update(matches)
    
    # Evaluar calidad de la traducción
    if results['english_texts'] and results['spanish_texts']:
        results['translation_quality'] = 'Mixta (contiene textos en inglés y español)'
    elif results['english_texts'] and not results['spanish_texts']:
        results['translation_quality'] = 'Solo inglés (sin traducción)'
    elif not results['english_texts'] and results['spanish_texts']:
        results['translation_quality'] = 'Completa (solo español)'
    
    return results

def main():
    st.set_page_config(
        page_title="Analizador de Traducciones PDF",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Analizador de Traducciones PDF")
    st.markdown("""
    Sube un archivo PDF para analizar la calidad de las traducciones entre inglés y español.
    """)
    
    uploaded_file = st.file_uploader("Sube tu archivo PDF", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner('Analizando el documento...'):
            text = extract_pdf_text(uploaded_file)
            if text:
                results = analyze_translations(text)
                
                # Mostrar resultados
                st.header("📊 Resultados del Análisis")
                
                # Calidad de la traducción
                st.markdown("""
                ### Calidad de la Traducción
                <div style='padding: 10px; border-radius: 5px; background-color: #f0f2f6; margin: 10px 0;'>
                    <span style='font-weight: bold;'>{}</span>
                </div>
                """.format(results['translation_quality']), unsafe_allow_html=True)
                
                # Secciones encontradas
                with st.expander("📑 Secciones del Documento", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("✅ Secciones Encontradas")
                        for section in results['sections_found']:
                            st.success(f"✓ {section}")
                    with col2:
                        if results['sections_missing']:
                            st.subheader("❌ Secciones Faltantes")
                            for section in results['sections_missing']:
                                st.error(f"✗ {section}")
                
                # Textos en inglés
                if results['english_texts']:
                    with st.expander("🔍 Textos en Inglés Encontrados", expanded=False):
                        st.warning("Se encontraron los siguientes textos en inglés:")
                        for text in sorted(results['english_texts']):
                            st.write(f"- {text}")
                
                # Textos en español
                if results['spanish_texts']:
                    with st.expander("🔍 Textos en Español Encontrados", expanded=False):
                        st.success("Se encontraron los siguientes textos en español:")
                        for text in sorted(results['spanish_texts']):
                            st.write(f"- {text}")
                
                # Vista previa del texto
                with st.expander("📄 Vista Previa del Texto", expanded=False):
                    st.text_area("Primeras 500 caracteres del documento:", 
                               value=text[:500] + ("..." if len(text) > 500 else ""),
                               height=200)

if __name__ == "__main__":
    main()
