# Visual Language Model for Remote Sensing 
#### **Internship by GISTDA on 2024/06/04 - Present** 

## Table of Contents

- **[Project Description](#project-description)**
- **[Literature Reading](#literature-reading)**
    - [Satellite Image Deep Learning](#satellite-image-deep-learning--github)
    - [Visual Language Models in Remote Sensing](#visual-language-models-in-remote-sensing--github)
        - [Complications of VLMs in RS](#complications-with-vlms-in-rs)
        - [Potential Solutions of VLM in RS](#potential-solutions-with-vlms-in-rs)
    - [SatGPT](#satgpt--github--website)
- **Requirements**
- **Installation**
- **Overview**
- **License**

## Literature Reading

### Satellite Image Deep learning | [GitHub](https://github.com/satellite-image-deep-learning)
The satellite-image-deep-learning organisation is a good way to start as it provides resources on deep learning applied to satellite and aerial imagery. They provide many useful repositories such as:
- datasets: lists many datasets 
- model-training-and-deployment: lists information on the training and deployment of deep learning models
- software: for working with satellite & aerial imagery data & datasets
- techniques: for deep learning with satellite & aerial imagery

### Visual Language Models in Remote Sensing | [GitHub](https://github.com/lzw-lzw/awesome-remote-sensing-vision-language-models.git)

This repo is more relevant and specific to our project as it involves all papers, research, code, dataset related to VLMs in Remote Sensing. 
#### Complications with VLMs for Remote Sensing

Good VLMs are produceds with a large dataset of image-text pairs. However in Remote Sensing, there is not enough image text pairs to create a good data set. (Many multitudes lower than usual)

In remote sensing, image-level classification assigns semantic labels like 'urban', 'forest', 'agricultural land' to images. However, complications arise when images contain multiple land cover types. This requires advanced techniques combining feature extraction and machine learning for accurate classification. 

#### Potential Solutions with VLMs for Remote Sensing

Recent research has demonstrated that fine-tuning large vision language models on small-scale, high-quality datasets can yield impressive performance in visual and language understanding.

### SatGPT | [GitHub](https://github.com/lalligagger/satgpt.git) | [Website](https://satgpt.net/) 
GPT for satellite mission planning
