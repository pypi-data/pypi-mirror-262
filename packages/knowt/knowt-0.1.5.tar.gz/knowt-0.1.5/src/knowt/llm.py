"""
Create RAG to answer questions using a VectorDB(globs=['data/corpus/**/*.txt']) of text files

>>> from knowt.constants import DATA_DIR
>>> rag = RAG(min_relevance=.5, temperature=0.05)  # (`db=DATA_DIR / 'corpus_hpr/'`)
>>> q = 'Explain phone phreaking to me'
>>> kwds = 'phreak teleph experi'.split()
>>> ans = rag.ask(q)
>>> for t in kwds:
>>>     assert t in ans.lower(), f"{t} not found in {ans.lower()}"

ans[:69] = 'Phreaking is the practice of studying, experimenting with, or explori'

>>> rag = RAG(db=DATA_DIR / 'corpus_nutrition')
>>> q = 'What is the healthiest fruit?'
>>> kwds = 'glycemic diabetes fat coconut raw'.split() + ['organic berries']
>>> ans = rag.ask(q)
>>> for t in kwds:
>>>     assert t in ans.lower(), f"{t} not found in {ans.lower()}"

ans[:69] = 'The healthiest fruits recommended for people with diabetes and glycem'

>>> q = 'How much exercise is healthiest?'
>>> kwds = 'exercis healthy'.split() + ['not specified']
>>> ans = rag.ask(q)
>>> for t in kwds:
>>>     assert t in ans.lower(), f"{t} not found in {ans.lower()}"

ans[:69] = 'The amount of exercise that is healthy for an individual is not speci'
"""

import sys
import logging
from pathlib import Path

from openai import OpenAI
from transformers import pipeline

from knowt.search import VectorDB
from knowt.constants import RAG_SEARCH_LIMIT, RAG_MIN_RELEVANCE, OPENROUTER_API_KEY
from knowt.constants import RAG_TEMPERATURE, RAG_SELF_HOSTED, RAG_MAX_NEW_TOKENS

try:
    log = logging.getLogger(__name__)
except NameError:
    log = logging.getLogger("llm.__main__")


try:
    CLIENT = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
except Exception:
    CLIENT = None

# globals().update(env)
LLM_MODELS = (
    "meta-llama/llama-2-13b-chat",  # openrouter expensive
    "openai/gpt-3.5-turbo",  # openrouter free?
    "auto",  # unknown?
    "stanford-crfm/alias-gpt2-small-x21",  # openrouter <500MB
    # 'open-orca/mistral-7b-openorca',  # openrouter cheaper/better than Llama-2-13
    "Open-Orca/Mistral-7B-OpenOrca",  # huggingface
    # 'mistralai/mistral-7b-instruct',  # openrouter free
    "mistralai/Mistral-7B-Instruct-v0.2",  # huggingface
)

LLM_MODEL_DICT = {s.split("/")[0].lower().split("-")[0].lower(): s for s in LLM_MODELS}
LLM_MODEL_DICT = {s.split("/")[0].lower().split("-")[-1].lower(): s for s in LLM_MODELS}
LLM_MODEL_DICT.update(
    {s.split("/")[-1].lower().split("-")[0].lower(): s for s in LLM_MODELS}
)
LLM_MODEL_DICT.update(
    {s.split("/")[-1].lower().split("-")[-1].lower(): s for s in LLM_MODELS}
)
LLM_MODEL = LLM_MODELS[-1]
SELF_HOSTED = True

