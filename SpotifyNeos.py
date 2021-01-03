import asyncio
import datetime
from requests.api import get
import websockets
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime


SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8000'
SCOPE = "user-library-modify,user-library-read,user-read-currently-playing,user-read-playback-position,user-read-playback-state,user-modify-playback-state,app-remote-control,streaming,playlist-read-private,playlist-modify-private,playlist-modify-public"
CACHE = '.spotipyoauthcache'
STREAM_URL = ''

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,cache_path=CACHE,open_browser=True))


async def echo(websocket, path):

    def get_time():
        time = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]:")
        return time

    # this code runs for each connected client

    try: 
        result = sp.current_playback()
        devices = sp.devices()
        tempstatus = '!init'
        PLAY_STATUS = result['shuffle_state']
        if PLAY_STATUS:
            tempstatus += 'True\!'
        else:
            tempstatus += 'False\!'
        REPEAT_STATUS = result['repeat_state']
        if REPEAT_STATUS == "off":
            tempstatus += 'False\!'
        elif REPEAT_STATUS == "context":
            tempstatus += 'True\!'
        tempstatus += str(result['is_playing']) + "\!" + STREAM_URL + "\!\!\!\!"

        await websocket.send(tempstatus)
        print (get_time(),'Client connected!')
        results = ""
        playlists = sp.current_user_playlists()
        playlistarr = []
        playtracks = ""
        eye = 0
        while True:
            temp = [''] * 5
            try:
                for i in range(5):
                    temp.insert(i,playlists['items'][eye]['name'])
                    temp.pop(len(temp) - 1)
                    eye += 1
                playlistarr.append(temp)
            except IndexError:
                    playlistarr.append(temp)
                    break
        eye = 0
        device_id = devices['devices'][0]['id']

        async for message in websocket:

            # this runs for each message a client sends a message
            # message format
            # command\!searchquery\!extra1\!extra2

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
                        ARTIST + "\!" + 
                        ALBUM + "\!" + 
                        ALBUM_IMG + "\!" +
                        TITLE + "\!" + 
                        str(VOLUME) + "\!" + 
                        str(SONG_PROGRESS) + "\!" + 
                        str(SONG_DURATION) + "\!" + 
                        str(PLAY_STATUS))
                except:
                    await websocket.send("!statusFatal error in fetching current info")
                          
            elif command == 'next':
                #sp.next_track(device_id=device_id)
                sp.next_track()
                await websocket.send('!statusPlaying next track')

            elif command == 'previous':
                #sp.previous_track(device_id=device_id)
                sp.previous_track()
                await websocket.send('!statusPlaying previous track')

            elif command == 'pause':
                #sp.pause_playback(device_id=device_id)
                sp.pause_playback()
                await websocket.send('!statusPaused')

            elif command == 'resume':
                #sp.start_playback(device_id=device_id)
                sp.start_playback()
                await websocket.send('!statusPlaying')

            elif command == 'volume':
                try:
                    #sp.volume(volume_percent=int(extra1), device_id=device_id)
                    sp.volume(volume_percent=int(extra1))
                    await websocket.send('!statusVolume set to: ' + extra1)
                except spotipy.exceptions.SpotifyException:
                    await websocket.send('!statusError adjusting volume, it might not be allowed on your selected device')
                
            elif command == 'shuffle':
                #sp.shuffle(state=True, device_id=device_id)
                sp.shuffle(state=True)

            elif command == 'shuffle_off':
                #sp.shuffle(state=False, device_id=device_id)
                sp.shuffle(state=False)

            elif command == 'repeat':
                #sp.repeat(state='context', device_id=device_id)
                sp.repeat(state='context')

            elif command == 'repeat_off':
                #sp.repeat(state='off', device_id=device_id)
                sp.repeat(state='off')

            elif command == 'search':
                output = "!search"
                count = 0
                if extra2 == "nameonly":
                    for i in range(min(5,len(results['tracks']['items']))):
                        output += str(results['tracks']['items'][int(i) + int(extra1)]['name']) + "\!"
                        count += 1
                    for i in range(8 - count):
                        output += "\!"
                elif extra2 == "nameartist":
                    for i in range(min(5,len(results['tracks']['items']))):
                        output += str(results['tracks']['items'][i + int(extra1)]['name']) + "\n" + str(results['tracks']['items'][i + int(extra1)]['artists'][0]['name']) + "\!"
                        count += 1
                    for i in range(8 - count):
                        output += "\!"

                elif extra2 == "nameartistalbum":
                    for i in range(min(5,len(results['tracks']['items']))):
                        output += str(results['tracks']['items'][i + int(extra1)]['name']) + "\n" 
                        + str(results['tracks']['items'][i + int(extra1)]['artists'][0]['name']) 
                        + "\n" + str(results['tracks']['items'][i + int(extra1)]['album']['name']) + "\!"
                        count += 1
                    for i in range(8 - count):
                        output += "\!"

                output = output[:-2]
                await websocket.send(str(output))

            elif command == 'searchcache':
                cache_num = 25
                results = sp.search(query, limit = cache_num)
                await websocket.send("!statusSearched for " + query)

            elif command == 'addqueue':
                if extra2 == 'fromsearch':
                    #sp.add_to_queue(results['tracks']['items'][int(extra1)]['id'],device_id=device_id)
                    sp.add_to_queue(results['tracks']['items'][int(extra1)]['id'])
                elif extra2 == 'fromplaylist':
                    #sp.add_to_queue(playtracks['tracks']['items'][int(extra1)]['track']['id'],device_id=device_id)
                    sp.add_to_queue(playtracks['tracks']['items'][int(extra1)]['track']['id'])
                await websocket.send('!status')

            elif command == 'playplaylist':
                #sp.start_playback(context_uri=playlists['items'][(eye * 5) + int(extra1)]['uri'],device_id=device_id)
                sp.start_playback(context_uri=playlists['items'][(eye * 5) + int(extra1)]['uri'])

            elif command == 'getplaylists':
                output = '!playlists'
                if (extra1 == 'nextpage' and eye < len(playlistarr) - 1):
                    eye += 1  
                    for i in playlistarr[eye]:
                        output += i + '\!'
                elif (extra1 == 'prevpage' and eye > 0):
                    eye -= 1
                    for i in playlistarr[eye]:
                        output += i + '\!'
                elif extra1 == 'init':
                    eye = 0
                    for i in playlistarr[eye]:
                        output += i + '\!'
                else:
                    for i in playlistarr[eye]:
                        output += i + '\!'
                output += "\!\!"
                await websocket.send(output)

            elif command == 'getplaylistsongs':
                playtracks = sp.playlist(playlists['items'][int(extra1)]['id'])
                #print(playtracks)
                output = ""
                for i in playtracks['tracks']['items']:
                    output += str(eye) + '. ' + i['track']['name'] + '\!'
                    eye += 1
                await websocket.send(output)

            elif command == 'showdevices':
                devices = sp.devices()
                output = '!devices'
                count = 0
                for i in devices['devices']:
                    output += i['name'] + "\!"
                    count += 1
                for i in range(8 - count):
                    output += "\!"
                output = output[:-2]
                await websocket.send(output)
            
            elif command == 'selectdevice':   
                sp.transfer_playback(device_id=device_id, force_play=True)
                device_id = devices['devices'][int(extra1)]['id']
                await websocket.send(devices['devices'][int(extra1)]['name'] + "\!\!\!\!\!\!\!")
            
            elif command == 'seek':
                sp.seek_track(int(extra1))

            elif command == 'addfavorite':
                a = bool(sp.current_user_saved_tracks_contains(tracks=[result['item']['id']]))
                print (str(a))
                print (result['item']['name'])
                if a:
                    sp.current_user_saved_tracks_delete(tracks=[result['item']['id']])
                    print ('contains!')
                else:
                    sp.current_user_saved_tracks_add(tracks=[result['item']['id']])
                    print('don\'t contains!')

                #print (str(sp.current_user_saved_tracks_contains(tracks=[result['item']['id']])))

            else:
                await websocket.send("!statusUnknown Command")
    except websockets.exceptions.ConnectionClosedError: 
        print(get_time(),"Client disconnected")
    except spotipy.SpotifyException as e:
        print(get_time(),e)
        await websocket.send('!status{e}')


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()