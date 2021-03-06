import os
from itertools import (takewhile, repeat)

CHECK_CSV_HEADER = 'line,point,easting,northing,check_easting,check_northing,error_easting,error_northing'
CHECK_EXT = '.check.csv'
NOT_IN_DB_CSV_HEADER = 'line,point,easting,northing'
NOT_IN_DB_EXT = '.not-in-db.csv'
LOG_EXT = '.check.log'


def csv_file_create(filename, header):
    check_file = open(filename, 'w')
    check_file.write(header + os.linesep)
    check_file.close()


def csv_file_record_add(filename, record):
    check_file = open(filename, 'a')
    check_file.write(record + os.linesep)
    check_file.close()


def log_file_create(filename):
    log_file = open(filename, 'w')
    log_file.close()


def log_file_record_add(filename, record):
    log_file = open(filename, 'a')
    log_file.write(record + os.linesep)
    log_file.close()


def count_file_line_number(filename):
    return sum(1 for line in open(filename))


def iter_count(file_name):
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)
