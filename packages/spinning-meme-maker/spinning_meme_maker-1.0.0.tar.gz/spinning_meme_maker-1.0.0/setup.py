from setuptools import setup, find_packages

setup(
    name='spinning_meme_maker',
    version='1.0.0',
    description='A package for creating spinning meme GIFs',
    author='Overtimepog',
    author_email='truen2005@gmail.com',
    packages=find_packages(),
    install_requires=[
        'panda3d',
        'Pillow',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'spinning_meme_maker=spinning_meme_maker.spin:spinning',
        ],
    },
)