PROMPT_EXAMPLES = []
PROMPT_EXAMPLES.append(
    [
        "PUG meetup",
        "2024-01-27",
        "You are an elementary school student answering questions on a reading comprehension test. "
        "Your answers must only contain information from the passage of TEXT provided. "
        "Read the following TEXT and answer the QUESTION below the text as succintly as possible. "
        "Do not add any information or embelish your answer. "
        "You will be penalized if you include information not contained in the TEXT passage. \n\n"
        "TEXT: {context}\n\n"
        "QUESTION: {question}\n\n",
    ]
)
PROMPT_EXAMPLES.append(
    [
        "Vish benchmark",
        "2024-02-01",
        "You are an elementary school student answering questions on a reading comprehension test. "
        "Your answers must only contain information from the passage of TEXT provided. "
        "Read the following TEXT and answer the QUESTION below the text as succinctly as possible. "
        "Do not add any information or embelish your answer. "
        "You will be penalized if your ANSWER includes any information not contained in the passage of TEXT provided above the QUESTION. \n\n"
        "TEXT: {context}\n\n"
        "QUESTION: {question}\n\n"
        "ANSWER: ",
    ]
)
PROMPT_EXAMPLES.append(
    [
        "reading comprehension exam",
        "2024-02-12",
        "You are an elementary school student answering questions on a reading comprehension exam. \n"
        "To answer the exam QUESTION, first read the TEXT provided to see if it contains enough information to answer the QUESTION. \n"
        "Read the TEXT provided below and answer the QUESTION as succinctly as possible. \n"
        "Your ANSWER should only contain the facts within the TEXT. \n"
        "If the TEXT provided does not contain enough information to answer the QUESTION you should ANSWER with \n "
        "'I do not have enough information to answer your question.'. \n"
        "You will be penalized if your ANSWER includes any information not contained in the TEXT provided. \n\n"
        "TEXT: {context}\n\n"
        "QUESTION: {question}\n\n"
        "ANSWER: ",
    ]
)
PROMPT_EXAMPLES.append(
    [
        "search results comprehension exam",
        "2024-02-24",
        "You are an elementary school student answering questions on a reading comprehension exam. \n"
        "To answer the exam QUESTION, first read the SEARCH_RESULTS to see if it contains enough information to answer the QUESTION. \n"
        "Read the SEARCH_RESULTS provided below and answer the QUESTION as succinctly as possible. \n"
        "Your ANSWER should only contain facts from found in the SEARCH_RESULTS. \n"
        "If SEARCH_RESULTS text does not contain enough information to answer the QUESTION you should ANSWER with \n "
        "'The question cannot be answered based on the search results provided.'. \n"
        "You will be penalized if your ANSWER includes any information not contained in SEARCH_RESULTS. \n\n"
        "SEARCH_RESULTS: {context}\n\n"
        "QUESTION: {question}\n\n"
        "ANSWER: ",
    ]
)


RAG_PROMPT_TEMPLATE = PROMPT_EXAMPLES[-1][-1]


def get_model(model=LLM_MODEL):
    return LLM_MODEL_DICT.get(model, model)


