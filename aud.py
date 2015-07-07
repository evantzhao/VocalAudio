#!/usr/bin/env python

import sound

def main():
	print "Working"

	mysound = sound.load_sound("/Users/eos/Desktop/Vocal Processing/airplane.wav")
	fade(mysound, 2000)

#Removes the singer's voice from the audio clip. Works only on songs that have been recorded with a single channel.
def rem_vocals(snd):
	length_of_sound = len(snd)
	no_vocals = sound.create_sound(length_of_sound)
	for x in range(0, length_of_sound):
		left_channel = sound.get_left(sound.get_sample(snd, x))
		right_channel = sound.get_right(sound.get_sample(snd,x))
		new_channel = (left_channel - right_channel) / 2

		sound.set_right(sound.get_sample(no_vocals, x), new_channel)
		sound.set_left(sound.get_sample(no_vocals, x), new_channel)

	print "Vocal stripping completed"
	sound.save_as(no_vocals, "new.wav")
	return no_vocals

#fade in function that fades in an audio sound clip linearly. Relies on below function. 
def fade_in(snd, fade_length):
	fade_in(snd, fade_length, True)

#Takes an audio clip and fades it in linearly. 
def fade_in(snd, fade_length, want_to_save):
	faded = sound.create_sound(len(snd))
	fade_interval = 1.0 / fade_length
	for x in range(0, fade_length):
		left_channel = sound.get_left(sound.get_sample(snd, x))
		right_channel = sound.get_right(sound.get_sample(snd, x))

		#needs to be rounded into an integer
		new_left = int(left_channel * fade_interval * x)
		new_right = int(right_channel * fade_interval * x)

		sound.set_left(sound.get_sample(faded, x), new_left)
		sound.set_right(sound.get_sample(faded, x), new_right)

	for x in range(fade_length + 1, len(snd)):
		left_channel = sound.get_left(sound.get_sample(snd, x))
		right_channel = sound.get_right(sound.get_sample(snd, x))

		sound.set_left(sound.get_sample(faded, x), left_channel)
		sound.set_right(sound.get_sample(faded, x), right_channel)

	print "Fade-in Completed"

	if(want_to_save == True):
		sound.save_as(faded, "faded.wav")

	return faded

#fades out an audio clip linearly. Relies on below function.
def fade_out(snd, fade_length):
	fade_out(snd, fade_length, True)

def fade_out(snd, fade_length, want_to_save):
	fade_out = sound.create_sound(len(snd))
	fade_interval = 1.0 / fade_length

	for x in range(0, (len(snd) - fade_length)):
		left_channel = sound.get_left(sound.get_sample(snd, x))
		right_channel = sound.get_right(sound.get_sample(snd, x))

		sound.set_left(sound.get_sample(fade_out, x), left_channel)
		sound.set_right(sound.get_sample(fade_out, x), right_channel)

	#local counter that makes it simpler to create the fading effect.
	counter = 0
	for x in range((len(snd) - fade_length + 1), len(snd)):

		left_channel = sound.get_left(sound.get_sample(snd, x))
		right_channel = sound.get_right(sound.get_sample(snd, x))

		#needs to be rounded into an integer. Take the total length left, and subtract one from it every time. 
		new_left = int(left_channel * fade_interval * ((fade_length) - counter))
		new_right = int(right_channel * fade_interval * ((fade_length) - counter))

		sound.set_left(sound.get_sample(fade_out, x), new_left)
		sound.set_right(sound.get_sample(fade_out, x), new_right)

		#steps up the value of the counter in order to continue decreasing the volume at a linear rate. 
		counter += 1

	print "Fade-out Completed"

	if(want_to_save == True):
		sound.save_as(fade_out, "fade-out.wav")

	return fade_out

#creates a fade in and fade out effect using both of the previous two methods. 
def fade(snd, fade_length):
	fading_audio = sound.create_sound(len(snd))
	fading_audio = fade_in(snd, fade_length, False)
	fading_audio_final = sound.create_sound(len(snd))
	fading_audio_final = fade_out(fading_audio, fade_length, False)

	sound.save_as(fading_audio_final, "fading audio.wav")
	print "Fade Completed"

def left_to_right(snd, pan_length):
	pan = sound.create_sound(len(snd))
	pan_interval = 1.0/pan_length

	for x in range(0, pan_length):
		right_channel = sound.get_right(sound.get_sample(snd, x))
		new_right = int(right_channel * pan_interval * x)

		sound.set_right(sound.get_sample(pan, x), new_right)

		left_channel = sound.get_right(sound.get_sample(snd, x))
		new_left = int(left_channel * pan_interval * abs(pan_length - x - 1))

		sound.set_left(sound.get_sample(pan, x), new_left)

	for y in range(pan_length + 1, len(snd)):
		left_channel = sound.get_left(sound.get_sample(snd, y))
		right_channel = sound.get_right(sound.get_sample(snd, y))

		sound.set_left(sound.get_sample(pan, y), left_channel)
		sound.set_right(sound.get_sample(pan, y), right_channel)

	print "Pan completed"



	sound.save_as(pan, "pan.wav")

	return pan

#Runs the main, after establishing that this is not a library. 
if __name__ == "__main__":
	main()
