'''
Generate the salt thin tarball from the installed python files
'''

# Import python libs
import os
import tarfile

# Import third party libs
import jinja2
import markupsafe
import yaml

# Import salt libs
import salt


def gen_thin(cachedir):
    '''
    Generate a salt-thin tarball and load it into the location in the cachedir
    '''
    thindir = os.path.join(cachedir, 'thin')
    if not os.path.isdir(thindir):
        os.makedirs(thindir)
    thintar = os.path.join(thindir, 'thin.tgz')
    thinver = os.path.join(thindir, 'version')
    if os.path.isfile(thintar):
        if not os.path.isfile(thinver):
            os.remove(thintar)
        elif open(thinver).read() == salt.__version__:
            return thintar
    tops = [
            os.path.dirname(salt.__file__),
            os.path.dirname(jinja2.__file__),
            os.path.dirname(markupsafe.__file__),
            os.path.dirname(yaml.__file__),
            ]
    with tarfile.open(thintar, 'w:gz') as tfp:
        start_dir = os.getcwd()
        for top in tops:
            base = os.path.basename(top)
            os.chdir(os.path.dirname(top))
            for root, dirs, files in os.walk(base):
                for name in files:
                    if not name.endswith(('.pyc', '.pyo')):
                        tfp.add(os.path.join(root, name))
        os.chdir(os.path.dirname(salt.utils.which('salt-call')))
        tfp.add('salt-call')
        os.chdir(start_dir)
    with open(thinver, 'w+') as fp_:
        fp_.write(salt.__version__)
    return thintar

