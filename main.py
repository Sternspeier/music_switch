from pygame import mixer

from mutagen.mp3 import MP3
from multiprocessing import Process, Manager
from time import sleep
import os


def _get_path(dir: str):
    dirname = os.path.dirname
    return os.path.join((dirname(__file__)), dir)


def _get_abba_files(genre: str, music_path: str):
    abba_path = music_path + f'/{genre}'
    return [os.path.join(abba_path, f) for f in os.listdir(abba_path) if f.endswith('.mp3')]


def _fool_proof_abba(bit_list: list, orc_list: list):
    if not (len(bit_list) == len(orc_list)):
        return False
    
    '''possibly compare the individual values here'''
    return True


def _switcher(mode, flag):
    '''
    8-bit = 0
    Orchestra = 1
    '''
    while True:
        m = input('Which list to start from (0 or 1):\n')
        if m in ['s', 'switch']:
            match mode.value:
                case 0: mode.value = 1
                case 1: mode.value = 0
            flag.value = False
        elif m in ['0', '8', '8-bit']:
            mode.value = 0
            flag.value = False
        elif m in ['1', 'o', 'orchestra']:
            mode.value = 1
            flag.value = False
        elif m == 'exit':
            return
        else:
            print('bad input')


def music_player(filepath: str, seconds: float, flag):
    as_mp3 = MP3(filepath)
    if seconds >= as_mp3.info.length: return 0

    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play(start=seconds)
    while mixer.music.get_busy():  # wait for music to finish playing
        sleep(1)
        seconds += 1
        if not flag.value: break

    return seconds


def music_looper(abba_zipped: list, mode, go_flag):
    seconds = 0
    index = 0
    while index < len(abba_zipped):
        song = abba_zipped[index][mode.value]
        song_split = song.split('/')
        print(f'\n-- now playing: {song_split[-1]} in {song_split[-2]} --\n')

        seconds = music_player(song, seconds, go_flag)

        if not go_flag.value:
            go_flag.value = True
            continue

        index+=1
        seconds = 0


def main():
    music_path = _get_path('music')
    abba_eight_bit = sorted(_get_abba_files('eight_bit', music_path))
    abba_orchestra = sorted(_get_abba_files('orchestra', music_path))

    if not _fool_proof_abba(abba_eight_bit, abba_orchestra):
        return

    abba_zipped = list(zip(abba_eight_bit, abba_orchestra))

    manager = Manager()
    mode = manager.Value('mode', 0)
    go_flag = manager.Value('flag', True)

    p = Process(target=music_looper, args=(abba_zipped, mode, go_flag))
    p.start()

    _switcher(mode, go_flag)

    p.join()


if __name__ == '__main__':
    main()