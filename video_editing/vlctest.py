import vlc

Instance = vlc.Instance('--fullscreen')
player = Instance.media_player_new()
Media = Instance.media_new('song.mp4')
player.set_media(Media)
player.play()

while True:
	pass
