const data = {
    /* labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], */
    datasets: [{
        label: 'Sales',
        data: [
            { x: new Date('2023-10-27T22:15:00'), y: 3 },
            { x: new Date('2023-10-28T20:50:00'), y: 10 },
            { x: new Date('2023-11-27T10:10:00'), y: 25 },
            { x: new Date('2023-12-27T16:15:00'), y: 9 },
            { x: new Date('2024-10-27T00:00:00'), y: 2 },
        ],
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 2.5,
        tension: 0.4,
        fill: true
    }]
};

// config 
const config_dwmy = {
    type: 'line',
    data,
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                },
                border: {
                    dash: [6,6]
                },
            },
            y: {
                beginAtZero: true,
                border: {
                    dash: [6,6],
                    color: 'rgba(102,102,102,1)'
                },
                
            }
        }
    }
};

const config_card = {
    type: 'line',
    data,
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                },
                border: {
                    display: false
                },
                grid: {
                    display: false
                },
                
            },
            y: {
                beginAtZero: true,
                border: {
                    display: false
                },
                grid: {
                    display: false
                }
            }
        }
    }
};

// render init block
const dwmy_chart = new Chart(
    document.getElementById('dwmy_chart'),
    config_dwmy
);

const card_chart_user = new Chart(
    document.getElementById('card_chart_user'),
    config_card
);

const card_chart_income = new Chart(
    document.getElementById('card_chart_income'),
    config_card
);

const card_chart_visitor = new Chart(
    document.getElementById('card_chart_visitor'),
    config_card
);

const card_chart_registrations = new Chart(
    document.getElementById('card_chart_registrations'),
    config_card
);


function dateFilter(time) {
    dwmy_chart.config.options.scales.x.time.unit = time;
    dwmy_chart.update();
    card_chart_user.config.options.scales.x.time.unit = time;
    card_chart_user.update();
    card_chart_income.config.options.scales.x.time.unit = time;
    card_chart_income.update();
    card_chart_visitor.config.options.scales.x.time.unit = time;
    card_chart_visitor.update();
    card_chart_registrations.config.options.scales.x.time.unit = time;
    card_chart_registrations.update();
}
