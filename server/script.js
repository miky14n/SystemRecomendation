function getRecommendations() {
    var animeName = document.getElementById('animeInput').value;

    fetch('/get_recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'anime_name': animeName })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('recommendations').innerHTML = data.recommendations.join('<br>');
    })
    .catch(error => console.error('Error:', error));
}
