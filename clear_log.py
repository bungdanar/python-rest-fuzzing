import os
import shutil


def clear_log():
    try:
        log_path = 'logs'
        filename = 'res-time.log'
        filename_2 = 'res_time_with_req_body.log'

        if os.path.exists(log_path):
            shutil.rmtree(log_path)

        os.makedirs(log_path)

        log_file = os.path.join(log_path, filename)
        with open(log_file, 'w'):
            pass

        log_file_2 = os.path.join(log_path, filename_2)
        with open(log_file_2, 'w'):
            pass
    except Exception as e:
        print(e)


clear_log()
