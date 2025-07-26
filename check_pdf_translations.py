#!/usr/bin/env python3
import PyPDF2
import re

def extract_pdf_text(pdf_path):
    """Extraer texto del PDF"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error leyendo PDF: {e}")
        return ""

def analyze_translations(text):
    """Analizar qué secciones están en inglés vs español"""
    print("=== ANÁLISIS DE TRADUCCIONES EN EL PDF ===\n")
    
    # Buscar secciones principales
    sections = [
        "SYNAPSE DATA ANALYSIS REPORT",
        "EXECUTIVE SUMMARY", 
        "TABLE OF CONTENTS",
        "FILE INFORMATION",
        "MISSING VALUES",
        "FINAL DATA TABLE",
        "DESCRIPTIVE STATISTICS",
        "CORRELATION ANALYSIS",
        "CATEGORICAL FREQUENCIES",
        "CUSTOM CHART",
        "DATA QUALITY INSIGHTS",
        "CLEANING NOTES",
        "OBSERVATIONS AND RECOMMENDATIONS"
    ]
    
    print("🔍 SECCIONES ENCONTRADAS:")
    for section in sections:
        if section in text:
            print(f"✅ {section}")
        else:
            print(f"❌ {section} - NO ENCONTRADA")
    
    print("\n🔍 TEXTOS EN INGLÉS ENCONTRADOS:")
    english_patterns = [
        r"Data Quality Score",
        r"Total missing values",
        r"Column.*Mean.*Median.*Std Dev",
        r"Value.*Frequency",
        r"Examples of rows with incomplete data",
        r"Row \d+: Missing",
        r"Available data",
        r"Applied strategy",
        r"Removed rows with missing values",
        r"Filled missing values with",
        r"High variability detected",
        r"Potential outliers detected",
        r"Data shows skewness",
        r"High cardinality",
        r"Imbalanced categories",
        r"Small sample size",
        r"Missing values detected",
        r"Mixed data types detected",
        r"Duplicate values detected",
        r"Critical.*Warning.*Information",
        r"Bar Chart",
        r"Line Chart", 
        r"Scatter Plot",
        r"Unsupported chart type"
    ]
    
    found_english = []
    for pattern in english_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_english.extend(matches)
    
    if found_english:
        for item in set(found_english):
            print(f"❌ Texto en inglés: {item}")
    else:
        print("✅ No se encontraron textos en inglés")
    
    print("\n🔍 TEXTOS EN ESPAÑOL ENCONTRADOS:")
    spanish_patterns = [
        r"REPORTE DE ANÁLISIS DE DATOS SYNAPSE",
        r"RESUMEN EJECUTIVO",
        r"INFORMACIÓN DEL ARCHIVO",
        r"VALORES FALTANTES",
        r"ESTADÍSTICAS DESCRIPTIVAS",
        r"FRECUENCIAS CATEGÓRICAS",
        r"OBSERVACIONES Y RECOMENDACIONES",
        r"Total de valores faltantes",
        r"Nombre del archivo",
        r"Número de filas",
        r"Número de columnas",
        r"Fecha de análisis",
        r"Columna",
        r"Media",
        r"Mediana",
        r"Desv\. Est\.",
        r"Mín",
        r"Máx",
        r"Valor",
        r"Frecuencia",
        r"Porcentaje"
    ]
    
    found_spanish = []
    for pattern in spanish_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_spanish.extend(matches)
    
    if found_spanish:
        for item in set(found_spanish):
            print(f"✅ Texto en español: {item}")
    else:
        print("❌ No se encontraron textos en español")

if __name__ == "__main__":
    pdf_path = "/home/jesus/Descargas/synapse_report_20250726_145018.pdf"
    print(f"Analizando PDF: {pdf_path}")
    
    text = extract_pdf_text(pdf_path)
    if text:
        analyze_translations(text)
        
        # Mostrar las primeras líneas para contexto
        print("\n📄 PRIMERAS LÍNEAS DEL PDF:")
        lines = text.split('\n')[:20]
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"{i:2d}: {line.strip()}")
    else:
        print("No se pudo extraer texto del PDF") 