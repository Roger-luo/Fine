import os
import shutil
import setuptools.command.install
import setuptools.command.build_py
import setuptools.command.develop
import distutils.command.clean
from setuptools import setup, find_packages
from subprocess import call


class build_py(setuptools.command.build_py.build_py):

    def run(self):
        self.create_version_file()
        self.install_reveal()
        setuptools.command.build_py.build_py.run(self)

    def install_reveal(self):
        from fine.commands import install_reveal
        install_reveal()

    @staticmethod
    def create_version_file():
        global version, cwd
        print('-- Building version ' + version)
        version_path = os.path.join(cwd, 'fine', 'version.py')
        with open(version_path, 'w') as f:
            f.write("__version__ = '{}'\n".format(version))


class develop(setuptools.command.develop.develop):

    def run(self):
        build_py.create_version_file()
        setuptools.command.develop.develop.run(self)


class clean(distutils.command.clean.clean):

    def run(self):
        import glob
        with open('.gitignore', 'r') as f:
            ignores = f.read()
            for wildcard in filter(bool, ignores.split('\n')):
                for filename in glob.glob(wildcard):
                    if filename == 'venv/':
                        continue

                    try:
                        os.remove(filename)
                    except OSError:
                        shutil.rmtree(filename, ignore_errors=True)
        # print('cleaning')
        distutils.command.clean.clean.run(self)


class install(setuptools.command.install.install):
    """include reveal.js installation process
    """

    def run(self):
        # from fine.commands.install import install_reveal
        super(install, self).run()
        # install_reveal()

version = '0.0.1'
cwd = os.path.dirname(os.path.abspath(__file__))

setup(
    name='fine',
    version=version,
    description="Roger's Markdown Slide Show Generator",
    cmdclass={
        'build_py': build_py,
        'develop': develop,
        'clean': clean,
        'install': install,
    },
    entry_points={
        'console_scripts': ['fine=fine.commands:main'],
    },
    packages=find_packages(),
    include_package_data=True,
    # package_data={'fine': [
    #     '*/*.html',
    #     '*/*.yml',
    #     '*.yml'
    # ]},
    zip_safe=False
)
