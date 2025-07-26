// Synapse Data Assistant - Frontend JavaScript Module

document.addEventListener('DOMContentLoaded', function() {
    initializeInteractiveHeart();
    initializeFileUpload();
    initializeTemporaryMessages();
    
    console.log('Synapse frontend module loaded successfully');
});

// ===== INTERACTIVE HEART FUNCTIONALITY =====
function initializeInteractiveHeart() {
    const heartElement = document.getElementById('corazon');
    
    if (!heartElement) return;
    
    let clickCounter = 0;
    
    heartElement.addEventListener('click', function() {
        clickCounter++;
        
        this.classList.add('clickeado');
        
        const message = getHeartClickMessage(clickCounter);
        if (message) {
            showTemporaryMessage(message, 'success');
        }
        
        applyHeartClickEffect(this, clickCounter);
        
        setTimeout(() => {
            this.classList.remove('clickeado');
        }, 600);
    });
    
    heartElement.addEventListener('mouseenter', function() {
        console.log('Heart element hovered');
    });
}

function getHeartClickMessage(clickCount) {
    const messages = {
        1: 'Synapse available on Linux (CLI) and Windows (Portable)',
        2: 'Data analysis with pandas',
        3: 'Automatic file cleanup',
        4: 'Interactive visualization with Chart.js',
        5: 'Missing values detection (NaN)',
        6: 'Complete descriptive statistics',
        7: 'Responsive and modern design',
        8: 'Fast CSV and Excel processing',
        9: 'Intuitive and attractive interface',
        10: 'Re-analysis after cleaning',
        11: 'Synapse: Your perfect data assistant!'
    };
    
    if (clickCount <= 11) {
        return messages[clickCount];
    }
    
    const extraMessages = [
        'Intelligent data analysis',
        'Precise and reliable results',
        'Automatic configuration',
        'Professional charts',
        'Advanced cleaning tools',
        'Complete statistical analysis',
        'Modern visualization',
        'Optimized performance',
        'Available on Linux (CLI) and Windows (Portable)'
    ];
    
    return extraMessages[Math.floor(Math.random() * extraMessages.length)];
}

function applyHeartClickEffect(element, clickCount) {
    if (clickCount === 1) {
        element.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            element.style.filter = '';
        }, 2000);
    } else if (clickCount === 6) {
        element.style.filter = 'hue-rotate(45deg)';
        setTimeout(() => {
            element.style.filter = '';
        }, 2000);
    } else if (clickCount === 11) {
        element.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            element.style.transform = '';
        }, 1000);
    }
}

// ===== TEMPORARY MESSAGE SYSTEM =====
function showTemporaryMessage(text, type) {
    const messageElement = createMessageElement(text, type);
    document.body.appendChild(messageElement);
    
    setTimeout(() => {
        messageElement.style.animation = 'slideOut 0.5s ease';
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 500);
    }, 3000);
}

function createMessageElement(text, type) {
    const message = document.createElement('div');
    message.className = `temp-message message-${type}`;
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.5s ease;
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        max-width: 300px;
        text-align: center;
    `;
    
    return message;
}

// ===== DYNAMIC STYLES =====
const dynamicStyles = document.createElement('style');
dynamicStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .error-grafico .error-content {
        display: flex;
        align-items: flex-start;
        gap: 15px;
    }
    
    .error-grafico .error-text h4 {
        margin: 0 0 10px 0;
        color: #d32f2f;
        font-size: 18px;
    }
    
    .error-grafico .error-text p {
        margin: 0;
        color: #333;
        line-height: 1.5;
        white-space: pre-line;
    }
    
    .error-grafico .error-close {
        background: none;
        border: none;
        font-size: 24px;
        color: #999;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
        line-height: 1;
    }
    
    .error-grafico .error-close:hover {
        color: #d32f2f;
    }
    
    .error-grafico svg {
        color: #d32f2f;
        flex-shrink: 0;
        margin-top: 2px;
    }
`;
document.head.appendChild(dynamicStyles);

// ===== DATA EXTRACTION UTILITIES =====
function extractColumnData(columnName) {
    console.log('Extracting data for column:', columnName);
    
    const tableRows = document.querySelectorAll('#main-table tbody tr');
    console.log('Found table rows:', tableRows.length);
    
    const data = [];
    let columnIndex = -1;
    
    // Find column index
    const headers = document.querySelectorAll('#main-table thead th');
    console.log('Found headers:', headers.length);
    
    headers.forEach((header, index) => {
        console.log(`Header ${index}: "${header.textContent.trim()}"`);
        if (header.textContent.trim() === columnName) {
            columnIndex = index;
            console.log('Found column at index:', index);
        }
    });
    
    if (columnIndex === -1) {
        console.log('Column not found, returning empty array');
        return [];
    }
    
    tableRows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll('td');
        if (cells[columnIndex]) {
            const cellValue = cells[columnIndex].textContent.trim();
            // Skip empty values but log them
            if (cellValue === '' || cellValue === 'nan' || cellValue === 'NaN') {
                console.log(`Row ${rowIndex}: Empty/NaN value skipped`);
            } else {
                data.push(cellValue);
                console.log(`Row ${rowIndex}: "${cellValue}"`);
            }
        }
    });
    
    console.log('Extracted data:', data);
    return data;
}

