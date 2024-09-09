// Function to toggle dropdown
function toggleDropdown(event) {
    const buttonId = event.currentTarget.id;
    const dropdownId = buttonId.replace('-btn', '-dropdown');
    const dropdown = document.getElementById(dropdownId);

    // Hide all dropdowns
    document.querySelectorAll('.dropdown').forEach(d => {
        if (d !== dropdown) {
            d.classList.remove('show');
        }
    });

    // Toggle the visibility of the clicked dropdown
    dropdown.classList.toggle('show');

    // Adjust dropdown position
    const rect = event.currentTarget.getBoundingClientRect();
    dropdown.style.left = `0`; // Align with the button's left edge
    dropdown.style.top = `${event.currentTarget.offsetHeight}px`; // Position it below the button

    // Prevent the event from propagating to the document
    event.stopPropagation();
}

// Attach event listeners to buttons
document.querySelectorAll('.header-right button').forEach(button => {
    button.addEventListener('click', toggleDropdown);
});

// Close dropdowns if clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown').forEach(d => {
        d.classList.remove('show');
    });
});