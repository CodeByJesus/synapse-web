# 🧠 Synapse - Plataforma de Análisis de Datos Inteligente

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 📢 **AVISO IMPORTANTE - VERSIONES DISPONIBLES**

Synapse está disponible en **tres versiones** para diferentes necesidades:

- 🌐 **[Versión Web (GitHub)](https://github.com/CodeByJesus/synapse-web)** - Aplicación web completa con interfaz gráfica
- 🐧 **[Versión Linux CLI](https://github.com/CodeByJesus/synapse-cli)** - Interfaz de terminal intuitiva para Linux
- 🪟 **[Versión Windows Portable](https://github.com/CodeByJesus/synapse-windows)** - Aplicación portable para Windows

---

## 🚀 **Descripción**

**Synapse** es una plataforma avanzada de análisis de datos que automatiza el proceso de **Exploratory Data Analysis (EDA)** y generación de reportes profesionales. Diseñada para analistas de datos, consultores e investigadores que necesitan insights rápidos y precisos.

### ✨ **Características Principales**

- 📊 **Análisis Automático de Datos** - EDA completo con estadísticas descriptivas
- 🧹 **Limpieza Inteligente de Datos** - Detección y corrección automática de valores faltantes
- 📈 **Visualizaciones Interactivas** - Gráficas personalizables con Chart.js
- 📄 **Generación de PDFs Profesionales** - Reportes completos con insights y recomendaciones
- 🌍 **Soporte Multilingüe** - Interfaz en Español e Inglés
- 📱 **Diseño Responsive** - Funciona perfectamente en desktop y móvil
- ⚡ **Procesamiento Rápido** - Optimizado para datasets grandes

## 🛠️ **Tecnologías Utilizadas**

### **Backend**
- **Python 3.12+** - Lenguaje principal
- **Django 5.2** - Framework web robusto
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Computación numérica
- **Matplotlib** - Generación de gráficas
- **ReportLab** - Generación de PDFs profesionales

### **Frontend**
- **HTML5/CSS3** - Estructura y estilos modernos
- **JavaScript ES6+** - Interactividad avanzada
- **Chart.js** - Visualizaciones interactivas
- **Font Awesome** - Iconografía profesional

### **Herramientas de Desarrollo**
- **Git** - Control de versiones
- **Virtual Environment** - Gestión de dependencias
- **SQLite** - Base de datos ligera

## 📦 **Instalación**

### **Prerrequisitos**
- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git

### **Pasos de Instalación**

1. **Clonar el repositorio**
```bash
git clone https://github.com/CodeByJesus/synapse-web.git
cd synapse-web
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**
```bash
python manage.py migrate
```

5. **Ejecutar el servidor**
```bash
python manage.py runserver
```

6. **Abrir en el navegador**
```
http://127.0.0.1:8000
```

## 🎯 **Cómo Usar Synapse**

### **1. Subir Datos**
- Arrastra y suelta archivos CSV o Excel
- O haz clic para explorar y seleccionar archivos
- Formatos soportados: `.csv`, `.xlsx`, `.xls`

### **2. Análisis Automático**
- Synapse analiza automáticamente tu dataset
- Detecta valores faltantes y problemas de calidad
- Genera estadísticas descriptivas completas
- Identifica patrones y anomalías

### **3. Limpieza de Datos**
- **Eliminar filas con valores faltantes**
- **Rellenar con media/mediana/moda**
- **Rellenar con cero**
- **Revertir cambios** si es necesario

### **4. Visualizaciones**
- **Gráficas de barras** para datos categóricos
- **Gráficas de línea** para tendencias temporales
- **Gráficas de dispersión** para correlaciones
- **Personalización completa** de ejes y estilos

### **5. Exportar Reportes**
- **PDF profesional** con todos los análisis
- **Insights automáticos** y recomendaciones
- **Gráficas de alta calidad** incluidas
- **Estadísticas detalladas** por columna

## 📊 **Características Técnicas**

### **Análisis de Datos**
- ✅ **Estadísticas descriptivas** (media, mediana, desviación estándar)
- ✅ **Detección de valores faltantes** con porcentajes
- ✅ **Análisis de frecuencias** para variables categóricas
- ✅ **Correlación entre variables** numéricas
- ✅ **Detección de outliers** y anomalías
- ✅ **Evaluación de calidad** de datos

### **Limpieza Automática**
- ✅ **Estrategias múltiples** de imputación
- ✅ **Validación de datos** antes y después
- ✅ **Preservación de integridad** de datos
- ✅ **Logs detallados** de cambios realizados

### **Generación de Reportes**
- ✅ **PDFs profesionales** con branding
- ✅ **Secciones organizadas** y numeradas
- ✅ **Gráficas de alta resolución**
- ✅ **Recomendaciones específicas** por dataset
- ✅ **Métricas de calidad** de datos

### **Interfaz de Usuario**
- ✅ **Diseño responsive** para todos los dispositivos
- ✅ **Interfaz intuitiva** con drag & drop
- ✅ **Feedback visual** en tiempo real
- ✅ **Soporte multilingüe** (ES/EN)
- ✅ **Animaciones suaves** y profesionales

## 🏗️ **Arquitectura del Proyecto**

```
synapse/
├── data_assistant_app/          # Aplicación principal
│   ├── static/                  # Archivos estáticos
│   │   ├── css/                # Estilos CSS
│   │   └── js/                 # JavaScript
│   ├── templates/              # Plantillas HTML
│   ├── views.py               # Lógica de vistas
│   ├── pdf_generator.py       # Generador de PDFs
│   ├── translations.py        # Sistema de traducciones
│   └── utils_pdf.py          # Utilidades para PDFs
├── synapse_project/           # Configuración Django
├── media/                     # Archivos subidos
├── requirements.txt           # Dependencias
└── manage.py                 # Script de gestión
```

## 🔧 **Configuración Avanzada**

### **Variables de Entorno**
```bash
# Crear archivo .env
DEBUG=True
SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1
```

### **Configuración de Base de Datos**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🧪 **Testing**

```bash
# Ejecutar tests
python manage.py test

# Tests específicos
python manage.py test data_assistant_app.tests
```

## 📈 **Casos de Uso**

### **Para Analistas de Datos**
- **EDA rápido** de nuevos datasets
- **Limpieza automática** de datos
- **Generación de reportes** para stakeholders
- **Identificación de patrones** y anomalías

### **Para Consultores**
- **Análisis rápido** de datos de clientes
- **Reportes profesionales** para presentaciones
- **Insights automáticos** para recomendaciones
- **Visualizaciones** para dashboards

### **Para Investigadores**
- **Análisis exploratorio** de datasets de investigación
- **Limpieza de datos** de encuestas
- **Generación de reportes** para publicaciones
- **Validación de calidad** de datos

### **Para Startups**
- **Análisis de datos** de usuarios
- **Métricas de producto** y KPIs
- **Reportes automáticos** para inversores
- **Insights de crecimiento** y optimización

## 🚀 **Roadmap**

### **Versión 2.0 (Próximamente)**
- 🔮 **Machine Learning** básico (clustering, regresión)
- 🔗 **APIs externas** (Google Sheets, Dropbox)
- 👥 **Autenticación** de usuarios
- 🤝 **Colaboración** en tiempo real
- 📊 **Dashboards** interactivos

### **Versión 3.0 (Futuro)**
- 🤖 **IA avanzada** para insights automáticos
- ☁️ **Cloud deployment** automático
- 📱 **Aplicación móvil** nativa
- 🔄 **Integración** con herramientas BI
- 🌐 **API pública** para desarrolladores

## 🤝 **Contribuir**

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 **Autor**

**Jesus david martinez julio** - Desarrollador junior enfocado en backend y Data Scientist

- 🌐 [Portfolio](https://portafolio-jesusmartinez.netlify.app/)
- 💼 [LinkedIn]( https://www.linkedin.com/in/jesus-martinez-bb4596348/)
- 🐙 [GitHub](https://github.com/CodeByJesus)
- 📧 [Email](jd67941@gmail.com)

## 🙏 **Agradecimientos**

- **Django** por el framework web robusto
- **Pandas** por las herramientas de análisis de datos
- **Chart.js** por las visualizaciones interactivas
- **ReportLab** por la generación de PDFs profesionales
- **Font Awesome** por los iconos

## 📞 **Soporte**

Si tienes preguntas o necesitas ayuda:

- 📧 **Email**: jesusdmartinezj03@gmail.com
- 💬 **Issues**: [GitHub Issues](https://github.com/CodeByJesus/synapse-web/issues)
- 📖 **Documentación**: [Wiki](https://github.com/CodeByJesus/synapse-web/wiki)

---

<div align="center">

**⭐ Si te gusta Synapse, ¡dale una estrella al repositorio! ⭐**

*Construido con ❤️ para la comunidad de Data Science*

</div> 
