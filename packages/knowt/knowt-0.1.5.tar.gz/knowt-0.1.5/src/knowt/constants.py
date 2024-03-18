# constants.py
import datetime
import logging
import os

from pathlib import Path

log = logging.getLogger(__name__)
OPENROUTER_API_KEY = None


def set_loglevel():
    global OPENROUTER_API_KEY, DEBUG, LOGLEVEL, logging, env, log
    env = dict(os.environ)
    DEBUG = env.get("DEBUG", "").strip()
    LOGLEVEL = env.get("LOGLEVEL", "WARNING").strip()
    if DEBUG and DEBUG.lower()[0] in "tyd1":
        DEBUG = True
        LOGLEVEL = "DEBUG"
    else:
        DEBUG = ""
    LOGLEVELS = dict(zip("diwef", "DEBUG INFO WARNING ERROR FATAL".split()))
    if LOGLEVEL:
        LOGLEVEL = LOGLEVELS.get(LOGLEVEL.lower()[0], "")

    if LOGLEVEL:
        logging.basicConfig(level=getattr(logging, LOGLEVEL))
    try:
        log = logging.getLogger(__name__)
    except NameError:
        log = logging.getLogger("llm.__main__")
    OPENROUTER_API_KEY = env.get("OPENROUTER_API_KEY", None)
    return env, log


env, log = set_loglevel()

try:
    import dotenv  # noqa - dotenv is installed with `knowt[all]` or `knowt[llm]`

    dotenv.load_dotenv()
    env, log = set_loglevel()
    assert OPENROUTER_API_KEY is not None, "ADD YOUR OPENROUTER_API_KEY TO .env FILE!"
except Exception as e:
    log.info(str(e))
    log.warning(
        "Unable to import `dotenv` or no `.env` file found.\n"
        "The dotenv package is not needed unless you plan to use external LLM services."
    )
try:
    # Will only work
    BASE_DIR = Path(__file__).parent.parent.parent
    assert (BASE_DIR / "src").is_dir()
except Exception:
    BASE_DIR = Path.home() / ".knowt-data"
DATA_DIR = BASE_DIR / ".knowt-data"
DATA_DIR.mkdir(exist_ok=True)
GLOBS = ("**/*.txt", "**/*.md")  # add preprocessors for ReST and HTML

CORPUS_HPR = DATA_DIR / "corpus_hpr"
CORPUS_NUTRITION = DATA_DIR / "corpus_nutrition"
CORPUS_DIR = CORPUS_HPR

CORPUS_DIR.mkdir(exist_ok=True)
TEXT_LABEL = "sentence"
DF_PATH = CORPUS_DIR / f"{TEXT_LABEL}s.csv.bz2"
EMBEDDINGS_PATH = DF_PATH.with_suffix(".embeddings.joblib")
EXAMPLES_PATH = DF_PATH.with_suffix(".search_results.csv")

TODAY = datetime.date.today()
RAG_SEARCH_LIMIT = 8
RAG_MIN_RELEVANCE = 0.5
RAG_TEMPERATURE = 0.05
RAG_SELF_HOSTED = True
RAG_MAX_NEW_TOKENS = 256
