document.querySelectorAll('.vote-btn').forEach(button => {
    button.addEventListener('click', function () {
        const answerId = this.dataset.id;    // get answer ID
        const value = this.dataset.value;    // get vote type (1 or -1)

        fetch("{% url 'voting' %}", {        // call Django view
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `id=${answerId}&value=${value}`
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                // update vote counts without refreshing
                document.getElementById(`upvotes-${answerId}`).innerText = data.upvotes;
                document.getElementById(`downvotes-${answerId}`).innerText = data.downvotes;
            }
        })
        .catch(error => console.log("Error:", error));
    });
});

