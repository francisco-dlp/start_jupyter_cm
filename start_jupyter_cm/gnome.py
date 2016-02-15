import os
import stat
from subprocess import call

NPATH = os.path.expanduser("~/.local/share/nautilus")
SPATH = os.path.join(NPATH, "scripts")


def add_jupyter_here():
    if not os.path.exists(NPATH):
        print("Nothing done. Currently only Gnome and Windows are supported.")
        return
    if not os.path.exists(SPATH):
        os.makedirs(SPATH)

    logo_path = os.path.expandvars(os.path.join(
        os.path.dirname(__file__), 'icons'))
    logos = {'qtconsole': os.path.join(logo_path, 'jupyter-qtconsole.png'),
             'notebook': os.path.join(logo_path, 'jupyter.png')}
    for terminal in ["qtconsole", "notebook"]:
        script_path = os.path.join(SPATH, "Jupyter %s here" % terminal)
        if not os.path.exists(script_path):
            with open(script_path, "w") as f:
                f.write("#!/bin/sh\njupyter-%s" % terminal)
            st = os.stat(script_path)
            os.chmod(script_path, st.st_mode | stat.S_IEXEC)
            print('Jupyter %s here created.' % terminal)
            call(['gvfs-set-attribute', '-t', 'string', '%s' % script_path,
                  'metadata::custom-icon', 'file://%s' % logos[terminal]])


def remove_jupyter_here():
    for terminal in ["qtconsole", "notebook"]:
        script_path = os.path.join(SPATH, "Jupyter %s here" % terminal)
        if os.path.exists(script_path):
            os.remove(script_path)
            print("Jupyter %s here removed." % terminal)
