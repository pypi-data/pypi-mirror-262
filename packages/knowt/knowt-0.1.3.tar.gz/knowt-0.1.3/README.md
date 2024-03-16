# Knowt
Knowt turns notes into knowledge.
You can search your notes for the name of that person you saw at the cafe last week or even have a conversation with your past self about anything at all.
It won't write your term paper for you, or draw you dreamy pictures, but it will help you remember the important things, the things that your favorite humans wrote down.

## Getting started
My favorite humans these days are on open source communities like Hacker Public Radio.
So `knowt` comes with all the show notes from every on of the 4,000+ HPR episodes recorded in its 15+ years of cointinuous broadcasting.
What questions do you have for the 100s of agalmic contributors to HPR?

```bash
$ pip install knowt
$ knowt what is Haycyon?
```


## Installation

#### Python virtual environment

To set up the project environment, follow these steps:

1. Clone the project repository or download the project files to your local machine.
2. Navigate to the project directory.
3. Create a Python virtual environment in the project directory:

```bash
pip install virtualenv
python -m virtualenv .venv
```

4. Activate the virtual environment (mac/linux):

```bash
source .venv/bin/activate
```

#### Install dependencies

Not that you have a virtual environment, you're ready to install some Python packages and download language models (spaCy and BERT).

1. Install the required packages using the `requirements.txt` file:

```bash
pip install -e .
```

2. Download the small BERT embedding model (you can use whichever open source model you like):

```bash
python -c 'from sentence_transformers import SentenceTransformer; sbert = SentenceTransformer("paraphrase-MiniLM-L6-v2")'
```

#### Quick start

You can search an example corpus of nutrition and health documents by running the `search_engine.py` script.

#### Search your personal docs

1. Replace the text files in `data/corpus` with your own.
2. Start the command-line search engine with:

```bash
python search_engine.py --refresh
```

The `--refresh` flag ensures that a fresh index is created based on your documents.
Otherwise it may ignore the `data/corpus` directory and reuse an existing index and corpus in the `data/cache` directory.

The `search_engine.py` script will first segement the text files into sentences.
Then it will create a "reverse index" by counting up words and character patterns in your documents.
It will also creat semantic embeddings to allow you to as questions about vague concepts without even knowing any the words you used in your documents.

## Contributing

Submit an Issue (bug or feature suggestion) or a Merge Request and someone will  respond within the week.
