from setuptools import setup, find_packages
setup(
name='baraat',
version='1.1.7',
author='Project Baraat',
author_email='akash.kamalesh03@gmail.com',
description='''Project Baarat enhances accessibility to India's linguistic diversity through technology. It's an open-source initiative using LLMs for Indic-NLP tasks. Features include tokenizers for Indian languages and fine-tuned LLMs for accurate text generation. It fosters community-driven innovation and offers high-quality datasets for training. NOTE: The Kannada experts model is under development and is not meant to be used as of now. A future release will enable the model to be used for inference.''',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.9',
install_requires=[
    'transformers',
    'tokenizers',
    'datasets',
    'fasttext',
    'huggingface_hub',    
    'xformers==0.0.22.post7',
    'gradio',
    'bitsandbytes',
    'accelerate',
    'peft',
],
)