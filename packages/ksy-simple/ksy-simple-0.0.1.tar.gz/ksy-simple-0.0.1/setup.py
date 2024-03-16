from setuptools import setup, find_packages

setup(
    name='ksy-simple',
    version='0.0.1',
    description='PYPI tutorial package creation written by kyeob',
    author='kyeob',
    author_email='koak1107@gmail.com',
    url='https://github.com/kyeob1107/package_upload_test',
    install_requires=['numpy'],
    packages=find_packages(exclude=[]),
    keywords=['kyeob', 'python code kata', 'python tutorial', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)