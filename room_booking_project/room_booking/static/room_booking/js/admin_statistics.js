

const dwmy = document.getElementById('dwmy_chart').getContext('2d');
const ccu = document.getElementById('card_chart_user').getContext('2d');
const cci = document.getElementById('card_chart_income').getContext('2d');
const ccv = document.getElementById('card_chart_visitor').getContext('2d');
const ccr = document.getElementById('card_chart_registrations').getContext('2d');

// Sample data - Adapt this with your actual data
const data_ccu = {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [
        {  //  Line chart dataset #1
            type: 'line',
            label: 'Weekly Data',
            data: [20, 90, 70, 10, 40, 10, 50],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true
        }
    ]
}

const data_cci = {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [
        {  //  Line chart dataset #1
            type: 'line',
            label: 'Weekly Data',
            data: [20, 90, 70, 10, 40, 10, 50],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true
        }
    ]
}

const data_ccv = {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [
        {  //  Line chart dataset #1
            type: 'line',
            label: 'Weekly Data',
            data: [20, 90, 70, 10, 40, 10, 50],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true
        }
    ]
}

const data_ccr = {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [
        {  //  Line chart dataset #1
            type: 'line',
            label: 'Weekly Data',
            data: [20, 90, 70, 10, 40, 10, 50],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true
        }
    ]
}

const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
        {  //  Line chart dataset #1
            type: 'line',
            label: 'Line Data #1',
            data: [20, 30, 50, 20, 80, 60, 10, 40, 90, 50, 70, 100],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true // Enable fill for area under the line
        },
        {  //  Line chart dataset #2
            type: 'line',
            label: 'Line Data #2',
            data: [80, 20, 60, 100, 30, 90, 70, 10, 40, 10, 50, 20],
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 2, 
            tension: 0.4,
            fill: true 
        },
        {  //  Line chart dataset #3
            type: 'line',
            label: 'Line Data #3',
            data: [40, 70, 30, 90, 20, 50, 100, 60, 80, 10, 30, 40],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2, 
            tension: 0.4, 
            fill: true 
        }
    ]
};

const dwmy_chart = new Chart(dwmy, {
    data: data,
    options: {
        scales: {
            y: {
                ticks: { 
                    stepSize: 10 
                }
            }
        }
    }
});

const card_chart_user = new Chart(ccu, {
    data: data_ccu,
    options: {
        scales: {
            y: {
                ticks: { 
                    stepSize: 10 
                }
            }
        }
    }
});

const card_chart_income = new Chart(cci, {
    data: data_cci,
    options: {
        scales: {
            y: {
                ticks: { 
                    stepSize: 10 
                }
            }
        }
    }
});

const card_chart_visitor = new Chart(ccv, {
    data: data_ccv,
    options: {
        scales: {
            y: {
                ticks: { 
                    stepSize: 10 
                }
            }
        }
    }
});

const card_chart_registrations = new Chart(ccr, {
    data: data_ccr,
    options: {
        scales: {
            y: {
                ticks: { 
                    stepSize: 10 
                }
            }
        }
    }
});
