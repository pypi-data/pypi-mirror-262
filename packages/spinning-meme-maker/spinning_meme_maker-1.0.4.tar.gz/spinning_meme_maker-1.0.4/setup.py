from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='spinning_meme_maker',
    version='1.0.4',
    description='A package for creating spinning meme GIFs',
    long_description=long_description,
    long_description_content_type="text/markdown",
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