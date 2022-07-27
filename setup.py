from setuptools import setup
 
setup(
    name='ImageDuplicateFinder',
    version='0.6.0',
    author='Michael Hermelschmidt',
    author_email='mail.hermel@gmail.com',
    packages=['image_duplicate_finder'],
    url='http://pypi.python.org/pypi/picture_duplicate_finder/',
    license='LICENSE.txt',
    description='Simple duplication finder for Images, matches on names and then compares image hashes.',
    entry_points={
        'console_scripts': ['idf = image_duplicate_finder:find_duplicate_argparse']},
    
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=[
        "ImageHash==4.2.1"
    ],
)
