from setuptools import setup, find_packages

setup(
    name='algo_fun_fibonacci',
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
    description='Give the fibonacci sequence up and including a given number',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ChristopheLagaillarde/algo_fun_fibonacci',
    package_data={'': ['*.asc']},

)

