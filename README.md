# SpotifySocket
 Websocket code for Neos spotify controller

This is the server code for the Spotify controller. The code will allow you to control your spotify client from inside of Neos. (Premium account required).

License:

These scripts are subject to the CC BY-NC 4.0 license, meaning you are free to take, modify, build upon, or remix the source code as long as credit is provided and that the use is non commercial. Read more here: https://creativecommons.org/licenses/by-nc/4.0/

## Features:

- See the song information, including the album icon
- Play, pause, skip, and play previous tracks
- Seek through your song with the progress bar
- Automatically syncs with your Spotify client on startup and during playback
- You and your friends can all use the player, however you can disable others from interacting with it
- Play from your public and private playlists (liked songs not supported)
- Share the music with your Neos friends with optional streaming. Turn the controller into a player!

Here's how to get it working...

## Step 0, Installing Python:

This tool runs entirely on Python. If you don't have it, head over to https://www.python.org/ and grab yourself the latest stable copy.

## Step 1, Configuring Spotify:

This program requires a couple things from Spotify to get working. Head over to their developer website at https://developer.spotify.com/dashboard/login and log into your account. Then, click "Create an App". Then, enter a name and description. It can be anything, but if you plan on having multiple apps, you might want to use identifiable information. Read and agree to the terms and continue. Once your dashboard is loaded, click 'Edit settings', and find 'redirect URL'. Enter in 'http://localhost:8000'. Save those settings and click "show client secret". From there, you need to copy the client ID, client secret, and redirect URL into the config file.

## Step 2, In Neos:

Neos setup is easy! Just go into the SpotifySocket folder in my public and spawn it out, then click the connect button. It should open a window on your desktop, asking for permissions to connect to your local server (you only need to do this once). After that, you're done! Enjoy your tunes on your own, or with friends. The controller can be made completely local by enabling the "local toggle" and clicking it. Green means global. 

## Step 3, Configuring streaming (optional):

This program, along with the controller inside Neos, have the cool ability of easily transforming into a Spotify player you can use to play (and control!) your music with your friends. To do this, you will need a way to stream your audio with low latency. I use VoiceMeeter to do this, but however you isolate the audio, you can then spawn out an audio stream in Neos from your Home menu and drop it into the player.

# Issues? Here are some known bugs/tips

- The Spotify API requires an active device to work properly. If you pause your music long enough, Spotify will forget what you're listening on, and attempting to start the server like this will cause an error. If the player disconnects from the server and the server is throwing errors, it is because you left the music paused too long. This is not fixable. 
- The current player sometimes doesn't register when other users press some buttons, so if the player doesn't react, try clicking them again.

Any questions or errors? PM me ingame or shoot me a discord message at Kodufan#7558.