// ===== CHART GENERATION =====
function generateChart() {
    console.log('Chart generation initiated');
    
    // Check if table exists
    const table = document.getElementById('main-table');
    if (!table) {
        console.error('Table with ID "main-table" not found');
        displayChartError('Data table not found. Please upload a file first.');
        return;
    }
    
    const chartTypeSelect = document.getElementById('tipo_grafico');
    const xColumnSelect = document.getElementById('columna_x');
    const yColumnSelect = document.getElementById('columna_y');
    
    if (!chartTypeSelect || !xColumnSelect || !yColumnSelect) {
        console.error('Chart form elements not found');
        displayChartError('Chart controls not found. Please refresh the page.');
        return;
    }
    
    const chartType = chartTypeSelect.value;
    const xColumn = xColumnSelect.value;
    const yColumn = yColumnSelect.value;
    const xLabels = extractColumnData(xColumn);
    const yData = extractColumnData(yColumn).map(value => {
        // Handle different number formats
        const cleanValue = value.toString().replace(/[^\d.,-]/g, '').replace(',', '.');
        const parsed = parseFloat(cleanValue);
        console.log(`Converting "${value}" to "${cleanValue}" = ${parsed}`);
        return parsed;
    });

    console.log('Chart parameters:', { 
        type: chartType, 
        xColumn, 
        yColumn, 
        labelCount: xLabels.length, 
        dataCount: yData.length 
    });

    const validationError = validateChartData(chartType, xColumn, yColumn, xLabels, yData);
    if (validationError) {
        console.log('Chart validation failed:', validationError);
        displayChartError(validationError);
        return;
    }

    cleanupPreviousChart();
    createNewChart(chartType, xColumn, yColumn, xLabels, yData);
    
    showTemporaryMessage('Chart generated successfully', 'success');
    saveChartConfiguration(chartType, xColumn, yColumn, xLabels, yData);
}

function cleanupPreviousChart() {
    console.log('Cleaning up previous chart');
    const canvas = document.getElementById('miGrafico');
    const context = canvas.getContext('2d');
    
    if (window.currentChart) {
        console.log('Destroying previous chart instance');
        window.currentChart.destroy();
        window.currentChart = null;
    } else {
        console.log('No previous chart found');
    }
}

function createNewChart(chartType, xColumn, yColumn, xLabels, yData) {
    console.log('Creating new chart instance');
    
    const canvas = document.getElementById('miGrafico');
    const context = canvas.getContext('2d');
    
    const chartData = {
        type: chartType === 'scatter' ? 'scatter' : chartType,
        data: {
            labels: chartType === 'scatter' ? undefined : xLabels,
            datasets: [{
                label: `${yColumn} vs ${xColumn}`,
                data: chartType === 'scatter'
                    ? xLabels.map((x, i) => ({x: parseFloat(x.replace(',', '.')), y: yData[i]}))
                    : yData,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                showLine: chartType === 'line' || chartType === 'scatter'
            }]
        },
        options: {
            scales: chartType === 'scatter' ? {
                x: { 
                    type: 'linear', 
                    position: 'bottom', 
                    title: { display: true, text: xColumn } 
                },
                y: { 
                    title: { display: true, text: yColumn } 
                }
            } : {}
        }
    };
    
    window.currentChart = new Chart(context, chartData);
}

