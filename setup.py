from setuptools import setup
 
setup(
    name='ImageDuplicateFinder',
    version='0.1.0',
    author='Michael Hermelschmidt',
    author_email='mail.hermel@gmail.com',
    packages=['image_duplicate_finder'],
    url='http://pypi.python.org/pypi/picture_duplicate_finder/',
    license='LICENSE.txt',
    description='Simple duplication finder for Images, matches on names and then compares image hashes.',
    entry_points={
        'console_scripts': ['idf = image_duplicate_finder.__init__:find_duplicates']},
    long_description=open('README.md').read(),
    install_requires=[
        "ImageHash==4.2.1"
    ],
)