from pip._internal import main as pipmain

try:
   from websockets import serve
except ImportError:
    pipmain(['install', 'websockets'])
    from websockets import serve

try:
   import spotipy
except ImportError:
    pipmain(['install', 'spotipy'])
    import spotipy

try:
   import yaml
except ImportError:
    pipmain(['install', 'pyyaml'])
    import yaml

import asyncio
import datetime
import os
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime



def get_time():
        time = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]:")
        return time

filePath = os.getcwd() + "\\config.yml"
with open(filePath, "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

SPOTIPY_CLIENT_ID = cfg["spotify"]["clientID"]
SPOTIPY_CLIENT_SECRET = cfg["spotify"]["clientSecret"]
SPOTIPY_REDIRECT_URI = cfg["spotify"]["redirectURI"]
SCOPE = cfg["spotify"]["scope"]
CACHE = cfg["spotify"]["cache"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,cache_path=CACHE,open_browser=True))

test = sp.devices()

print(get_time() + " Connected to Spotify successfully!")

async def server(websocket, path):
    # this code runs for each connected client
    result = sp.current_playback()
    devices = sp.devices()
    tempstatus = '!init'
    PLAY_STATUS = result['shuffle_state']
    if PLAY_STATUS:
        tempstatus += 'True\t'
    else:
        tempstatus += 'False\t'
    REPEAT_STATUS = result['repeat_state']
    if REPEAT_STATUS == "off":
        tempstatus += '0\t'
    elif REPEAT_STATUS == "context":
        tempstatus += '1\t'
    elif REPEAT_STATUS == "track":
        tempstatus += "2\t"
    tempstatus += str(result['is_playing']) + "\t\t\t\t\t"

    await websocket.send(tempstatus)
    print (get_time(),'Client connected!')
    results = ""
    playlists = sp.current_user_playlists()
    playlistarr = []

    for i in range(len(playlists['items'])):
        name = playlists['items'][i]['name']
        icon = playlists['items'][i]['images'][0]['url']
        playlistarr.append(name + "\b" + icon)

    try:
        async for message in websocket:
            
                # this runs for each message a client sends a message
                # message format
                # command\tsearchquery\textra1\textra2

                command = message.split(";")[0]
                query = message.split(";")[1]
                extra1 = message.split(";")[2]
                extra2 = message.split(";")[3]
                if command == 'current':
                    result = sp.current_playback()
                    try:
                        ARTIST = ""
                        for i in result['item']['artists']:
                            ARTIST += i['name'] + ", "  
                        ARTIST = ARTIST[:-2]
                        ALBUM = result['item']['album']['name']
                        ALBUM_IMG = result['item']['album']['images'][1]['url']
                        TITLE = result['item']['name']
                        SONG_PROGRESS = result['progress_ms']
                        SONG_DURATION = result['item']['duration_ms']
                        PLAY_STATUS = result['is_playing']
                        VOLUME = result['device']['volume_percent']
                        await websocket.send("!current" + 
                            ARTIST + "\t" + 
                            ALBUM + "\t" + 
                            ALBUM_IMG + "\t" +
                            TITLE + "\t" + 
                            str(VOLUME) + "\t" + 
                            str(SONG_PROGRESS) + "\t" + 
                            str(SONG_DURATION) + "\t" + 
                            str(PLAY_STATUS))
                    except:
                        await websocket.send("!statusFatal error in fetching current info")
                            
                elif command == 'next':
                    sp.next_track()
                    await websocket.send('!statusPlaying next track')

                elif command == 'previous':
                    sp.previous_track()
                    await websocket.send('!statusPlaying previous track')

                elif command == 'pause':
                    try:
                        sp.pause_playback()
                    except:
                        await websocket.send('!statusFailed to pause')
                    await websocket.send('!statusPaused')

                elif command == 'resume':
                    try:
                        sp.start_playback()
                    except:
                        await websocket.send('!statusFailed to resume')
                    await websocket.send('!statusPlaying')

                elif command == 'volume':
                    try:
                        sp.volume(volume_percent=int(extra1))
                        await websocket.send('!statusVolume set to: ' + extra1)
                    except spotipy.exceptions.SpotifyException:
                        await websocket.send('!statusError adjusting volume, it might not be allowed on your selected device')
                    
                elif command == 'shuffle':
                    sp.shuffle(state=True)

                elif command == 'shuffle_off':
                    sp.shuffle(state=False)

                elif command == 'repeat':
                    sp.repeat(state='context')

                elif command == 'repeat_off':
                    sp.repeat(state='off')

                elif command == 'repeat_one':
                    sp.repeat(state='track')

                elif command == 'search':
                    if (query == '') :
                        continue
                    cache_num = 25
                    results = sp.search(query, limit = cache_num)

                    output = "!search"

                    if extra2 == "nameartistcover":
                        for i in range(len(results['tracks']['items'])):
                            track = str(results['tracks']['items'][i]['name'])
                            artist = ""
                            for j in range(len(results['tracks']['items'][i]['artists'])):
                                artist += str(results['tracks']['items'][i]['artists'][j]['name']) + ", "
                            artist = artist[:-2]
                            try: 
                                cover = str(results['tracks']['items'][i]['album']['images'][1]['url'])
                            except IndexError:
                                cover = "https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png"
                            output += (track + "\b" + artist + "\b" + cover + "\n")
                        output += "\t\t\t\t\t\t\t"

                    output = output[:-2]
                    await websocket.send(str(output))

                elif command == 'addqueue':
                    if extra2 == 'fromsearch':
                        sp.add_to_queue(results['tracks']['items'][int(extra1)]['id'])
                    await websocket.send('!status')

                elif command == 'playplaylist':
                    sp.start_playback(context_uri=playlists['items'][int(extra1)]['uri'])

                elif command == 'getplaylists':
                    output = '!playlists'
                    for i in range(len(playlistarr)):
                        output += playlistarr[i] + "\n"
                    output = output[:-2]
                    output += "\t\t\t\t\t\t\t"
                    await websocket.send(output)

                elif command == 'seek':
                    sp.seek_track(int(extra1))
                else:
                    await websocket.send("!statusUnknown Command")
    except:
        print (get_time(),'Client disconnected!')

async def main():
    async with serve(server, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())