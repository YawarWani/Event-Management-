document.addEventListener('DOMContentLoaded', async () => {
    const loadingOverlay = document.getElementById('loading-overlay'); // Get the loader element
    const registrationBtns = document.querySelectorAll('.registration-btn'); // All buttons

    // Function to check if registration is open
    async function checkRegistrationStatus(eventId) {
        try {
            const response = await fetch(`/check_registration_status/${eventId}`);
            const data = await response.json();
            return data.is_open; // Return true if registration is open
        } catch (error) {
            console.error('Error checking registration status:', error);
            return false; // Default to closed on error
        }
    }

    // Function to check user's registration status and update button
    async function updateRegistrationStatus(eventId, btn) {
        try {
            const response = await fetch(`/check_registration/${eventId}`);
            const data = await response.json();

            if (data.is_registered) {
                btn.textContent = 'Registered';
                btn.disabled = true;
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-success');
            } else {
                btn.textContent = 'Register';
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Error checking registration:', error);
            btn.textContent = 'Register';
        }
    }

    // Function to update all buttons
    async function updateAllButtons() {
        const promises = [];

        registrationBtns.forEach((btn) => 
            {
            const eventId = btn.getAttribute('data-event-id');

            const updatePromise = (async () =>
                {
                const isOpen = await checkRegistrationStatus(eventId);

                if (!isOpen) 
                    {
                    btn.textContent = 'Closed';
                    btn.disabled = true;
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-secondary');
                } else {
                    await updateRegistrationStatus(eventId, btn);
                }

                const form = document.getElementById(`registration-form-${eventId}`);
                form.addEventListener('submit', async (e) => 
                    {
                    e.preventDefault();
                    try {
                        const response = await fetch('/register_event', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ event_id: eventId }),
                        });

                        const data = await response.json();

                        if (data.success) {
                            btn.textContent = 'Registered';
                            btn.disabled = true;
                            btn.classList.remove('btn-primary');
                            btn.classList.add('btn-success');
                            alert('Successfully registered for the event!');
                        } else {
                            alert(data.message || 'Registration failed');
                        }
                    } catch (error) {
                        console.error('Registration error:', error);
                        alert('An error occurred during registration');
                    }
                });
            })();

            promises.push(updatePromise); // Collect all promises
        });

        await Promise.all(promises);
    }

    await updateAllButtons();
    loadingOverlay.style.display = 'none'; 
});

function setFilter(filterType) {
    const searchInput = document.getElementById('searchInput');
    const filterInput = document.getElementById('filterInput');

    filterInput.value = filterType;

    if (filterType === 'date') {
        searchInput.type = 'date';
        searchInput.placeholder = 'Search by Date';

    }

    else {
        searchInput.type = 'search';
        searchInput.placeholder = 'Search by Name';
    }
}