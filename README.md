# SpotifySocket
 Websocket code for Neos spotify controller

This is the server code for the Spotify controller. The code will allow you to control your spotify client on your desktop inside of Neos. (This has not been tested with a non-premium account).

License:

These scripts are subject to the CC BY-NC 4.0 license, meaning you are free to take, modify, build upon, or remix the source code as long as credit is provided and that the use is non commercial. Read more here: https://creativecommons.org/licenses/by-nc/4.0/

## Features:

- See the song information, including the album icon
- Play, pause, skip, and play previous tracks
- Seek through your song with the progress bar
- Adjust the volume of your Spotify client
- Automatically syncs with your Spotify client on startup and during playback
- Search for songs and add them to your play queue
- Play from your public and private playlists (liked songs not supported)
- Share the music with your Neos friends with optional HTML streaming. Turn the controller into a player!

Here's how to get it working...

## Step 0, Installing Python:

This tool runs entirely on Python. If you don't have it, head over to https://www.python.org/ and grab yourself the latest stable copy.

## Step 1, Configuring Spotify:

This program requires a couple things from Spotify to get working. Head over to their developer website at https://developer.spotify.com/dashboard/login and log into your account. Then, click "Create an App". Then, enter a name and description. It can be anything, but if you plan on having multiple apps, you might want to use identifiable information. Read and agree to the terms and continue. Once your dashboard is loaded, click 'Edit settings', and find 'redirect URL'. Enter in 'http://localhost:8000', or for advanced users, the value in 'SPOTIPY_REDIRECT_URI'. Just make sure they're matching. Save those settings and click "show client secret". From there, you need to copy the client ID into 'SPOTIPY_CLIENT_ID' and the client secret into 'SPOTIPY_CLIENT_SECRET'. Don't forget the quotes!

## Step 2, Configuring streaming:

This program, along with the controller inside Neos, have the cool ability of easily transforming into a Spotify player you can use to play (and control!) your music with your friends. To do this, you will need a way to stream your audio with low latency. My setup, which introduces about 3 seconds of total lag, consists of VoiceMeeter to isolate Spotify's audio, and VLC to encode and stream it over HTML. Once you have this stream, copy the URL to the 'STREAM_URL' variable. The player in Neos will automatically start playing from it. Magic! 

## Step 3, In Neos:

Neos setup is easy! Just go into the SpotifySocket folder in my public and spawn it out. Crack it open in the inspector and go to the 'config' slot. You'll find a string valueField. Simply enter your name, and start the script. It should open a window on your desktop, asking for permissions to connect (this only happens when permissions are updated or the cache is lost, you'll likely need to only do this once). After that, you're done! Enjoy your tunes on your own, or with friends. The controller can be made completely local by enabling the "local toggle" and clicking it. Green means global. 

# Issues? Here are some known bugs/tips

- The script doesn't like it when spotify isn't playing when it starts. Make sure to have it running when you start the script and connect with Neos.
- Desyncs with the Neos can lead to crashes when pausing/playing. Just wait, Neos will attempt to connect again within 10 seconds, and the controller is built to sync itself on connect.
- Don't hear any audio after setting up the stream? Test it with VLC, and if it is indeed streaming, make sure your multimedia is turned up. The audio is localized at the player, so you will need to be close to it to hear. If none of that works, swap the playback engine back and forth in the "audio strem" slot. 
- Long latency using the stream function? Duplicate the player and delete the old copy, that ought to give you the most up to date stream.
- Scrolling through playlists can lead to pages being skipped due to the limitations of using a websocket. Simply click reset if there are issues.

Any questions or errors? PM me ingame or shoot me a discord message at Kodufan#7558. If you find this useful, feel free to toss me some NCR or KFC.
