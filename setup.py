from setuptools import setup

setup(name='dynpy',
      version='1.0.0',
      description='Interact with the dynmap API from Python ',
      url='https://github.com/Ewpratten/dynpy',
      author='Evan Pratten',
      author_email='ewpratten@gmail.com',
      license='GPLv3',
      packages=['dynpy'],
      zip_safe=False,
      include_package_data=True,
      instapp_requires=[
            "requests",
            "numpy"
      ]
      )