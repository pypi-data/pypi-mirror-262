from setuptools import setup, find_packages

setup(
    name='neon-connector',
    version='0.1.2',
    author='Timotius Marselo',
    author_email='timotiusmarselo@gmail.com',
    description='Connect to Neon DB and perform operations through Python.',
    url='https://github.com/supertypeai/neon_connector',
    packages=find_packages(where='src'),  # Look for packages in 'src' directory
    package_dir={'': 'src'},  # Specify the 'src' directory as the package director
    install_requires=[
        # List of dependencies required by your package
        'python-dotenv==1.0.0',
        'psycopg2==2.9.9',
        'pandas==2.2.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = ">=3.6"
)