class RAG:

    def __init__(
        self,
        prompt_template=RAG_PROMPT_TEMPLATE,
        llm_model_name=LLM_MODEL,
        search_limit=RAG_SEARCH_LIMIT,
        min_relevance=RAG_MIN_RELEVANCE,
        client=None,
        db=None,
        self_hosted=RAG_SELF_HOSTED,
        temperature=RAG_TEMPERATURE,
        max_new_tokens=RAG_MAX_NEW_TOKENS,
    ):
        self.pipe = None
        self.temperature = temperature = min(temperature or 0, RAG_TEMPERATURE)
        self.max_new_tokens = max_new_tokens or RAG_MAX_NEW_TOKENS
        self.self_hosted = bool(self_hosted) or SELF_HOSTED
        global CLIENT
        client = client or CLIENT
        self.client = client
        self.prompt_template = prompt_template
        self.llm_model_name = get_model(llm_model_name or LLM_MODEL)
        self.hist = []
        self.search_limit = search_limit or RAG_SEARCH_LIMIT
        self.min_relevance = min_relevance or RAG_MIN_RELEVANCE

        if self_hosted:
            self.pipe = pipeline("text-generation", model=self.llm_model_name)

        if not db:
            self.db = VectorDB(
                search_limit=self.search_limit, min_relevance=self.min_relevance
            )
        elif not isinstance(db, VectorDB):
            db = Path(db)
            self.db = VectorDB(
                db, search_limit=self.search_limit, min_relevance=self.min_relevance
            )

    def setattrs(self, *args, **kwargs):
        if len(args) and isinstance(args[0], dict):
            kwargs.update(args[0])
        for k, v in kwargs.items():
            # TODO: try/except better here
            if not hasattr(self, k):
                log.error(
                    f'No such attribute "{k}" in a {self.__class__.__name__} class!'
                )
                raise AttributeError(
                    f"No such attribute in a {self.__class__.__name__} class!"
                )
            setattr(self, k, v)

    def ask(
        self,
        question,
        context=0,
        search_limit=None,
        min_relevance=None,
        prompt_template=None,
        **kwargs,
    ):
        """Ask the RAG a question, optionally reusing previously retrieved context strings

        Args:
          context (int|str): A str will be used directly in the LLM prompt.
            -1 => last context from history of chat queries
             0 => refresh the context using the VectorDB for semantic search
             1 => use the first context retrieved this session
             2 => use the 2nd context retrieved this session
        """
        self.question = question
        self.search_limit = search_limit = search_limit or self.search_limit
        self.min_relevance = min_relevance = min_relevance or self.min_relevance
        self.prompt_template = prompt_template = prompt_template or self.prompt_template
        self.setattrs(kwargs)
        if (not context or context in [0, "refresh", "", None]) or not len(self.hist):
            topdocs = self.db.search(question, limit=search_limit)
            topdocs = topdocs[topdocs["relevance"] > min_relevance]
            context = "\n".join(list(topdocs[self.db.text_label]))
        if isinstance(context, int):
            try:
                context = self.hist[context]["context"]
            except IndexError:
                context = self.hist[-1]["context"]
        self.context = context = context or "Search returned 0 results."
        self.hist.append(
            {k: getattr(self, k) for k in "question context prompt_template".split()}
        )
        prompt = self.prompt_template.format(**self.hist[-1])  # **vars(self))
        results = self.run_model(prompt)
        self.hist[-1].update(results)  # answer=completion['content']
        for k, v in results.items():
            setattr(self, k, v)
        # TODO: function to flatten an openAI Completion object into a more open-standard interoperable format
        # FIXME: .hist rows should each be temporarily stored in a .turn dict with well-defined schema accepted by all functions
        return self.answer

    def run_model(self, prompt, self_hosted=None, max_new_tokens=None):
        self.max_new_tokens = max_new_tokens or self.max_new_tokens
        if self_hosted is not None:
            self.self_hosted = self_hosted
        if self.self_hosted:
            if not self.pipe:
                self.pipe = self.pipe = pipeline("text-generation", self.llm_model_name)
            self.answer = self.pipe(prompt, max_new_tokens=max_new_tokens)[0][
                "generated_text"
            ]
            self.answers = [(self.answer, 0)]
            self.answer_logprob = 0
            self.answer_id = f"self_hosted_{len(self.hist)+1}"
        else:
            self.completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://qary.ai",  # Optional, for including your app on openrouter.ai rankings.
                    "X-Title": "https://qary.ai",  # Optional. Shows in rankings on openrouter.ai.
                },
                model=self.llm_model_name,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            self.answers = [
                (cc.message.content, cc.logprobs) for cc in self.completion.choices
            ]
            self.answer, self.answer_logprob = self.answers[0]
            self.answer_id = self.completion.id
        return dict(
            answers=self.answers,
            answer=self.answer,
            answer_id=self.answer_id,
            answer_logprob=self.answer_logprob,
        )


def main():
    question = " ".join(sys.argv[1:])
    rag = RAG()
    answers = [rag.ask(question)]
    # answers = ask_llm(
    #     question=question,
    #     model='auto',
    #     context='',
    #     prompt_template=PROMPT_NO_CONTEXT)
    print(answers + "\n")


if __name__ == "__main__":
    main()
