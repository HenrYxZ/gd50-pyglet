from constants import GLOBAL_VOLUME


def play(sound, volume=GLOBAL_VOLUME):
    player = sound.play()
    player.volume = volume
    return player
