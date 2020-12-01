import os
import re
import pathlib
import logging
import datetime
from dotenv import load_dotenv

load_dotenv()

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)


def find_all_files(directory):

    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def rename_file(file):

    file_name_size = 80
    file_name = os.path.splitext(os.path.basename(file))[0]
    file_extension = os.path.splitext(file)[1]

    return file_name[:-((len(file_name) + len(file_extension)) - file_name_size)].strip() + file_extension


def generate_path(file):

    file_directory = os.path.dirname(file)

    return os.path.join(file_directory, rename_file(file))


def main():

    count_folder_path = os.environ['COUNT_FOLDER_PATH']
    count_size = int(os.environ['COUNT_SIZE'])

    log_file = os.environ['LOG_FILE_PATH'] + os.environ['LOG_FILE_NAME']

    if not os.path.isfile(log_file):
        with open(log_file, 'w'):
            pass

    with open(log_file, mode='a') as f:
        if os.path.isdir(count_folder_path):
            for file in find_all_files(count_folder_path):

                file_name = os.path.basename(file)

                if file_name.startswith(".") or file_name == "" or file_name == "README.md":
                    pass
                    continue

                if file_name.endswith(".tar.gz"):
                    logging.warning(
                        '%s', "The file extension is .tar.gz：[　" + str(file) + "　]")
                    f.write('\n' + "WARNING " +
                            str(datetime.datetime.now()) + " The file extension is .tar.gz：[　" + str(file) + "　]")
                    continue

                if len(file_name) > count_size:

                    new_path = generate_path(file)

                    if len(os.path.basename(new_path)) <= count_size:
                        os.rename(file, new_path)
                        f.write('\n' + "RENAME " + str(datetime.datetime.now()) +
                                " " + str(os.path.dirname(file)) + " [　" + str(os.path.basename(file)) + " →→→ " + str(os.path.basename(new_path)) + "　]")
                    else:
                        logging.error(
                            '%s', str(len(os.path.basename(new_path))) + "文字 指定文字数を超えています")
                        f.write('\n' + "ERROR " +
                                str(datetime.datetime.now()) + " " + str(len(os.path.basename(new_path))) + "文字 指定文字数を超えています")

                else:
                    f.write('\n' + "SKIP " + str(datetime.datetime.now()) +
                            " " + str(os.path.dirname(file)) + " [　" + str(os.path.basename(file)) + "　]")
        else:
            logging.error('%s', 'No Date folder')
            f.write('\n' + "ERROR " +
                    str(datetime.datetime.now()) + " No Date folder")


if __name__ == "__main__":
    main()
