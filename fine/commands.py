import os
import shutil
import fine
import click
import yaml
import zipfile
import tarfile
import importlib
from jinja2 import Template

reveal_url_fallback = 'https://github.com/hakimel/reveal.js/archive/3.5.0.tar.gz'
slide_template = Template(
    """---
{%- for key, val in meta.items() %}
{{ key|safe }} : {{ val|safe }}
{%- endfor %}
..."""
)

try:
    # Python 3
    FileNotFoundError
except NameError:
    # Python 2
    FileNotFoundError = IOError


try:
    # python 3
    from urllib.request import urlretrieve
except ImportError:
    # python 2
    from urllib import urlretrieve


def find_project_root():
    pwd = os.getcwd()
    curr = pwd
    for _ in range(100):
        if not os.path.isfile(os.path.join(curr, 'config.yml')):
            os.chdir('..')
            curr = os.getcwd()
        else:
            os.chdir(pwd)
            return curr
    os.chdir(pwd)
    raise FileNotFoundError('This is not a fine project')


def download(url):
    print('download %s' % url)
    try:
        response = urlretrieve(url)
        return response[0]
    except Exception:
        raise


def move_and_replace(src, dst):
    """
    Helper function used to move files from one place to another,
    creating os replacing them if needed

    :param src: source directory
    :param dst: destination directory
    """

    print('move %s to %s' % (src, dst))
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    for src_dir, _, files in os.walk(src):
        # using os walk to navigate through the directory tree
        # keep te dir structure by replacing the source root to
        # the destination on walked path
        dst_dir = src_dir.replace(src, dst)

        if not os.path.exists(dst_dir):
            # to copy not fail, create the not existing dirs
            os.makedirs(dst_dir)

        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)

            if os.path.exists(dst_file):
                os.remove(dst_file)  # to copy not fail, create existing files

            shutil.move(src_file, dst_dir)  # move the files

    shutil.rmtree(src)  # remove the dir structure from the source


def extract_file(compressed_file, path='.'):
    print('extract %s to %s' % (compressed_file, path))
    if os.path.isfile(compressed_file):
        if tarfile.is_tarfile(compressed_file):
            with tarfile.open(compressed_file, 'r:gz') as tfile:
                basename = tfile.members[0].name
                tfile.extractall(path + '/')
        elif zipfile.is_zipfile(compressed_file):
            with zipfile.ZipFile(compressed_file, 'r') as zfile:
                basename = zfile.namelist()[0]
                zfile.extractall(path)
        else:
            raise NotImplementedError('File type not supported')
    else:
        raise FileNotFoundError(
            '{0} is not a valid file'.format(compressed_file))

    return os.path.abspath(os.path.join(path, basename))


def load_url(config):
    for key in config:
        if key.upper() == 'REVEAL':
            if 'url' in config[key]:
                return config[key]['url']

    return None


def install_reveal():
    package_root = os.path.dirname(fine.__file__)
    with open(os.path.join(package_root, 'config.yml')) as f:
        default_config = yaml.load(f.read())
    default_url = load_url(default_config)

    usr_config_path = os.path.join(os.getcwd(), 'config.yml')
    if os.path.isfile(usr_config_path):
        with open(usr_config_path, 'r') as f:
            usr_config = yaml.load(f.read())
        usr_url = load_url(usr_config)
    else:
        usr_url = None

    if usr_url is not None:
        url = usr_url
    elif default_url is not None:
        url = default_url
    else:
        url = reveal_url_fallback

    path = download(url)

    target = os.path.join(os.path.dirname(fine.__file__), 'static/revealjs')
    print(target)
    move_and_replace(
        extract_file(path),
        target,
    )

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copydemo(dst):
    package_root = os.path.dirname(fine.__file__)
    demo_path = os.path.join(package_root, 'demo')
    copytree(demo_path, dst)


@click.group()
def main():
    """fine, make a fine presentation

    fine is a markdown presentation generator developed
    based on flask-reveal. To use it in command line, you
    can simply type the command fine.
    """
    pass


@main.command(short_help="init fine project")
def init(path=None):
    """init a fine project in root/current folder.

    Usage:
        fine init [project-path]
    """
    if path is None:
        path = os.getcwd()
    os.chdir(path)
    copydemo(path)


@main.command(short_help="install revealjs")
def install():
    install_reveal()


@main.command(short_help="new slide")
@click.argument('name', metavar='<name>')
def new(name):
    """Create a new presentation

    Usage:
        fine new <name>
    """
    # preprocess name
    name, _ = os.path.splitext(name)
    package_root = os.path.dirname(fine.__file__)
    project_root = find_project_root()
    default_config = os.path.join(package_root, 'config.yml')
    usr_config = os.path.join(project_root, 'config.yml')
    with open(usr_config, 'r') as f:
        config = yaml.load(f.read())

    source_dir = None
    author = None
    for key in config:
        if key.upper() == 'SOURCE_DIR':
            source_dir = config[key]
        if key.upper() == 'META':
            if 'author' in config[key]:
                author = config[key]['author']

    if source_dir is None:
        with open(default_config, 'r') as f:
            config = yaml.load(f.read())

        for key in config:
            if key.upper() == 'SOURCE_DIR':
                source_dir = config[key]

            if key.upper() == 'META':
                if 'author' in config[key]:
                    author = config[key]['author']

    source_path = os.path.join(project_root, source_dir)
    file_path = os.path.join(source_path, name + '.md')
    if os.path.isfile(file_path):
        raise FileExistsError('presentation[%s] exists' % name +
                              ' cannot generate new presentation')

    meta = {
        'title': name,
        'author': author,
    }

    with open(file_path, 'w') as f:
        f.write(slide_template.render(meta=meta))


# See this:
# https://stackoverflow.com/questions/67631/


@main.command(short_help="start service")
def serve(name=None, debug=False):
    """start service.

    Usage:
        fine s, start [--debug]
    """
    if name is None:
        project_root = find_project_root()
        start_file_path = os.path.join(project_root, 'start.py')
        spec = importlib.util.spec_from_file_location('start', start_file_path)
        start = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(start)
        start.app.run()
    else:
        # TODO: load single file
        # app = fine.Fine('fine')
        pass


main.add_command(init)
main.add_command(install)
main.add_command(new)
main.add_command(serve)

if __name__ == '__main__':
    main()
