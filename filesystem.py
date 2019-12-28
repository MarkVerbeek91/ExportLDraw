import os

from . import options

search_paths = []


def reset_caches():
    global search_paths
    search_paths = []


def append_search_path(path):
    if path != "" and os.path.exists(path):
        search_paths.append(path)


def append_search_paths():
    ldraw_path = options.ldraw_path

    append_search_path(os.path.join(ldraw_path))
    append_search_path(os.path.join(ldraw_path, "models"))
    append_search_path(os.path.join(ldraw_path, "unofficial", "lsynth"))
    append_search_path(os.path.join(ldraw_path, "unofficial", "parts"))
    append_search_path(os.path.join(ldraw_path, "parts"))

    if options.resolution == "High":
        append_search_path(os.path.join(ldraw_path, "unofficial", "p", "48"))
    elif options.resolution == "Low":
        append_search_path(os.path.join(ldraw_path, "unofficial", "p", "8"))
    append_search_path(os.path.join(ldraw_path, "unofficial", "p"))

    if options.resolution == "High":
        append_search_path(os.path.join(ldraw_path, "p", "48"))
    elif options.resolution == "Low":
        append_search_path(os.path.join(ldraw_path, "p", "8"))
    append_search_path(os.path.join(ldraw_path, "p"))


# https://stackoverflow.com/a/8462613
def path_insensitive(path):
    """
    Get a case-insensitive path for use on a case sensitive system.

    >>> path_insensitive('/Home')
    '/home'
    >>> path_insensitive('/Home/chris')
    '/home/chris'
    >>> path_insensitive('/HoME/CHris/')
    '/home/chris/'
    >>> path_insensitive('/home/CHRIS')
    '/home/chris'
    >>> path_insensitive('/Home/CHRIS/.gtk-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive('/home/chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive('/HOME/Chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive("/HOME/Chris/I HOPE this doesn't exist")
    "/HOME/Chris/I HOPE this doesn't exist"
    """

    return _path_insensitive(path) or path


def _path_insensitive(path):
    """
    Recursive part of path_insensitive to do the work.
    """

    if path == '' or os.path.exists(path):
        return path

    base = os.path.basename(path)  # may be a directory or a file
    dirname = os.path.dirname(path)

    suffix = ''
    if not base:  # dir ends with a slash?
        if len(dirname) < len(path):
            suffix = path[:len(path) - len(dirname)]

        base = os.path.basename(dirname)
        dirname = os.path.dirname(dirname)

    if not os.path.exists(dirname):
        dirname = _path_insensitive(dirname)
        if not dirname:
            return

    # at this point, the directory exists but not the file

    try:  # we are expecting dirname to be a directory, but it could be a file
        files = os.listdir(dirname)
    except OSError:
        return

    baselow = base.lower()
    try:
        basefinal = next(fl for fl in files if fl.lower() == baselow)
    except StopIteration:
        return

    if basefinal:
        return os.path.join(dirname, basefinal) + suffix
    else:
        return


def check_encoding(filepath):
    """Check the encoding of a file for Endian encoding."""

    filepath = path_insensitive(filepath)

    # Open it, read just the area containing a possible byte mark
    with open(filepath, "rb") as encode_check:
        encoding = encode_check.readline(3)

    # The file uses UCS-2 (UTF-16) Big Endian encoding
    if encoding == b"\xfe\xff\x00":
        return "utf_16_be"

    # The file uses UCS-2 (UTF-16) Little Endian
    elif encoding == b"\xff\xfe0":
        return "utf_16_le"

    # Use LDraw model standard UTF-8
    else:
        return "utf_8"


def read_file(filepath):
    # print(filepath)
    lines = []
    if os.path.exists(filepath):
        file_encoding = check_encoding(filepath)
        try:
            with open(filepath, 'rt', encoding=file_encoding) as file:
                lines = file.read().strip().splitlines()
        except:
            with open(filepath, 'rt', encoding="latin_1") as file:
                lines = file.read().strip().splitlines()
    return lines


def locate(filename):
    part_path = filename.replace("\\", os.path.sep)
    part_path = os.path.expanduser(part_path)
    for path in search_paths:
        full_path = os.path.join(path, part_path)
        if options.debug_text:
            print(full_path)
        full_path = path_insensitive(full_path)
        if os.path.exists(full_path):
            return full_path
    return None
