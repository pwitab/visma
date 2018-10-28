import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'visma'
DESCRIPTION = "A Python Client/ORM library for integration to Visma " \
              "e-Accounting, Visma e-Ekonomi"
URL = 'https://github.com/pwitab/visma'
EMAIL = 'henrik@pwit.se'
AUTHOR = "Henrik Palmlund Wahlgren @ Palmlund Wahlgren Innovative Technology AB"
REQUIRES_PYTHON = '>=3.6'
# VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'marshmallow>=3.0.0b1',
    'click',
    'iso8601',
    'requests'
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        # os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name=NAME,
    version='0.0.3',
    python_requires=REQUIRES_PYTHON,
    description=DESCRIPTION,
    long_description=readme + '\n\n' + history,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'visma = visma.cli:cli',
        ],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="BSD-3",
    zip_safe=False,
    keywords=['accounting', 'visma', 'eekonomi'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
