from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'CPR Package for PKiL'
LONG_DESCRIPTION = 'A package that allows for the use of PKiL in CPR'

# Setting up
setup(
    name="cpkil",
    version=VERSION,
    author="Jinendra Malekar",
    author_email="<jmalekar@email.sc.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['certifi==2022.9.24', 'charset-normalizer==2.1.1', 'click==8.1.3', 'filelock==3.8.0', 'Flask==2.2.2', 'Flask-Cors==3.0.10', 'gensim==4.2.0', 'huggingface-hub==0.9.1', 'idna==3.4', 'itsdangerous==2.1.2', 'Jinja2==3.1.2', 'joblib==1.2.0', 'MarkupSafe==2.1.1', 'nltk==3.7', 'numpy==1.24.1', 'packaging==21.3', 'Pillow==9.2.0', 'pyparsing==3.0.9', 'PyYAML==6.0', 'regex==2022.9.13', 'requests==2.31.0', 'scikit-learn==1.2.2', 'scipy==1.9.1', 'sentence-transformers==2.2.2', 'sentencepiece==0.1.97', 'six==1.16.0', 'smart-open==6.2.0', 'threadpoolctl==3.1.0', 'tokenizers==0.12.1', 'torch==2.2.1', 'torchvision==0.13.1', 'tqdm==4.64.1', 'transformers==4.22.1', 'typing_extensions==4.6.1', 'urllib3==1.26.12', 'Werkzeug==2.2.2'],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)