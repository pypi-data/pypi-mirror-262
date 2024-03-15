from setuptools import setup, find_packages
import os

# def read_requirements():
#     cwd = os.getcwd()
#     path = os.path.join(cwd, 'requirements.txt')
#     with open(path) as req:
#         content = req.read()
#         requirements = content.split('\n')
#     return requirements

# requirements = read_requirements()

setup(
    name='img-to-pdf',
    version='1.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'makePDF=src.main:main',
        ],
    },
    author='Christopher Bannon',
    author_email='cbannon@berkeley.edu',
    description='Simple CLI tool to convert images in a directory to a PDF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cbannon35/makePDF',
    # install_requires=open('requirements.txt').read().splitlines(),
    #ERROR Backend subprocess exited when trying to invoke get_requires_for_build_wheel -- no such file :(
    install_requires=[
        "img2pdf==0.5.1",
        "Pillow==10.2.0",
        "pillow_heif==0.15.0",
        "PyPDF2==3.0.1",
        "setuptools==58.0.4",
        "tqdm==4.62.3"
    ],
    license='MIT',
    username="__token__",
    password="pypi-AgENdGVzdC5weXBpLm9yZwIkOGFkMTY3NzMtNGVhMC00ODk4LWFkOWMtMzgwM2QyYjBmYmViAAIqWzMsIjkyODNiYmUxLTM2NzUtNGRhZi04M2FlLTRmYzYzOGY4ZGJhYSJdAAAGIKDTnKxIqziEp-U7GccwjSOmGJ70Gfmv8C7PaOce2FJa",
    keywords='PDF, image, convert',
)