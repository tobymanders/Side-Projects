from moviepy.editor import *
import pickle

def cut_new_clips():
	path = 'episode.mkv'
	with open('/Users/cytology/Documents/code/video_editing/clips/timepoints', 'rb') as fb:
		timepoints = pickle.load(fb)

	for i, timepoint in enumerate(timepoints):
		start = timepoint - 10
		end = timepoint + 10
		clip = VideoFileClip(path).subclip(start, end)
		clip.write_videofile('/Users/cytology/Documents/code/video_editing/clips/' + str(i + 1) + '.mp4', temp_audiofile="temp-audio.m4a", 
			remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
	cut_new_clips()