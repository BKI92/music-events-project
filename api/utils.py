import requests

API_KEY = '7956b85bf637a83170b24efead48a2c4'
USER_AGENT = 'Dataquest'
headers = {
    'user-agent': USER_AGENT
}

URL = 'http://ws.audioscrobbler.com/2.0/'
PAYLOAD = {
    'api_key': API_KEY,
    'method': 'track.search',
    'format': 'json',
}


def get_tracks(url: str, payload: dict, name: str, artist: str,
               limit: int) -> list or None:
    payload['track'] = name
    if artist:
        payload['artist'] = artist
    response = requests.get(url, params=payload).json()
    if limit:
        payload['limit'] = limit

    if response:
        return response.get('results').get('trackmatches').get('track')
    return


def refactor_results(tracks):
    if tracks:
        final_data = []
        for number, track in enumerate(tracks):
            name_value, artist_value, url_value = track.get('name'), track.get(
                'artist'), track.get('url')
            final_data.append({'temp_id': number,
                               'name': name_value,
                               'artist': artist_value,
                               'url': url_value})
        return final_data
    return

# print(refactor_results(get_tracks(URL, PAYLOAD, 'Belive')))
