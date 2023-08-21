import os
import shutil


def clear_log():
    try:
        log_path = 'logs'
        filename = 'res-time.log'

        if os.path.exists(log_path):
            shutil.rmtree(log_path)

        os.makedirs(log_path)

        log_file = os.path.join(log_path, filename)
        with open(log_file, 'w'):
            pass
    except Exception as e:
        print(e)


clear_log()
