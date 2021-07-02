import base64
from pyDes import *
import jiosaavn


def format_song(data):
    global song_url
    song_data = {}
    artists = []
    media = {}
    try:
        song_url = data['media_preview_url']
        song_url = song_url.replace('preview', 'aac')
        song_url = song_url.replace('_96_p.mp4', '_96.mp4')
        media['96kbps'] = song_url
        song_url_160 = song_url.replace('_96.mp4', '_160.mp4')
        media['160kbps'] = song_url_160
        if data['320kbps'] == 'true':
            song_url_320 = song_url.replace('_96.mp4', '_320.mp4')
            media['320kbps'] = song_url_320
    except KeyError or TypeError:
        data['media_url'] = decrypt_url(data['encrypted_media_url'])
        if data['320kbps'] != "true":
            data['media_url'] = data['media_url'].replace("_320.mp4", "_160.mp4")

    song_data['singers'] = stringToArray(data['singers'])
    song_data['starring'] = stringToArray(data['starring'])
    song_data['media_url'] = media
    song_data['music'] = format_song_data(data['music'])
    song_data['album'] = format_song_data(data['album'])
    song_data["primary_artists"] = format_song_data(data["primary_artists"])
    song_data['image'] = data['image'].replace("150x150", "500x500")
    song_data['id'] = data['id']
    song_data['language'] = data['language']
    song_data['title'] = format_song_data(data['song'])
    song_data['play_count'] = data['play_count']
    song_data['has_lyrics'] = data['has_lyrics']
    song_data['release_date'] = data['release_date']
    song_data['320kbps'] = data['320kbps']
    song_data['duration'] = data['duration']
    for artist in data['artistMap']:
        artists.append(artist)
    song_data['artists'] = artists
    if data['has_lyrics'] == 'true':
        song_data['lyrics'] = jiosaavn.getLyrics(data['id'])
    return song_data


def stringToArray(raw_data):
    data_raw = format_song_data(raw_data)
    data_raw = data_raw.split(',')
    data_list = []
    for data in data_raw:
        if data != " ":
            data = data.lstrip()
            data = data.rstrip()
            if data != "":
                data_list.append(data)
    return data_list


def format_song_data(string):
    return string.encode().decode('unicode-escape').replace("&quot;", "'").replace("&amp;", "&").replace("&#039;", "'")


def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url
