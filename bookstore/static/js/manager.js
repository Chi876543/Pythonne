let revenueChartInstance = null;
let inventoryChartInstance = null;
let stockChartInstance = null;

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(tabName).classList.add('active');
    document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');
}

function updateRevenueInputs() {
    const timeUnit = document.getElementById('timeUnit').value;
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');

    if (timeUnit === 'month') {
        startDate.type = 'month';
        endDate.type = 'month';
        startDate.value = '';
        endDate.value = '';
    } else if (timeUnit === 'year') {
        startDate.type = 'text';
        endDate.type = 'text';
        startDate.placeholder = 'YYYY';
        endDate.placeholder = 'YYYY';
        startDate.pattern = '\\d{4}';
        endDate.pattern = '\\d{4}';
        startDate.value = '';
        endDate.value = '';
    } else {
        startDate.type = 'date';
        endDate.type = 'date';
        startDate.placeholder = '';
        endDate.placeholder = '';
        startDate.pattern = '';
        endDate.pattern = '';
        startDate.value = '';
        endDate.value = '';
    }
}

function updateStockInputs() {
    const timeUnit = document.getElementById('stockTimeUnit').value;
    const startDate = document.getElementById('stockStartDate');
    const endDate = document.getElementById('stockEndDate');

    if (timeUnit === 'month') {
        startDate.type = 'month';
        endDate.type = 'month';
        startDate.value = '';
        endDate.value = '';
    } else {
        startDate.type = 'date';
        endDate.type = 'date';
        startDate.value = '';
        endDate.value = '';
    }
}

function validateDateRange(start, end, period) {
    if (!start || !end) {
        alert('Vui lòng chọn ngày bắt đầu và kết thúc!');
        return false;
    }

    let startDate, endDate;

    if (period === 'day') {
        startDate = new Date(start);
        endDate = new Date(end);
        const diffDays = (endDate - startDate) / (1000 * 60 * 60 * 24);
        if (diffDays > 7) {
            alert('Khoảng thời gian giới hạn chỉ 7 ngày');
            return false;
        }
    } else if (period === 'month') {
        startDate = new Date(start + '-01');
        endDate = new Date(end + '-01');
        const diffMonths = (endDate.getFullYear() - startDate.getFullYear()) * 12 +
            (endDate.getMonth() - startDate.getMonth());
        if (diffMonths > 3) {
            alert('Giới hạn tháng là 3 tháng!');
            return false;
        }
    } else if (period === 'year') {
        startDate = parseInt(start, 10);
        endDate = parseInt(end, 10);
        if (endDate - startDate > 5) {
            alert('Tối đa 5 năm!');
            return false;
        }
    }

    return true;
}

function formatDateForApi(start, end, period) {
    if (period === 'month') {
        const endDate = new Date(end + '-01');
        const lastDay = new Date(endDate.getFullYear(), endDate.getMonth() + 1, 0).getDate();
        return { start: start + '-01', end: end + '-' + lastDay };
    } else if (period === 'year') {
        return { start: start + '-01-01', end: end + '-12-31' };
    }
    return { start, end };
}

function generateRevenueChart() {
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;
    const period = document.getElementById('timeUnit').value;

    if (!validateDateRange(start, end, period)) {
        return;
    }

    const { start: apiStart, end: apiEnd } = formatDateForApi(start, end, period);

    fetch('/api/revenue/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start: apiStart, end: apiEnd, period })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            if (data.labels.length === 0) {
                alert('Không có dữ liệu!');
                return;
            }

            if (revenueChartInstance) {
                revenueChartInstance.destroy();
            }

            const ctx = document.getElementById('revenueChart').getContext('2d');
            revenueChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Revenue',
                            data: data.revenues,
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                            fill: false
                        },
                        {
                            label: 'Order Count',
                            data: data.order_counts,
                            backgroundColor: 'rgba(153, 102, 255, 0.2)',
                            borderColor: 'rgba(153, 102, 255, 1)',
                            borderWidth: 1,
                            fill: false,
                            hidden: true
                        }
                    ]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Amount' } },
                        x: { title: { display: true, text: period.charAt(0).toUpperCase() + period.slice(1) } }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra!');
        });
}

function generateInventoryChart() {
    fetch('/api/inventory/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            if (data.labels.length === 0) {
                alert('Không có dữ liệu!');
                return;
            }

            if (inventoryChartInstance) {
                inventoryChartInstance.destroy();
            }

            const ctx = document.getElementById('inventoryChart').getContext('2d');
            inventoryChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Stock',
                        data: data.stocks,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Stock Quantity' } },
                        x: { title: { display: true, text: 'Category' } }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi đã xảy ra!');
        });
}

function generateStockChart() {
    const start = document.getElementById('stockStartDate').value;
    const end = document.getElementById('stockEndDate').value;
    const period = document.getElementById('stockTimeUnit').value;

    if (!validateDateRange(start, end, period)) {
        return;
    }

    const { start: apiStart, end: apiEnd } = formatDateForApi(start, end, period);

    fetch('/api/stock/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start: apiStart, end: apiEnd, period })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            if (data.labels.length === 0) {
                alert('Không có dữ liệu!');
                return;
            }

            if (stockChartInstance) {
                stockChartInstance.destroy();
            }

            const ctx = document.getElementById('importExportChart').getContext('2d');
            stockChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Stock In',
                            data: data.stock_in,
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                            fill: false
                        },
                        {
                            label: 'Stock Out',
                            data: data.stock_out,
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            fill: false
                        }
                    ]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Quantity' } },
                        x: { title: { display: true, text: period.charAt(0).toUpperCase() + period.slice(1) } }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra!');
        });
}

// Khởi tạo input khi tải trang
document.addEventListener('DOMContentLoaded', function() {
    updateRevenueInputs();
    updateStockInputs();
});