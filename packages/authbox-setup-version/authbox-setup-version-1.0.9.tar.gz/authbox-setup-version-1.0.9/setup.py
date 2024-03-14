from setuptools import setup, find_packages
from os.path import abspath, dirname, join
from authbox_setup_version import get_version

#from authbox_setup_version._version import __version__
# Fetches the content from README.md
# This will be used for the "long_description" field.
base_dir = dirname(abspath(__file__))
README_MD = open(join(base_dir, "README.md")).read()

setup(
    name='authbox-setup-version',
    #version='1.0.7',
    version=get_version(join(base_dir, "authbox_setup_version", "_version.py")),
    description='Read version variable from _version.py and make incremental version',
    
    author='Iwan Setiawan',
    # The author name and email fields are self explanatory.
    # These fields are OPTIONAL
    # author_name="ione03",
    author_email="suratiwan03@gmail.com",

    packages=find_packages(exclude=['tests', 'tests.*']),
    
    install_requires=[
        'incremental', 'click', 'twisted',
    ],

    # agar file manifest .in dieksekusi
    include_package_data = True,
    
    # The content that will be shown on your project page.
    # In this case, we're displaying whatever is there in our README.md file
    # This field is OPTIONAL
    long_description=README_MD,
    
    # Now, we'll tell PyPI what language our README file is in.
    # In my case it is in Markdown, so I'll write "text/markdown"
    # Some people use reStructuredText instead, so you should write "text/x-rst"
    # If your README is just a text file, you have to write "text/plain"
    # This field is OPTIONAL
    long_description_content_type="text/markdown",
    
    # The url field should contain a link to a git repository, the project's website
    # or the project's documentation. I'll leave a link to this project's Github repository.
    # This field is OPTIONAL
    url="https://github.com/PROJECT-AUTHBOX/authbox_setup_version.git",

    classifiers=[
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    
    keywords="project, version, incremental, setup, django, python",
)
