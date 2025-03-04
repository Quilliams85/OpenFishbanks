function animateTimeChange(element, newTime) {
    let currentTime = element.textContent;
    let targetTime = newTime;

    // If current and target time are the same, skip the animation
    if (currentTime === targetTime) {
        return;
    }

    // Fade out the time part
    element.style.opacity = 0;

    setTimeout(() => {
        // Update the time after fade out
        element.textContent = targetTime;

        // Fade in the new time
        element.style.opacity = 1;
    }, 300); // Delay matches the CSS transition duration
}

function updateGameTime() {
    fetch('/api/get-time/')
        .then(response => response.json())
        .then(data => {
            // Extract the static and dynamic parts of the date-time string
            let dateTime = data.time; // e.g., "1972-02-03 09:59:47"
            let [datePart, timePart] = dateTime.split(' '); // Split into date and time

            // Update the static date part (does not change)
            document.getElementById('game-date').textContent = datePart;

            // Apply the fade effect to only the time part
            let timeElement = document.getElementById('game-time');
            animateTimeChange(timeElement, timePart);
        })
        .catch(error => console.error('Error fetching time:', error));
}

// Update the time every second
setInterval(updateGameTime, 3000);
updateGameTime();
