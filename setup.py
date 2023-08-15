from setuptools import setup

setup(
    name='spinque-query-api',
    version='0.0.1',
    description='Library to use the Spinque Query API in your Python project.',
    author='Spinque B.V.',
    author_email='chris@spinque.com',
    install_requires=['requests'],
    package_dir={'spinque_query_api': 'spinque-query-api'},
    packages=['spinque_query_api'],
    url='https://github.com/spinque/query-api-python/',
    license='MIT License'
)
