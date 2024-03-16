from setuptools import setup, find_packages
setup(
name='baraat',
version='0.0.1',
author='Project Baraat',
author_email='akash.kamalesh03@gmail.com',
description='''Project Baarat enhances accessibility to India's linguistic diversity through technology. It's an open-source initiative using LLMs for Indic-NLP tasks. Features include tokenizers for Indian languages and fine-tuned LLMs for accurate text generation. It fosters community-driven innovation and offers high-quality datasets for training. NOTE: The Kannada experts model is under development and is not meant to be used as of now. A future release will enable the model to be used for inference.''',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.9',
)