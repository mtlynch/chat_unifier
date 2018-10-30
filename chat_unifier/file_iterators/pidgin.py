import os

_IGNORED_MEDIA = ['irc']


def iterate_files(directory):
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if _is_log_file(filename):
                log_path = os.path.join(root, filename)
                if _get_log_medium(log_path) in _IGNORED_MEDIA:
                    continue
                yield log_path


def _is_log_file(filename):
    _, extension = os.path.splitext(filename)
    return extension == '.html'


def _get_log_medium(log_path):
    path_parts = log_path.split(os.path.sep)
    if len(path_parts) < 4:
        return None
    return path_parts[-4]
