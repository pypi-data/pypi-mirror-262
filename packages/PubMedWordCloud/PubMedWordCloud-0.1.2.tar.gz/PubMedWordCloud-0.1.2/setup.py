from setuptools import setup, find_packages

setup(
    name='PubMedWordCloud',
    version='0.1.2',
    packages=find_packages(),
    license='MIT',
    description='PubMedWordCloud is a Python package for generating word clouds from PubMed titles.',
    package_data={'PubMedWordCloud': ['nltk_data/corpora/stopwords/*']},
    author='Edris Sharif Rahmani',
    author_email='rahmani.biotech@gmail.com',
    url='https://github.com/sharifrahmanie/PubMedWordCloud',
    download_url='https://github.com/sharifrahmanie/PubMedWordCloud/archive/refs/tags/v0.1.tar.gz',
    keywords=['PubMed', 'Word Cloud', 'NLP', 'Bioinformatics'],
    install_requires=[
        'nltk',
        'matplotlib',
        'wordcloud',
        'Pillow',
        'numpy',
        'biopython',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)

