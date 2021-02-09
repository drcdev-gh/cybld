#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from setuptools import setup
import sys
import os
import shutil
import gzip

def get_version():
    if os.system("git rev-parse") == 0:
        print("Using git version for installation...")
        return os.popen('git describe --long | cut -d "-" -f-2 | sed "s/-/./g"').read()
    else:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION')) as version_file:
            print("Falling back on version from VERSION file for installation....")
            return version_file.read().strip()

    print("ERROR: Unable to determine version...")
    sys.exit(1)

requirements = []

setup(
    name         = "cybld",
    version      = get_version(),
    author       = "David",
    description  = ("trigger commands anywhere"),
    license      = "MIT",
    keywords     = "development",
    packages     = ['cybld', 'tests'],
    package_data = { 'cybld': ['../VERSION'] },
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Utilities",
        "Topic :: Software Development"
    ],
    provides = ["cybld"],
    entry_points = { 'console_scripts': ['cybld=cybld.__main__:main'], },
    install_requires = requirements,
    extras_require = { 'neovim IPC': ["neovim"],
                       'docs and man page': ["sphinx"]}
)

def docs():
    if shutil.which("sphinx-build") is None:
        print("ERROR: Install sphinx to build the documentation...")
        print("ERROR: Man page will not be available")
        return

    # Setup some paths
    base_dir     = os.path.abspath(os.curdir)
    src_dir      = os.path.abspath(os.path.join(os.curdir, "cybld"))
    doc_dir      = os.path.abspath(os.path.join(os.curdir, "docs"))

    docbuild_dir     = os.path.abspath(os.path.join(doc_dir, "build"))
    docbuild_api_dir = os.path.abspath(os.path.join(docbuild_dir, "apidoc"))
    docbuild_man_dir = os.path.abspath(os.path.join(docbuild_dir, "man"))

    # Build apidoc
    os.chdir(doc_dir)
    os.system("sphinx-apidoc -o " + docbuild_api_dir + " " + src_dir)

    # Build HTML and Man Page
    os.chdir(doc_dir)
    os.system("make html")
    os.system("make man")

    if os.geteuid() != 0:
        print("ERROR: Need sudo rights to build and create man page!")
        return

    # Now install the man page
    man_path = '/usr/share/man/man1'
    if not os.path.exists(man_path):
        print("Unable to install man page - " + man_path + " does not exist")
    else:
        print("Installing man page")
        man_page        = "cybld.1"
        man_page_src    = os.path.join(docbuild_man_dir, man_page)
        if not os.path.exists(man_page_src):
            print("ERROR: Something went wrong while creating man page...")
            return

        man_page_target = os.path.join(man_path, man_page)
        shutil.copy(man_page_src, man_page_target)
        os.chmod(man_page_target, int('444', 8))

        with open(man_page_target, 'rb') as f_in, gzip.open(man_page_target + ".gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            os.remove(man_page_target)
            print("Successfully installed man page")


if 'install' in sys.argv:
    docs()
