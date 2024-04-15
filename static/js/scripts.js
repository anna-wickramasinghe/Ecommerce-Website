document.addEventListener('DOMContentLoaded', function() {
    // Function to update dark mode toggle button text
    function updateDarkModeButtonText() {
        // Check if dark mode preference is stored in localStorage
        var darkModeEnabled = localStorage.getItem('darkModeEnabled');

        // Get the dark mode toggle button
        var darkModeToggle = document.getElementById('darkModeToggle');

        // Update button text based on dark mode state
        if (darkModeEnabled === 'true') {
            darkModeToggle.textContent = '☼';
            document.body.classList.add('dark-mode'); // Apply dark mode class to body
        } else {
            darkModeToggle.textContent = '☾';
            document.body.classList.remove('dark-mode'); // Remove dark mode class from body
        }
    }

    // Call the function to update button text when page loads
    updateDarkModeButtonText();

    // Add event listener to toggle dark mode
    document.getElementById('darkModeToggle').addEventListener('click', function() {
        // Toggle dark mode class on body
        document.body.classList.toggle('dark-mode');

        // Update dark mode preference in localStorage
        var darkModeEnabled = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkModeEnabled', darkModeEnabled);

        // Update dark mode toggle button text
        updateDarkModeButtonText();
    });
});
