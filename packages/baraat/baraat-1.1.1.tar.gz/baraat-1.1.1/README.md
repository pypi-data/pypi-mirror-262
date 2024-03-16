## Welcome to Project Baraat!🎉
<div align="center">
   
   # Project Baraat
   
   <img src="https://github.com/asphytheghoul/Baarat/assets/91832216/f3438f2e-0c52-46b8-ae03-60764387d1f6">

</div>
<br/>

### View the project on [huggingface](https://huggingface.co/projectbaraat) and on [github](https://www.github.com/asphytheghoul/Baarat)

Project Baarat is an open-source initiative to leverage the power of
LLMs on Indic-NLP tasks. We aim to build Continually pre-trained, Task
Specific Language Models in a Mixture of Experts (MoE) setup through
domain adaptive pre-training. We plan on making a **multilingual**
**and**  **cross-lingual** LLM that is :

  
- 1\) Pre-trained on a large text corpus containing various sources of
knowledge including crawled wikipedia articles, textbooks, news,
social media sites, magazines etc.

- 2\) Continually pre-trained on different downstream tasks. We first
train a 7B LLaMa-2 model on an unsupervised text corpus in the target
language and save it as a base model. We have considered the following
tasks as downstream tasks that will be incorporated in the fine-tuning
process:

1. Machine Translation 
2. Question Answering 
3. Instruct Fine-Tuning
4. Logical Reasoning and Mathematical Capability


This notebook provides you a short walkthrough on loading and using our fine-tuned models. We currently have fine-tuned models on kannada and hindi languages on: 
- **Translation**: Translation support between the original base langauge, its Romanized form and English. Any combination of the same is accepted.
- **Question Answering**: Answering questions based on a context provided to the model. It can handle inputs in English, Romanized script or base language form and provide outputs as well in any combination of the above languages.
- **Instruct Tuned Tasks**: This expert is capable of handling any general queries that you may have and serves as a general purpose assistant. it is capable of handling inputs and replying in the base language or in English.

**Currently, the project is undergoing a critical update and the Kannada and Hindi models in specific are being retrained across all tasks. The current models were released only to serve the purpose of demonstrating a "Proof of Concept" of our approach of building language-specific task-specific Mixture of Experts (MOEs).**

**Coming Soon**:
- **Extending Support for Images and Audio:** In the future, we aim to expand Project Baarat's capabilities beyond text to include support for images and audio, enabling multimodal learning techniques.
- **Pipeline for Automated Dataset Cleaning:** We plan to develop a pipeline for dataset cleaning, leveraging small models like stabilityai/stablelm-zephyr-3b or microsoft/phi-2 for automated data cleaning processes.
- **Enhanced Reasoning Ability in Fine-Tuning:** We intend to introduce an additional step in fine-tuning to enhance the model's reasoning ability, integrating techniques for logical reasoning and inferencin using datasets like meta-math/MetaMathQA or microsoft/orca-math-word-problems-200k. We plan to release translated versions of the datasets to facilitate research in mathematical reasoning and question answering across diverse linguistic communities.

## Installation Instructions:
- The project utilizes the Unsloth framework for training and loading models,  before installing the package, we require that you install the appropriate version of unsloth based on your GPU's capability. Please find the below attached code from the Unsloth example notebook itself:
```python
%%capture
import torch
major_version, minor_version = torch.cuda.get_device_capability()
if major_version >= 8:
    # Use this for new GPUs like Ampere, Hopper GPUs (RTX 30xx, RTX 40xx, A100, H100, L40)
    !pip install "unsloth[colab_ampere] @ git+https://github.com/unslothai/unsloth.git"
else:
    # Use this for older GPUs (V100, Tesla T4, RTX 20xx)
    !pip install "unsloth[colab] @ git+https://github.com/unslothai/unsloth.git"
pass
```
- After installing unsloth, you will need to install seamless_communication by running the following : ```git clone https://github.com/facebookresearch/seamless_communication```

- Once you have unsloth installed, simply pip install the project by doing the following : ```pip install baraat```
- You can now follow along for the rest of the example. The code for this example can be found on this [notebook](https://colab.research.google.com/drive/13Esn2MUTdB2GzlEOPjWVFLT5IH6XOFca?usp=sharing)

## Support
This project is still in its infancy and is undergoing critical updates. We are working on a major update which should be released in a few weeks. We aim on improving the support with regards to the python package and the performance of the models as well. The Mixture of Experts models are undergoing a re-training phase and will be available soon. Please support the project on [github](https://www.github.com/asphytheghoul/Baarat). Consider giving the repository a star ⭐ if you liked what we are doing!