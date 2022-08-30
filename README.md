# DatGen
_A web application for creating your own image dataset_
![example workflow](https://github.com/martinagvilas/DatGen/actions/workflows/ci.yml/badge.svg)

TODO: Description of the problem, solution
## Using DatGen
Use DatGen to:
- Easily create your own customized image dataset through an intuitive web application.
- Decide which and how objects appear in your dataset using natural language input.
- Make use of human annotated public image datasets.
- Leverage multimodal AI systems capable of detecting and generating images matching your needs.

### :wrench: How to use?
Head over [here]() and start building your dataset. You will be able to choose, using text input and dropdown menus:
1. The objects that compose your dataset.
2. Their size with respect to the rest of the image.
3. Their visual attributes.
4. Their location.
5. The number of images you want for each object.
6. Whether to match the images in their contrast values.

DatGen will take care of scraping public image databases that match your input specifications, or leverage a multimodal deep generative model to create the images that you need.

You dataset will be generated in a matter of minutes and ready to download in compressed format!


## Reporting an issue
If you are experiencing an issue when using DatGen, or 
you simply want to leave some feedback, 
please open an [issue](https://github.com/martinagvilas/DatGen/issues).


## Installing DatGen locally
1. Clone this repository on your local machine
```
git clone https://github.com/martinagvilas/DatGen.git
```

2. Create a conda environment (optional)
```
conda create --name datgen python=3.9
conda activate datgen
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Install DatGen source code
```
pip install -e .
```

## Acknowledgements
DatGen is built on top of:
- [Streamlit](https://streamlit.io/), an open source tool for building web applications.
- [CLIP](https://github.com/openai/CLIP), a text-language deep learning model.
- [Dalle-mini](https://huggingface.co/spaces/dalle-mini/dalle-mini), a multimodal deep generative model. 