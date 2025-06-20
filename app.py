from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow calls from frontend (localhost or your domain)

@app.route('/billboard', methods=['GET'])
def get_top_10_songs():
    birthday = request.args.get('date')  # expects format YYYY-MM-DD
    if not birthday:
        return jsonify({"error": "Missing 'date' query parameter"}), 400

    url = f'https://www.billboard.com/charts/hot-100/{birthday}/'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': f"Failed to fetch Billboard chart for {birthday}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    chart_items = soup.select('li.o-chart-results-list__item')

    songs = []
    for item in chart_items:
        title_tag = item.select_one('h3.c-title')
        artist_tag = item.select_one('span.c-label')
        if title_tag and artist_tag:
            song = title_tag.get_text(strip=True)
            artist = artist_tag.get_text(strip=True)
            songs.append(f"{len(songs) + 1}. {song} by {artist}")
        if len(songs) == 10:
            break

    return jsonify({'songs': songs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
