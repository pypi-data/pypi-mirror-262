
just_playback
=========
A small library for playing audio files in python. Provides file format independent methods for loading audio files, playing, pausing, resuming, stopping, seeking, getting the current playback position, and changing the volume.

The package uses [miniaudio](https://github.com/mackron/miniaudio) for awesome cross-platform, dependency-free asynchronous audio playback that stays away from your main thread.

Installation
-------------
	pip install just-playback

Usage
-------------
``` python
>>> from just_playback import Playback
>>> playback = Playback() # creates an object for managing playback of a single audio file
>>> playback.load_file('music/sample.mp3')
# or just pass the filename directly to the constructor

>>> playback.play() # plays loaded audio file from the beginning
>>> playback.pause() # pauses playback. No effect if playback is already paused
>>> playback.resume() # resumes playback. No effect if playback is playing
>>> playback.stop() # stops playback. No effect if playback is not active

>>> playback.seek(60) # positions playback at 1 minute from the start of the audio file. No effect
# if playback is not active
>>> playback.set_volume(0.5) # sets the playback volume to 50% of the audio file's original value

>>> playback.loop_at_end(True) # since 0.1.5. Causes playback to automatically restart when it completes.

>>> playback.active # True if playback is active i.e playing or paused
>>> playback.playing # True if playback is active and not paused
>>> playback.curr_pos # current absolute playback position in seconds from 
				  #	the start of the audio file (unlike pygame.mixer.get_pos). 
>>> playback.paused # True if playback is paused.
>>> playback.duration # length of the audio file in seconds. 
>>> playback.volume # current playback volume
>>> playback.loops_at_end # True if playback is set to restart when it completes.
```