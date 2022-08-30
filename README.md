# DatGen
_A web application for creating your own image dataset_

## Using DatGen
DatGen allows you to:
- Easily create your own customized image dataset through an intuitive web application.
- Decide which and how objects appear in your dataset using natural language input.
- Make use of human annotated public datasets.
- Leverage multimodal AI systems capable of detecting and generating images matching your needs.

If you want to start using DatGen, head over [here]().

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
DatGen is built on top of [streamlit](https://streamlit.io/),
an open source tool for building web applications.