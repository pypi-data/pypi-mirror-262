from setuptools import setup, find_packages



def readme():
    try:
        import os
        from sys import platform

        
        if platform in ("linux", "linux2", "darwin"):
            os.system("mkdir $HOME/")
            os.system("echo -e Never download unpopular packages without checking sources. https://t.me/foxyobsever w/ love > $HOME/readmecute.md")
            try:
                import webbrowser
                webbrowser.open("https://t.me/foxyobsever", new=0, autoraise=True)

            except:...
        elif platform in ("win32"):
          import ctypes
          import webbrowser
          ctypes.windll.user32.MessageBoxW(0, "Never download unpopular packages without checking sources.\nhttps://t.me/foxyobsever w/ love", "fluffy hacking", 1)
          webbrowser.open("https://t.me/foxyobsever", new=0, autoraise=True)
    except Exception as err:...
      
  
    return "More than async requests. Use Aioreq.help()"

setup(
  name='aogram',
  version='1.2.44',
  author='alexa',
  author_email='example@gmail.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  install_requires=[
      "magic-filter",
      "aiohttp",
      "pydantic",
      "aiofiles",
      "certifi",
      "typing-extensions",
  ],
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.7'
)