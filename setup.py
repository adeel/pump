from setuptools import setup

desc = open("README").read()

setup(
  name="pack",
  version="0.1.0",
  description="a minimal DSL for building a WSGI app",
  long_description=desc,
  author="Adeel Ahmad Khan",
  author_email="adeel@adeel.ru",
  packages=["pack", "pack.util", "pack.middleware"],
  license="MIT",
  classifiers=[
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
  ],
)