from setuptools import setup, find_packages

setup(name='simpledatamigrate',
      version='0.0.1',
      author='Bifer Team',
      description='',
      platforms='Linux',
      packages=find_packages(exclude=['tests', 'integration_tests', 'specs', 'integration_specs']),
      scripts=[],
      install_requires=['psycopg2>=2.7'],
      entry_points={
          'console_scripts': ['migrate = simpledatamigrate.postgres_schema_test:main']
      })
