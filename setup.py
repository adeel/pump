from setuptools import setup

desc = open("README").read()

setup(
  name="pump",
  version="0.1.0",
  description="A web application library.",
  long_description=desc,
  author="Adeel Ahmad Khan",
  author_email="adeel@adeel.ru",
  packages=["pump", "pump.util", "pump.middleware"],
  license="MIT",
  classifiers=[
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License'])