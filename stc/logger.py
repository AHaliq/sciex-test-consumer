"""
stc.logger
~~~~~~~~~~

Logging util
"""

import sys
from stc.table import errors_to_file_errors

OKBLUE = '\033[94m'
WARNING = '\033[93m'
FAIL = '\033[91m'
OKGREEN = '\033[92m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'


def erase_line():
    sys.stdout.write('\x1b[2K')


def log_reader(i, number_of_files, path):
    erase_line()
    print(
        f"  {OKBLUE}[{i + 1}/{number_of_files}]{ENDC} reading '{path}'",
        end='\r'
    )


def log_failed_reads(number_of_files, number_of_read_files, failed_to_read_files):
    print(f'{FAIL}{BOLD}failed to read {number_of_files - number_of_read_files} files{ENDC}')
    for f in failed_to_read_files:
        print(f'  {FAIL}{f}{ENDC}')


def log_errors(errors):
    print(FAIL + BOLD + "\ntabulating selector failures..." + ENDC)
    file_errors = errors_to_file_errors(errors, True)
    print(FAIL + BOLD + "\nselector failures:" + ENDC)
    error_list = file_errors.items()
    fail_count = 0
    for key, value in error_list:
        print(FAIL + UNDERLINE + key + ENDC, end='\n  ')
        for file_name in value:
            fail_count += 1
            print(FAIL + f'{file_name}, ' + ENDC, end='')
        print('')
    msg = f"\n{fail_count} selector failures:"
    print(FAIL + BOLD + msg + ENDC)


def log_success(number_of_read_files, number_of_files, excel_path):
    print(f"\n{OKGREEN}{number_of_read_files} out of {number_of_files} files successfully generated '{excel_path}'{ENDC}")
