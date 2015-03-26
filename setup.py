from setuptools import setup, find_packages

setup(name='simpledatamigrate',
      version='0.0.1',
      author='Bifer Team',
      description='',
      platforms='Linux',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=[],
      install_requires=[line for line in open('requirements.txt')],
      entry_points={
          'console_scripts': ['migrate = migrate.postgres_schema_test:main']
      })
