document.addEventListener('DOMContentLoaded', function() {
    const synopsisText = document.querySelector('.synopsis-text');
    const editableContent = document.querySelector('.edit-container');
    const editTextarea = document.querySelector('.edit-textarea');
    const stars = document.querySelectorAll('.star');
    const showElement = document.querySelector('.show');

    // Function to toggle the edit container visibility
    function toggleEditContainer() {
        editableContent.style.display = (editableContent.style.display === 'none') ? 'block' : 'none';

        if (editableContent.style.display === 'block') {
            editTextarea.value = synopsisText.textContent;
        }
    }

    // Function to handle the click event on the save edit button
    function handleSaveEditButtonClick(event) {
        event.preventDefault();

        const showId = showElement.getAttribute('data-show-id');

        const editTextarea = document.querySelector('.edit-textarea');
        const editedDescription = editTextarea.value;

        fetch(`/edit_show`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,  
            },
            body: JSON.stringify({ description: editedDescription , show_id: showId}),
        })
        .then(response => response.json())
        .then(data => {
            // Update the show description on success
            if (data.success) {
                synopsisText.textContent = editedDescription;
                toggleEditContainer();  // Hide the edit container after saving
            } else {
                console.error('Failed to save edited description');
            }
        });
    }

    stars.forEach(star => {
        star.addEventListener('mouseover', function() {
            this.style.color = 'orange'; // Change color on hover
            let previousStars = this.previousElementSibling;
            while (previousStars) {
                previousStars.style.color = 'orange'; // Change color for stars to the left
                previousStars = previousStars.previousElementSibling;
            }
        });
    
        star.addEventListener('mouseout', function() {
            this.style.color = 'grey'; // Change back to initial color
            let previousStars = this.previousElementSibling;
            while (previousStars) {
                previousStars.style.color = 'grey'; // Change back color for stars to the left
                previousStars = previousStars.previousElementSibling;
            }
        });
    });

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');

            // Capture the 'rating' value from the clicked star
            alert(`You rated this show ${rating} stars!`);

            const showId = showElement.getAttribute('data-show-id');
            fetch(`/show/${showId}/rate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token,
                },
                body: JSON.stringify({ stars: rating }),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    console.log(response.status);
                    throw new Error('Failed to rate the show.');
                }
            }).then(data =>{
                console.log(`Show has been rated ${rating} stars.`);
                console.log(typeof data.average_rating);
                updateRatingUI(data.average_rating.toFixed(2), data.total_ratings);
            })
            .catch(error => {
                console.log(error);
            });
        });
    });
      
    function updateRatingUI(averageRating, totalRatings) {
        const showRatingElement = document.querySelector('.show-rating');
        showRatingElement.innerHTML = `Rating: ${averageRating}/5 (${totalRatings} users)`;
    }

    // Attach event listener to the edit button
    const editShowbutton = document.querySelector('.edit-show-btn');
    if (editShowbutton) {
        editShowbutton.addEventListener('click', toggleEditContainer);
    }
 
    // Attach event listener to the save edit button
    const saveEditbutton = document.querySelector('.save-edit-btn');
    if (saveEditbutton) {
        saveEditbutton.addEventListener('click', handleSaveEditButtonClick);
    }



});
