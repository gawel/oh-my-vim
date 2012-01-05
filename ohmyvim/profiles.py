from glob import glob
import os

__doc__ = """
profiles documentation
"""

TITLE = """
%(title)s
%(sep)s

"""

def gendoc():
    """generate profiles documentations"""
    dirname = os.path.abspath(os.path.dirname(__file__))
    dirname = os.path.dirname(dirname)
    docs = os.path.join(dirname, "docs", "profiles.rst")
    match = os.path.join(dirname, "profiles", "*.vim")
    with open(docs, "w") as docs:
        docs.write("=======================\n")
        docs.write("Profiles\n")
        docs.write("=======================\n\n")
        docs.write(".. automodule:: ohmyvim.profiles\n\n")
        for filename in glob(match):
            with open(filename) as fd:
                title, _ = os.path.splitext(os.path.basename(filename))
                docs.write(TITLE % dict(title=title, sep="=" * len(title)))
                data = fd.readlines()
                for i, line in enumerate(data):
                    if line.startswith('"'):
                        docs.write(line.strip('" '))
                    break
                docs.write("\n.. literalinclude:: %s\n" % filename)
                docs.write("   lines: %s\n" % (i + 1,))

if __name__ == "__main__":
    gendoc()

