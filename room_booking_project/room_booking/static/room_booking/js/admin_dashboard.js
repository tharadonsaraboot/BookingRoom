$(document).ready(function() {
    fetch('/user-data/')
        .then(response => response.json())
        .then(data => {
            $('#total-users').text('Total Users: ' + data.total_users);
            $('#users-with-bookings').text('Users with Bookings: ' + data.users_with_bookings);

            const userList = $('#user-list');
            data.user_list.forEach(user => {
                userList.append(`<li>${user.username} (${user.first_name} ${user.last_name})</li>`);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
