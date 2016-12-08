def openFile(file_path):
    try:
        f = file(file_path, "r")
        return f
    except Exception, e:
        print "Exception: ", e

def closeFile(f):
    f.close()
