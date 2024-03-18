from distutils.core import setup
setup(
  name = 'umangchaudhary',         # How you named your package folder (MyLib)
  packages = ['umangchaudhary'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'personal lib',   # Give a short description about your library
  author = 'Umang Chaudhary',                   # Type in your name
  author_email = 'umang3934@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/nikrozine/umangchaudhary',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/nikrozine/umangchaudhary/archive/refs/tags/1.0.tar.gz',
  keywords = ['python', 'umangchaudhary', 'machine learning', 'ai'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)