import json
import requests
import endpoints
import formatter


def search_for_song(query):
    song_dict = {
        'success': True,
        'data': [],
        'query': query
    }
    if query.startswith('http') and 'saavn.com' in query:
        song_id = get_song_id(query)
        return get_song(song_id)

    search_base_url = endpoints.search_base_url + query
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    response = json.loads(response)
    song_response = response['songs']['data']
    songs = []
    for song in song_response:
        song_id = song['id']
        song_data = get_song(song_id)
        if song_data:
            songs.append(song_data)
    song_dict['data'] = songs
    return song_dict


def get_song(song_id):
    search_base_url = endpoints.song_details_base_url + song_id
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    response = json.loads(response)
    song_data = formatter.format_song(response[song_id])
    if song_data:
        return song_data
    else:
        return None


def getLyrics(song_id):
    search_base_url = endpoints.lyrics_base_url + song_id
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    response = json.loads(response)
    return response['lyrics']


def get_song_id(query):
    res = requests.get(query, data=[('bitrate', '320')])
    try:
        return res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
    except IndexError:
        return (res.text.split('"pid":"'))[1].split('","')[0]
