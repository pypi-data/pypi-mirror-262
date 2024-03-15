from setuptools import setup, find_packages

setup(
    name='algo_fun_prime_number',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='Christophe Lagaillarde',
    author_email='chrislag94@gmail.com',
    description='Tell if a number is prime or not',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ChristopheLagaillarde/prime_number',
    package_data={'': ['*.asc']},

)

