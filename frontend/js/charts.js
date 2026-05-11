// Global Chart Configurations
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(17, 17, 17, 0.9)';
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.cornerRadius = 8;

let revenueChartInstance = null;
let categoryChartInstance = null;

// Initialize Revenue Chart
function initRevenueChart(historicalData, predictedData, labels) {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    
    if (revenueChartInstance) {
        revenueChartInstance.destroy();
    }

    // Create Gradients
    const gradientHistorical = ctx.createLinearGradient(0, 0, 0, 400);
    gradientHistorical.addColorStop(0, 'rgba(14, 165, 233, 0.5)'); // Secondary
    gradientHistorical.addColorStop(1, 'rgba(14, 165, 233, 0.0)');

    const gradientPredicted = ctx.createLinearGradient(0, 0, 0, 400);
    gradientPredicted.addColorStop(0, 'rgba(79, 70, 229, 0.5)'); // Primary
    gradientPredicted.addColorStop(1, 'rgba(79, 70, 229, 0.0)');

    revenueChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Revenue',
                    data: historicalData,
                    borderColor: '#0ea5e9',
                    backgroundColor: gradientHistorical,
                    borderWidth: 2,
                    pointBackgroundColor: '#0ea5e9',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'AI Predicted Forecast',
                    data: predictedData,
                    borderColor: '#4F46E5',
                    backgroundColor: gradientPredicted,
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointBackgroundColor: '#4F46E5',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000) + 'k';
                        }
                    }
                }
            }
        }
    });
}

// Initialize Category Doughnut Chart
function initCategoryChart(data = [45, 25, 20, 10]) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Enterprise', 'Consumer', 'E-commerce', 'Wholesale'],
            datasets: [{
                data: data,
                backgroundColor: [
                    '#4F46E5', // Primary
                    '#0ea5e9', // Secondary
                    '#8b5cf6', // Accent
                    'rgba(255, 255, 255, 0.1)'
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });
}

// Export initialization functions and instances
window.ForecastCharts = {
    initRevenueChart,
    initCategoryChart,
    getRevenueInstance: () => revenueChartInstance,
    getCategoryInstance: () => categoryChartInstance
};
