from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path
this_directory = Path(__file__).parent
# long_description = (this_directory / "readme.md").read_text()


VERSION = '0.1.3'
DESCRIPTION = 'CPR Python Package'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

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
    install_requires=['certifi', 'charset-normalizer', 'click', 'filelock', 'Flask', 'Flask-Cors', 'gensim', 'huggingface-hub', 'idna', 'itsdangerous', 'Jinja2', 'joblib', 'MarkupSafe', 'nltk', 'numpy', 'packaging', 'Pillow', 'pyparsing', 'PyYAML', 'regex', 'requests', 'scikit-learn', 'scipy', 'sentence-transformers', 'sentencepiece', 'six', 'smart-open', 'threadpoolctl', 'tokenizers', 'torch', 'torchvision', 'tqdm', 'transformers', 'typing_extensions', 'urllib3', 'Werkzeug'],
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