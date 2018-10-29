import os


def iterate_files(directory):
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if _is_log_file(filename):
                yield os.path.join(root, filename)


def _is_log_file(filename):
    _, extension = os.path.splitext(filename)
    return extension == '.html'
