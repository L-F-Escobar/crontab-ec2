from setuptools import setup

setup(
    name="CDS",
    version='0.1',
    py_modules=['cds.cli'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        cds=cds.cli:cli
    ''',
)
