from setuptools import setup, find_packages

setup(
    name='GEOMetadataDownloader',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='GEOMetadataDownloader is a Python package designed to effortlessly fetch and organize metadata information from GEO datasets. Seamlessly download and categorize metadata based on types such as RNA, SRA, and more into convenient spreadsheet formats.',
    author='Edris Sharif Rahmani',
    author_email='rahmani.biotech@gmail.com',
    url='https://github.com/sharifrahmanie/GEOMetadataDownloader',
    download_url='https://github.com/sharifrahmanie/GEOMetadataDownloader/archive/refs/tags/v_0.1.tar.gz',
    keywords=['Gene Expression Omnibus', 'GEO', 'Metadata', 'GSE series', 'GEO sample information'],
    install_requires=[
        'GEOparse',
        'tqdm',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)

