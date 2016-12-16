def openFile(file_path):
    """Open a file using path(:argument: file_path) and return it."""
    try:
        f = file(file_path, "r")
        return f
    except Exception, e:
        print "Exception: ", e


def closeFile(f):
    """Close file(:argument: f)."""
    f.close()
