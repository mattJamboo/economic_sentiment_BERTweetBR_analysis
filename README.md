# Economic Sentiment Machine Learning Analysis

This repository contains notebooks and source code for an undergraduate research project on economic sentiment in Brazilian political tweets related to the 2022 presidential election.
We would like to thank Fernando Carneiro, Daniela Vianna, Jonnathan Carvalho, Alexandre Plastino & Aline Paes for training BERTweetBR and making it publicly available.

## Project Structure

- `src/data_treatment/`: data extraction, normalization, filtering, and manual labeling notebooks.
- `src/notebooks/`: sentiment and economic-topic modeling experiments.
- `src/president_sentiment_analysis/`: candidate mention analysis, economic discourse interactions, and result visualizations.
- `data/`: expected location for local datasets. The directory is kept in the repository with `.gitkeep`, but its contents are ignored.

## Data

The datasets are not included in this public repository. To reproduce the notebooks, place the required files in the `data/` directory.

The notebooks use relative paths through:

```python
from src.imports import DATA_DIR
```

This avoids machine-specific paths and allows the project to run from different local environments.

## Ignored Files

The repository intentionally ignores:

- raw and processed datasets in `data/`;
- generated figures, including `.png` and `.PNG` files;
- trained model artifacts such as `.pkl`, `.pt`, and `.pth`;
- Word/PDF drafts and temporary files.

## Environment

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

Some notebooks may require access to Hugging Face models. Do not store access tokens in notebooks or source files. Use an interactive login or environment variable instead.
