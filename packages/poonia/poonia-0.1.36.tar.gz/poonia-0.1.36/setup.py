from setuptools import setup, find_packages

setup(
    name='poonia',
    version='0.1.36',
    description='Collection of small utilities',
    author='proteus',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        p=poonia.__main__:main
    ''',
    license='AGPLv3',
    license_files=('LICENSE.txt',),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities"
    ]
)
