from setuptools import setup, find_packages

setup(
    name="XpiumLibraryFlutter",
    version="0.0.6",
    author="Tassana Khrueawan",
    author_email="tassana.khr@gmail.com",
    description="Test Library for XpiumLibraryFlutter",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tassh571/XpiumLibraryFlutter.git",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'robotframework>=3.0', 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
