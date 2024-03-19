import os

from optparse import OptionParser

from DataLocker.locker.locker import Locker


def return_arguments():

    parser = OptionParser()

    parser.add_option('--lock', dest='lock', action='store_true', help='lock the specified file or directory')
    parser.add_option('--unlock', dest='unlock', action='store_true', help='unlock the specified file or directory')
    parser.add_option('-p', '--password', dest='password', help='password for locking and unlocking')
    parser.add_option('-f', '--file', dest='file', help='specify the file to be processed')
    parser.add_option('-d', '--directory', dest='directory', help='specify the directory to be processed')

    options = parser.parse_args()[0]

    check_arguments(parser, options)

    return options


def check_arguments(parser, options):

    if options.lock and options.unlock:
        parser.error('[-] One action only "--lock" or "--unlock"')

    if options.lock is None and options.unlock is None:
        parser.error('[-] Action not found')

    if options.file and options.directory:
        parser.error('[-] One target only "--file" or "--directory"')

    if not options.file and not options.directory:
        parser.error('[-] Target not found')


def get_file_name(file_path):

    return os.path.basename(file_path)


def lock_file(file_path, password):

    locker = Locker(password)
    locker.lock(file_path)

    print(f'[lock] {get_file_name(file_path)}')


def lock_files_in_dir(dir_path, password):

    locker = Locker(password)

    for path in os.listdir(dir_path):
        
        file_path = os.path.join(dir_path, path)
        if os.path.isfile(file_path):

            locker.lock(file_path)
            print(f'[lock] {get_file_name(file_path)}')


def unlock_file(file_path, password):

    locker = Locker(password)
    locker.unlock(file_path)

    print(f'[unlock] {get_file_name(file_path)}')


def unlock_files_in_dir(dir_path, password):

    locker = Locker(password)

    for path in os.listdir(dir_path):

        file_path = os.path.join(dir_path, path)
        if os.path.isfile(file_path) and check_locking_file(file_path):

            locker.unlock(file_path)
            print(f'[unlock] {get_file_name(file_path)}')


def check_locking_file(file_path):

    _, ext = os.path.splitext(file_path)
    return True if ext == '.lock' else False


def main():

    options = return_arguments()

    lock_mode = options.lock
    unlock_mode = options.unlock
    password = options.password
    file_path = options.file
    dir_path = options.directory

    if lock_mode:

        if file_path:
            lock_file(file_path, password)

        elif dir_path:
            lock_files_in_dir(dir_path, password)


    elif unlock_mode:

        if file_path:
            unlock_file(file_path, password)

        elif dir_path:
            unlock_files_in_dir(dir_path, password)


if __name__ == '__main__':
    main()
