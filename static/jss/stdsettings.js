document.addEventListener('DOMContentLoaded', () => {
    const notificationBtn = document.getElementById('notification-btn');
    const notificationDropdown = document.getElementById('notification-dropdown');
    
    const statusBtn = document.getElementById('status-btn');
    const statusDropdown = document.getElementById('status-dropdown');
    
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    // Toggle dropdown visibility
    notificationBtn.addEventListener('click', () => {
        toggleDropdown(notificationDropdown);
        closeOthers([statusDropdown, profileDropdown]);
    });

    statusBtn.addEventListener('click', () => {
        toggleDropdown(statusDropdown);
        closeOthers([notificationDropdown, profileDropdown]);
    });

    profileBtn.addEventListener('click', () => {
        toggleDropdown(profileDropdown);
        closeOthers([notificationDropdown, statusDropdown]);
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.header-right')) {
            closeDropdowns();
        }
    });

    function toggleDropdown(dropdown) {
        dropdown.classList.toggle('show');
    }

    function closeDropdowns() {
        notificationDropdown.classList.remove('show');
        statusDropdown.classList.remove('show');
        profileDropdown.classList.remove('show');
    }

    function closeOthers(dropdowns) {
        dropdowns.forEach(dropdown => dropdown.classList.remove('show'));
    }

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('change', function() {
        document.body.classList.toggle('dark');
        document.querySelector('.container').classList.toggle('dark');
        document.querySelector('header').classList.toggle('dark');
        document.querySelectorAll('.header-right button').forEach(button => button.classList.toggle('dark'));
        document.querySelectorAll('.dropdown').forEach(dropdown => dropdown.classList.toggle('dark'));
        document.querySelectorAll('.stat').forEach(stat => stat.classList.toggle('dark'));
        document.querySelectorAll('.option').forEach(option => option.classList.toggle('dark'));
    });
});

function switchUser() {
    // Add your code to switch user here
    alert('Switch User functionality is not implemented yet.');
}

function logout() {
    // Add your code to log out here
    alert('Logout functionality is not implemented yet.');
}
