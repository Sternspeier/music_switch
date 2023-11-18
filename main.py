from pygame import mixer
from time import sleep
from multiprocessing import Process, Manager
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
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play(start=seconds)
    seconds_count = 0
    while mixer.music.get_busy():  # wait for music to finish playing
        sleep(1)
        seconds_count += 1
        if not flag.value: break

    return seconds_count


def music_looper(abba_zipped: list, mode, go_flag):
    seconds = 0
    index = 0
    while index < len(abba_zipped):
        seconds = music_player(abba_zipped[index][mode.value], seconds, go_flag)

        if not go_flag.value:
            go_flag.value = True
            continue

        index+=1
        seconds = 0


def main():
    music_path = _get_path('music')
    abba_eight_bit = _get_abba_files('eight_bit', music_path)
    abba_orchestra = _get_abba_files('orchestra', music_path)

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


main()