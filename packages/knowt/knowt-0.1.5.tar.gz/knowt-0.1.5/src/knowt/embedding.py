""" Language models for tokenizing, sentencizing and embedding (encoding) natural language text:
* SpaCy (en_core_web_sm)
* BERT (all-MiniLM-L6-v2)
"""

from sentence_transformers import SentenceTransformer
import spacy
import time
import logging
import numpy as np

from knowt.search import TEXT_LABEL

log = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
nlp.add_pipe("sentencizer")


model = SentenceTransformer("all-MiniLM-L6-v2")
NUM_DIM = len(model.encode(["hi"])[0])


def encode_dataframe(df, encoder=model.encode, columns=[TEXT_LABEL]):
    """Generate embedding vectors, one for each row in the DataFrame.

    Embeddings are concatenated columnwise:
    >>> e1 = np.arange(6).reshape(2,3)
    >>> e1
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> e2 = np.arange(2, 14, 2).reshape(2,3)
    >>> e2
    array([[ 2,  4,  6],
           [ 8, 10, 12]])
    >>> np.array(np.concatenate([e2, e2], axis=1))
    array([[ 0,  1,  2,  2,  4,  6],
           [ 3,  4,  5,  8, 10, 12]])
    """
    if isinstance(columns, (str, int)):
        columns = [columns]
    log.info(
        f"Generating embeddings for {len(df)}x{len(columns)} documents (sentences)..."
    )
    embeddings = []
    for i, col in enumerate(columns):
        log.debug('Generating embeddings for column #{i}/{len(df)}, "{col}".')
        if isinstance(col, int):
            col = df.columns[col]
        num_tokens = df["num_tokens"].sum()
        num_chars = df[col].str.len().sum()
        t = time.time()
        embeddings.append(encoder(df[col].tolist(), show_progress_bar=True))
        t = time.time() - t
        log.info(
            f"Finished embedding in column {i}:{col} with {len(df)} documents ({num_tokens} tokens) in {t} s."
        )
        log.info(
            f"   {num_tokens/t/1000:.6f} token/ms\n   {num_chars/t/1000:.6f} char/ms"
        )

    return np.array(embeddings).T


def generate_passages(
    fin, min_line_len=0, max_line_len=1024, batch_size=1, num_dim=NUM_DIM
):
    """Crude rolling window chunking of text file: width=max_line_len, stride=max_line_len//2"""
    for line in fin:
        # Break up long lines into overlapping passages of text
        if len(line) > max_line_len:
            stride = max_line_len // 2
            for text in generate_passages(
                [line[i : i + max_line_len] for i in range(0, stride, len(line))]
            ):
                yield text
        yield line


def generate_batches(iterable, batch_size=1000):
    """Break an iterable into batches (lists of len batch_size containing iterable's objects)"""
    generate_batches.batch = []
    # TODO: preallocate numpy array with batch_size and increment i, truncating last numpy array
    for obj in iterable:
        generate_batches.batch.append(obj)
        if len(generate_batches.batch) >= batch_size:
            yield generate_batches.batch
            generate_batches.batch = []


generate_batches.batch = []


def generate_all_embeddings(df, encoder=model.encode, text_label=TEXT_LABEL):
    """Generate embedding vectors, one for each row in the DataFrame."""
    log.info(f"Generating embeddings for {len(df)} documents (sentences)...")
    num_tokens = df["num_tokens"].sum()
    num_chars = df[text_label].str.len().sum()
    t = time.time()
    embeddings = encoder(df[text_label].tolist(), show_progress_bar=True)
    t -= time.time()
    t *= -1
    log.info(f"Finished embedding {len(df)} sentences({num_tokens} tokens) in {t} s.")
    log.info(f"   {num_tokens/t/1000:.6f} token/ms\n   {num_chars/t/1000:.6f} char/ms")
    return embeddings
