from setuptools import setup
import os

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "cookiesparser", "__version__.py"), "r") as f:
    exec(f.read(), about)

readme = open("README.md","r").read()
setup(
	name=about["__title__"],
	version=about["__version__"],
	author=about["__author__"],
	description=about["__description__"],
	author_email=about["__author_email__"],
	long_description=readme,
	long_description_content_type="text/markdown",
	packages=["cookiesparser"],
	keywords=[
		"cookiesparser",
		"cookie parser",
		"cookies parser",
		"parse cookies"
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
    ],
	install_requires=[],
)
