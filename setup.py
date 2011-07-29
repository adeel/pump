from setuptools import setup

setup(
  name="pump",
  version="0.1.1",
  description="A web application library.",
  author="Adeel Ahmad Khan",
  author_email="adeel@adeel.ru",
  packages=["pump", "pump.util", "pump.middleware"],
  license="MIT",
  classifiers=[
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License'])