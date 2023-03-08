const form = document.querySelector('#form');
const urlsInput = document.querySelector('#urls');
const resultsDiv = document.querySelector('#results');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Retrieve the input URLs
    const urls = urlsInput.value.split(',');

    // Send the URLs to the Flask app using a POST request
    const response = await fetch('/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ urls: urls })
    });

    // Display the results
    const results = await response.json();
    resultsDiv.innerHTML = '';
    results.forEach(result => {
        const p = document.createElement('p');
        p.innerText = result;
        resultsDiv.appendChild(p);
    });
});
