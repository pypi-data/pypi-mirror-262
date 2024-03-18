# Part 1 - Motivation and demo

#### Outline
1. Motivation and demo
  - Goals:
    - private
    - teachable
    - aligned (honest+compliant)
    - transparent (humble)
    - reliable (no "halucenation")
    - loyal
  - gitlab.com/tangibleai/community/knowt
  - NLPiA release date? 

## HPR Script

There are some questions that you would never trust with corporate "AI".
Do you take notes at school, work or ... life?
Ever wanted to know what you wrote down at your last exam?
What about the name of that cute person with the mishievious smile that you saw at San Diego Tech Coffee?
You probably have that info in a text file on your laptop somewhere, but you probably haven't ever used the word "mischievous" in the notes you jot down in a rush.
You may forget those details unless you have a tool like knowt to help you resurface them.
All you need to do is put your text notes into the "data/corpus" directory and knowt will take care of the rest.

Under the hood, Knowt implements a RAG (Retrieval Augmented Generative model).
So knowt first processes your private text files to create a searchable index of each passage of text you provide.
This gives it to perform "semantic search" on this indexed data blazingly fast, without using approximations.
See the project [final report](docs/Information Retrieval Systems.pdf) for more details.
To index a 10k documents should take less than a minute, and adding new documents takes seconds.
And answers to your questions take milliseconds.
Even if you wanted to ask some general question about some fact on Wikipedia, that would take less than a second (though indexing those 10M text stings took 3-4 hours on my two-yr-old laptop).