// ===== DATA VALIDATION =====
function validateChartData(chartType, xColumn, yColumn, xLabels, yData) {
    if (xColumn === yColumn) {
        return 'Cannot use the same column for both axes';
    }

    if (xLabels.length === 0) {
        return `No data found for X-axis column "${xColumn}". Please check if the column exists and contains data.`;
    }
    
    if (yData.length === 0) {
        return `No data found for Y-axis column "${yColumn}". Please check if the column exists and contains data.`;
    }

    if (xLabels.length !== yData.length) {
        return `Data mismatch: X-axis has ${xLabels.length} values, Y-axis has ${yData.length} values.`;
    }
    
    // Check for valid numeric data in Y-axis
    const validNumericData = yData.filter(value => !isNaN(value));
    if (validNumericData.length === 0) {
        return `No valid numeric data found in Y-axis column "${yColumn}". Please select a column with numeric values.`;
    }

    if (chartType === 'bar') {
        const numericValues = yData.filter(value => !isNaN(value));
        if (numericValues.length === 0) {
            return `INCOMPATIBLE DATA FOR BAR CHART

To create a bar chart you need:
• X-axis: Categories (text)
• Y-axis: Numeric values (numbers)

Valid examples:
• Name vs Income
• City vs Average Age
• Gender vs Average Income

Your current selection is not compatible.`;
        }
    } else if (chartType === 'scatter') {
        const xNumeric = xLabels.filter(value => !isNaN(parseFloat(value.replace(',', '.'))));
        const yNumeric = yData.filter(value => !isNaN(value));
        
        if (xNumeric.length === 0 || yNumeric.length === 0) {
            return `INCOMPATIBLE DATA FOR SCATTER PLOT

To create a scatter plot you need:
• X-axis: Numeric values (numbers)
• Y-axis: Numeric values (numbers)

Valid examples:
• Age vs Income
• Height vs Weight
• Temperature vs Humidity

Your current selection is not compatible.`;
        }
    }

    return null;
}

function displayChartError(errorMessage) {
    const errorElement = createErrorElement(errorMessage);
    document.body.appendChild(errorElement);
    
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.parentNode.removeChild(errorElement);
        }
    }, 10000);
}

function createErrorElement(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-grafico';
    errorDiv.innerHTML = `
        <div class="error-content">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2"/>
                <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2"/>
            </svg>
            <div class="error-text">
                <h4>Chart Error</h4>
                <p>${message.replace(/\n/g, '<br>')}</p>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="error-close">×</button>
        </div>
    `;
    
    errorDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border: 2px solid #ff6b6b;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        max-width: 500px;
        max-height: 80vh;
        overflow-y: auto;
    `;
    
    return errorDiv;
}

// ===== CHART CONFIGURATION SAVING =====
function saveChartConfiguration(chartType, xColumn, yColumn, xLabels, yData) {
    const chartConfig = {
        type: chartType,
        xColumn: xColumn,
        yColumn: yColumn,
        labels: xLabels,
        data: yData
    };
    
    const formData = new FormData();
    formData.append('action', 'save_chart');
    formData.append('chart_data', JSON.stringify(chartConfig));
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Chart configuration saved successfully:', chartConfig);
        } else {
            console.error('Failed to save chart configuration:', data.message);
        }
    })
    .catch(error => {
        console.error('Chart configuration save request failed:', error);
    });
    
    console.log('Sending chart configuration to server:', chartConfig);
}

// ===== FILE UPLOAD FUNCTIONALITY =====
function initializeFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    
    if (!uploadArea || !fileInput) return;
    
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            uploadForm.submit();
        }
    });
    
    setupDragAndDrop(uploadArea, fileInput, uploadForm);
}

function setupDragAndDrop(uploadArea, fileInput, uploadForm) {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            uploadForm.submit();
        }
    });
}

// ===== TEMPORARY MESSAGE INITIALIZATION =====
function initializeTemporaryMessages() {
    const temporaryMessages = document.querySelectorAll('.temporary-message');
    
    temporaryMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 4000);
    });
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing functions...');
    
    // Initialize interactive heart
    initializeInteractiveHeart();
    
    // Initialize file upload functionality
    initializeFileUpload();
    
    // Initialize temporary messages
    initializeTemporaryMessages();
    
    console.log('All functions initialized successfully');
});

