from multiprocessing import freeze_support

from spotifylter import main

if __name__ == '__main__':
    freeze_support()
    main.run_with_gui()
