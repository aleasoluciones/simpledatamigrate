from setuptools import setup, find_packages

setup(name='simpledatamigrate',
      version='0.0.1',
      author='Bifer Team',
      description='',
      platforms='Linux',
      packages=find_packages(exclude=['specs']),
      scripts=[],
      install_requires=['psycopg==3.2.13'],
      entry_points={
          'console_scripts': ['migrate = simpledatamigrate.postgres_schema:main',
                              'test_migrate = simpledatamigrate.test_postgres_schema:main']
      })
