fetch('http://localhost:8000/api/v1/basket/basket/4/add_item', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        'service': 1,
        'quantity': 1,
    }),
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    // Handle the response data here
    console.log(data); // You can process the response data here
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});
