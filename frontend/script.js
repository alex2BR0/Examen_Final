// Configuración de la API
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINTS = {
    OPTIMIZE: '/optimizar',
    DETAILED: '/optimizar/detallado',
    EXAMPLES: '/ejemplos',
    HEALTH: '/health'
}; 

// Variables globales
let projectCounter = 0;
let charts = {};

// Clase principal de la aplicación
class PortfolioOptimizer {
    constructor() {
        this.initializeEventListeners();
        this.addInitialProject();
    }

    // Inicializar event listeners
    initializeEventListeners() {
        document.getElementById('addProject').addEventListener('click', () => this.addProject());
        document.getElementById('calculateBtn').addEventListener('click', () => this.calculateOptimization());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearForm());
        document.getElementById('loadExampleBtn').addEventListener('click', () => this.loadExample());
        
        // Modal event listeners
        const modal = document.getElementById('errorModal');
        const closeBtn = modal.querySelector('.close');
        closeBtn.addEventListener('click', () => this.closeErrorModal());
        window.addEventListener('click', (e) => {
            if (e.target === modal) this.closeErrorModal();
        });
    }

    // Agregar proyecto al formulario
    addProject() {
        projectCounter++;
        const projectHtml = this.createProjectHTML(projectCounter);
        document.getElementById('projectsContainer').insertAdjacentHTML('beforeend', projectHtml);
        
        // Agregar event listener al botón de eliminar
        const removeBtn = document.querySelector(`[data-project-id="${projectCounter}"]`);
        if (removeBtn) {
            removeBtn.addEventListener('click', (e) => this.removeProject(e));
        }
    }

    // Crear HTML para un proyecto
    createProjectHTML(id) {
        return `
            <div class="project-item" data-project-id="${id}">
                <h4>Proyecto ${id}</h4>
                <div class="project-fields">
                    <div class="form-group">
                        <label for="nombre_${id}">Nombre del Proyecto</label>
                        <input type="text" id="nombre_${id}" placeholder="Ej: Fondo_A" required>
                    </div>
                    <div class="form-group">
                        <label for="peso_${id}">Costo (USD)</label>
                        <input type="number" id="peso_${id}" placeholder="Ej: 2000" min="1" required>
                    </div>
                    <div class="form-group">
                        <label for="ganancia_${id}">Ganancia Esperada (USD)</label>
                        <input type="number" id="ganancia_${id}" placeholder="Ej: 1500" min="0" required>
                    </div>
                    <button type="button" class="remove-project" data-project-id="${id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }

    // Eliminar proyecto
    removeProject(event) {
        const projectId = event.currentTarget.getAttribute('data-project-id');
        const projectElement = document.querySelector(`[data-project-id="${projectId}"]`);
        if (projectElement) {
            projectElement.remove();
        }
    }

    // Agregar proyecto inicial
    addInitialProject() {
        this.addProject();
    }

    // Obtener datos del formulario
    getFormData() {
        const capacidad = parseInt(document.getElementById('capacidad').value);
        const projects = [];
        
        const projectElements = document.querySelectorAll('.project-item');
        projectElements.forEach(element => {
            const projectId = element.getAttribute('data-project-id');
            const nombre = document.getElementById(`nombre_${projectId}`).value.trim();
            const peso = parseInt(document.getElementById(`peso_${projectId}`).value);
            const ganancia = parseInt(document.getElementById(`ganancia_${projectId}`).value);
            
            if (nombre && !isNaN(peso) && !isNaN(ganancia)) {
                projects.push({
                    nombre: nombre,
                    peso: peso,
                    ganancia: ganancia
                });
            }
        });

        return { capacidad, objetos: projects };
    }

    // Validar datos del formulario
    validateFormData(data) {
        const errors = [];
        
        if (!data.capacidad || data.capacidad <= 0) {
            errors.push('La capacidad debe ser mayor que 0');
        }
        
        if (!data.objetos || data.objetos.length === 0) {
            errors.push('Debe agregar al menos un proyecto');
        }
        
        // Verificar nombres únicos
        const nombres = data.objetos.map(obj => obj.nombre);
        const nombresUnicos = new Set(nombres);
        if (nombres.length !== nombresUnicos.size) {
            errors.push('Los nombres de los proyectos deben ser únicos');
        }
        
        // Verificar valores válidos
        data.objetos.forEach((obj, index) => {
            if (!obj.nombre || obj.nombre.trim() === '') {
                errors.push(`El proyecto ${index + 1} debe tener un nombre`);
            }
            if (!obj.peso || obj.peso <= 0) {
                errors.push(`El proyecto ${obj.nombre || index + 1} debe tener un costo mayor que 0`);
            }
            if (obj.ganancia < 0) {
                errors.push(`El proyecto ${obj.nombre || index + 1} no puede tener ganancia negativa`);
            }
        });
        
        return errors;
    }

    // Calcular optimización
    async calculateOptimization() {
        try {
            const formData = this.getFormData();
            const errors = this.validateFormData(formData);
            
            if (errors.length > 0) {
                this.showError(errors.join('\n'));
                return;
            }

            this.showLoading(true);
            
            // Llamar a la API
            const response = await this.callAPI(API_ENDPOINTS.DETAILED, formData);
            
            if (response) {
                this.displayResults(response);
            }
            
        } catch (error) {
            console.error('Error en la optimización:', error);
            this.showError('Error al comunicarse con el servidor. Verifique que el backend esté ejecutándose.');
        } finally {
            this.showLoading(false);
        }
    }

    // Llamar a la API
    async callAPI(endpoint, data = null) {
        try {
            const url = `${API_BASE_URL}${endpoint}`;
            const options = {
                method: data ? 'POST' : 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(url, options);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
            }

            return await response.json();
            
        } catch (error) {
            throw error;
        }
    }

    // Mostrar resultados
    displayResults(data) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');
        
        // Mostrar sección de resultados
        resultsSection.style.display = 'block';
        resultsContent.style.display = 'block';
        
        // Actualizar tarjetas de resumen
        this.updateSummaryCards(data.resultado_optimizacion);
        
        // Actualizar tabla de proyectos seleccionados
        this.updateSelectedProjectsTable(data);
        
        // Actualizar análisis detallado
        this.updateDetailedAnalysis(data);
        
        // Crear gráficos
        this.createCharts(data);
        
        // Scroll a resultados
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Actualizar tarjetas de resumen
    updateSummaryCards(resultado) {
        document.getElementById('selectedCount').textContent = resultado.seleccionados.length;
        document.getElementById('totalGain').textContent = `$${resultado.ganancia_total.toLocaleString()}`;
        document.getElementById('totalWeight').textContent = `$${resultado.peso_total.toLocaleString()}`;
        document.getElementById('capacityUsed').textContent = `${resultado.capacidad_utilizada}%`;
    }

    // Actualizar tabla de proyectos seleccionados
    updateSelectedProjectsTable(data) {
        const tbody = document.getElementById('selectedProjectsBody');
        tbody.innerHTML = '';
        
        const resultado = data.resultado_optimizacion;
        const eficiencias = data.eficiencias_objetos;
        
        resultado.seleccionados.forEach(nombre => {
            const eficiencia = eficiencias.find(e => e.nombre === nombre);
            if (eficiencia) {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td><strong>${nombre}</strong></td>
                    <td>$${eficiencia.peso.toLocaleString()}</td>
                    <td>$${eficiencia.ganancia.toLocaleString()}</td>
                    <td>${eficiencia.eficiencia.toFixed(4)}</td>
                `;
            }
        });
    }

    // Actualizar análisis detallado
    updateDetailedAnalysis(data) {
        const stats = data.estadisticas;
        
        document.getElementById('portfolioEfficiency').textContent = data.resultado_optimizacion.eficiencia.toFixed(4);
        document.getElementById('totalProjects').textContent = stats.total_objetos_disponibles;
        document.getElementById('selectionPercentage').textContent = `${stats.porcentaje_seleccion}%`;
        document.getElementById('potentialGain').textContent = `$${stats.ganancia_total_disponible.toLocaleString()}`;
    }

    // Crear gráficos
    createCharts(data) {
        this.createInvestmentChart(data);
        this.createEfficiencyChart(data);
    }

    // Crear gráfico de distribución de inversión
    createInvestmentChart(data) {
        const ctx = document.getElementById('investmentChart').getContext('2d');
        
        if (charts.investment) {
            charts.investment.destroy();
        }
        
        const resultado = data.resultado_optimizacion;
        const eficiencias = data.eficiencias_objetos.filter(e => resultado.seleccionados.includes(e.nombre));
        
        charts.investment = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: eficiencias.map(e => e.nombre),
                datasets: [{
                    data: eficiencias.map(e => e.peso),
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#f5576c',
                        '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: $${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Crear gráfico de eficiencia
    createEfficiencyChart(data) {
        const ctx = document.getElementById('efficiencyChart').getContext('2d');
        
        if (charts.efficiency) {
            charts.efficiency.destroy();
        }
        
        const eficiencias = data.eficiencias_objetos;
        
        charts.efficiency = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: eficiencias.map(e => e.nombre),
                datasets: [{
                    label: 'Eficiencia (Ganancia/Costo)',
                    data: eficiencias.map(e => e.eficiencia),
                    backgroundColor: eficiencias.map((e, i) => {
                        const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'];
                        return colors[i % colors.length];
                    }),
                    borderWidth: 1,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Eficiencia'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Proyectos'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Eficiencia: ${context.parsed.y.toFixed(4)}`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Mostrar/ocultar loading
    showLoading(show) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        const resultsContent = document.getElementById('resultsContent');
        
        if (show) {
            loadingIndicator.style.display = 'block';
            resultsContent.style.display = 'none';
        } else {
            loadingIndicator.style.display = 'none';
            resultsContent.style.display = 'block';
        }
    }

    // Limpiar formulario
    clearForm() {
        document.getElementById('capacidad').value = '';
        document.getElementById('projectsContainer').innerHTML = '';
        document.getElementById('resultsSection').style.display = 'none';
        projectCounter = 0;
        this.addInitialProject();
    }

    // Cargar ejemplo
    async loadExample() {
        try {
            const response = await this.callAPI(API_ENDPOINTS.EXAMPLES);
            if (response && response.ejemplos && response.ejemplos.caso_1) {
                const ejemplo = response.ejemplos.caso_1.entrada;
                this.populateFormWithExample(ejemplo);
            }
        } catch (error) {
            console.error('Error al cargar ejemplo:', error);
            // Cargar ejemplo local si falla la API
            this.loadLocalExample();
        }
    }

    // Cargar ejemplo local
    loadLocalExample() {
        const ejemplo = {
            capacidad: 10000,
            objetos: [
                { nombre: "Fondo_A", peso: 2000, ganancia: 1500 },
                { nombre: "Fondo_B", peso: 4000, ganancia: 3500 },
                { nombre: "Fondo_C", peso: 5000, ganancia: 4000 },
                { nombre: "Fondo_D", peso: 3000, ganancia: 2500 },
                { nombre: "Fondo_E", peso: 1500, ganancia: 1800 }
            ]
        };
        this.populateFormWithExample(ejemplo);
    }

    // Poblar formulario con ejemplo
    populateFormWithExample(ejemplo) {
        // Limpiar formulario
        this.clearForm();
        
        // Establecer capacidad
        document.getElementById('capacidad').value = ejemplo.capacidad;
        
        // Agregar proyectos
        ejemplo.objetos.forEach((objeto, index) => {
            if (index > 0) {
                this.addProject();
            }
            
            const projectId = index + 1;
            document.getElementById(`nombre_${projectId}`).value = objeto.nombre;
            document.getElementById(`peso_${projectId}`).value = objeto.peso;
            document.getElementById(`ganancia_${projectId}`).value = objeto.ganancia;
        });
    }

    // Mostrar error
    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorModal').style.display = 'block';
    }

    // Cerrar modal de error
    closeErrorModal() {
        document.getElementById('errorModal').style.display = 'none';
    }
}

// Función global para cerrar modal (usada en HTML)
function closeErrorModal() {
    app.closeErrorModal();
}

// Inicializar aplicación cuando el DOM esté listo
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new PortfolioOptimizer();
    
    // Verificar conexión con el backend
    checkBackendConnection();
});

// Verificar conexión con el backend
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.HEALTH}`);
        if (!response.ok) {
            console.warn('Backend no disponible');
        }
    } catch (error) {
        console.warn('No se pudo conectar con el backend:', error);
    }
}
