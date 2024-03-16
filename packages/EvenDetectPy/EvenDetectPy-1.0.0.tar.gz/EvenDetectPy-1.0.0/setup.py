from setuptools import setup, find_packages

setup(
    name='EvenDetectPy',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    author='Toby Killen',
    author_email='itoby24@gmail.com',
    description='A small package to detect if a number is even.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-package-name',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
