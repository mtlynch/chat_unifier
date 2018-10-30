import os

# Pidgin log path is in the format:
#
#   [medium]/[local username]/[remote username]/[filename].html
#
_LOG_PATH_COMPONENTS = 4
_IGNORED_MEDIA = ['irc']


def iterate_files(directory):
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            log_path = os.path.join(root, filename)
            if _is_log_file(log_path):
                if _get_log_medium(log_path) in _IGNORED_MEDIA:
                    continue
                if _is_system_log(log_path):
                    continue
                yield log_path


def _is_log_file(log_path):
    if not _split_log_path(log_path):
        return False
    _, extension = os.path.splitext(os.path.basename(log_path))
    return extension == '.html'


def _is_system_log(log_path):
    return _get_remote_username(log_path) == '.system'


def _get_log_medium(log_path):
    path_parts = _split_log_path(log_path)
    if path_parts:
        return path_parts[-4]
    else:
        return None


def _get_remote_username(log_path):
    path_parts = _split_log_path(log_path)
    if path_parts:
        return path_parts[-2]
    else:
        return None


def _split_log_path(log_path):
    path_parts = log_path.split(os.path.sep)
    if len(path_parts) < _LOG_PATH_COMPONENTS:
        return None
    return path_parts
