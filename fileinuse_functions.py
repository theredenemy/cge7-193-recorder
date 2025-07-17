import os
def is_file_in_use(filename):
    import os
    try:
        os.rename(filename, filename)
        return False
    except PermissionError:
        return True