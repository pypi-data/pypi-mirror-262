from setuptools import setup, find_packages

setup(
    name='calculator',
    version='1.0.4',
    packages=find_packages(),
    description='A simple calculator package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Matheus Feliciano',
    author_email='matheusfelic16@gmail.com',
    url='https://github.com/TuringCollegeSubmissions/mfelic-DWWP.1.5',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
