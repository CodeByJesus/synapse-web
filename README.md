# 🧠 Synapse - Proyecto Educativo de Análisis de Datos

 

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Educational%20Project-orange.svg)]()

## 🎓 **PROYECTO EDUCATIVO - PROPÓSITO Y CONTEXTO**

**Synapse** es un **proyecto educativo** desarrollado para demostrar habilidades en **análisis de datos** y **desarrollo web**. Es importante aclarar que:

### ✅ **Lo que SÍ incluye:**
- **Demostración completa** de habilidades en tecnologías de análisis de datos
- **Implementación práctica** de librerías fundamentales (Pandas, NumPy, Matplotlib)
- **Desarrollo web** con Django y tecnologías frontend
- **Generación de PDFs** profesionales con ReportLab
- **Procesamiento de datos** y visualizaciones interactivas
- **Arquitectura de software** y buenas prácticas

### ❌ **Lo que NO incluye (limitaciones educativas):**
- **Funcionalidades avanzadas** de Machine Learning
- **Automatización completa** con IA
- **Soporte para Windows** (problemas de compatibilidad)
- **Características empresariales** como autenticación avanzada
- **Integración con APIs** externas complejas

### 🎯 **Motivo de Creación:**

Este proyecto fue desarrollado para **demostrar competencias** en las siguientes áreas de **análisis de datos**:

- **📊 Pandas**: Manipulación, limpieza y análisis de datasets
- **🔢 NumPy**: Computación numérica y operaciones matemáticas
- **📈 Matplotlib**: Generación de gráficas y visualizaciones
- **📄 ReportLab**: Creación de reportes PDF profesionales
- **🌐 Django**: Desarrollo web y arquitectura de aplicaciones
- **🎨 Frontend**: HTML, CSS, JavaScript para interfaces interactivas
- **📊 Chart.js**: Visualizaciones dinámicas en el navegador
- **🔧 Git**: Control de versiones y colaboración

### 🤖 **Limitación de IA:**

El proyecto **no incluye automatización con IA** debido a la **falta de recursos** para implementar sistemas de inteligencia artificial avanzados. Sin embargo, esto permite demostrar **habilidades técnicas puras** en el manejo de datos y desarrollo de software.

---

## 📢 **DISPONIBILIDAD**

Synapse está disponible para **ejecución local** en **Linux y macOS**:

- 🧩 **[Código Fuente (GitHub)](<https://github.com/CodeByJesus/synapse-web>)** — Proyecto completo (versión Django para ejecución local)

### ⚠️ **Nota sobre Windows**

Inicialmente se planeó crear una versión portable para Windows, pero se presentaron múltiples errores que se fueron acumulando y no fue posible solucionarlos de manera satisfactoria. Los problemas incluían:

- **Conflictos de dependencias** entre versiones de Python
- **Problemas de compatibilidad** con librerías específicas de Windows
- **Errores en la generación** de ejecutables portables
- **Inconsistencias** en el manejo de rutas de archivos
- **Limitaciones** en la virtualización de entornos

Por esta razón, la versión Windows no está disponible actualmente.

---

## 🚀 **Descripción**

**Synapse** es una **herramienta educativa** de análisis de datos que implementa **Exploratory Data Analysis (EDA)** y generación de reportes. Diseñada para **demostrar competencias** en tecnologías de análisis de datos y desarrollo web.

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
- **Linux/macOS** - Sistemas operativos soportados

## 📦 **Instalación**

Para ejecutar la versión completa localmente (entorno educativo con **Django**), sigue los pasos:

### **Prerrequisitos**
- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git
- Linux o macOS (Windows no soportado actualmente)

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

## 📈 **Casos de Uso Educativos**

### **Para Estudiantes de Data Science**
- **Práctica de EDA** con datasets reales
- **Aprendizaje de Pandas** y NumPy
- **Experimentación** con visualizaciones
- **Comprensión** de limpieza de datos

### **Para Desarrolladores Junior**
- **Demostración** de habilidades en análisis de datos
- **Portfolio** de proyectos técnicos
- **Aprendizaje** de Django y desarrollo web
- **Práctica** con tecnologías frontend

### **Para Educadores**
- **Herramienta de enseñanza** para cursos de análisis de datos
- **Ejemplos prácticos** de implementación de librerías
- **Demostración** de buenas prácticas de desarrollo
- **Material educativo** para estudiantes

### **Para Entrevistas Técnicas**
- **Portfolio** que demuestra competencias técnicas
- **Evidencia** de habilidades en múltiples tecnologías
- **Proyecto completo** que muestra capacidad de desarrollo
- **Demostración** de conocimientos en análisis de datos

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
- 🪟 **Soporte para Windows** (cuando se resuelvan los problemas de compatibilidad)

## 🤝 **Contribuir**

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 **Autor**

**Jesus david martinez julio** - Desarrollador junior enfocado en **análisis de datos** y **desarrollo web**

**Propósito del Proyecto**: Este proyecto fue desarrollado para **demostrar competencias técnicas** en análisis de datos y desarrollo de software, sirviendo como **portfolio educativo** que evidencia habilidades en múltiples tecnologías.

- 🌐 [Portfolio](https://portafolio-jesusmartinez.netlify.app/)
- 💼 [LinkedIn](https://www.linkedin.com/in/jesus-martinez-bb4596348/)
- 🐙 [GitHub](https://github.com/CodeByJesus)
- 📧 [Email](mailto:jd67941@gmail.com)

> 💡 **Tip**: Usa **Ctrl+Click** (Windows/Linux) o **Cmd+Click** (Mac) en los enlaces para abrirlos en una nueva pestaña.

## 🙏 **Agradecimientos**

- **Django** por el framework web que permitió demostrar habilidades de desarrollo
- **Pandas** por las herramientas fundamentales de análisis de datos
- **NumPy** por la computación numérica esencial
- **Matplotlib** por las capacidades de visualización
- **Chart.js** por las visualizaciones interactivas en el navegador
- **ReportLab** por la generación de PDFs profesionales
- **Font Awesome** por los iconos que mejoran la experiencia de usuario
- **Comunidad de Python** por las librerías que hacen posible el análisis de datos

## 📞 **Soporte**

Si tienes preguntas o necesitas ayuda:

- 📧 **Email**: jesusdmartinezj03@gmail.com
- 💬 **Issues**: [GitHub Issues](https://github.com/CodeByJesus/synapse-web/issues)
- 📖 **Documentación**: [Wiki](https://github.com/CodeByJesus/synapse-web/wiki)

---

<div align="center">

**⭐ Si te gusta este proyecto educativo, ¡dale una estrella al repositorio! ⭐**

*Construido con ❤️ para demostrar habilidades en análisis de datos y desarrollo web*

</div> 
