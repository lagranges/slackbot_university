import setuptools
import slackbot_university

version = {}

with open("...slackbot_university/version.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r") as fh:
    long_description = fd.read()

setuptools.setup(
    name="slackbot_university",        
    version = version["__version__"],
    packages=setuptools.find_packages(),
    install_requires=[
        "slackclient",
        "googletrans",
        "wikipedia",
    ],
    python_requires=">=3.6"
)
