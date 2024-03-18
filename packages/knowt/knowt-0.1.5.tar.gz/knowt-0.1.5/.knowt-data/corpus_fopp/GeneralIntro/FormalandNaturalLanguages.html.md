::: {#navbar .navbar .navbar-default .navbar-fixed-top role="navigation"}
::: {.container}
::: {.navbar-header}
[]{.icon-bar} []{.icon-bar} []{.icon-bar}

<div>

[![](../_static/img/RAIcon.png)](/runestone/default/user/login){.brand-logo}
[fopp](../index.html){#rs-book-toc-link .navbar-brand}

</div>
:::

::: {.navbar-collapse .collapse .navbar-ex1-collapse}
-   
-   []{#ad_warning}
-   []{#browsing_warning}
-   
-   [*[Search]{.visuallyhidden
    aria-label="Search"}*](#){.dropdown-toggle}
    -   [Table of Contents](../index.html)

    -   [Book Index](../genindex.html)

    -   

    -   ::: {.input-group}
        :::
-   
-   [*[User]{.visuallyhidden aria-label="User"}*](#){.dropdown-toggle}
    -   []{.loggedinuser}

    -   

    -   [Course Home](/ns/course/index)

    -   [Assignments](/assignment/student/chooseAssignment)

    -   [Practice](/runestone/assignments/practice)

    -   [[Peer Instruction
        (Instructor)](/runestone/peer/instructor.html)]{#inst_peer_link}

    -   [Peer Instruction (Student)](/runestone/peer/student.html)

    -   

    -   [Change Course](/runestone/default/courses)

    -   

    -   [[Instructor\'s
        Page](/runestone/admin/index)]{#ip_dropdown_link}

    -   [Progress Page](/runestone/dashboard/studentreport)

    -   

    -   [Edit Profile](/runestone/default/user/profile){#profilelink}

    -   [Change
        Password](/runestone/default/user/change_password){#passwordlink}

    -   [Register](/runestone/default/user/register){#registerlink}

    -   [Login](#)

    -   ::: {.slider .round}
        :::

        Dark Mode
-   
-   [[*[Scratch Activecode]{.visuallyhidden
    aria-label="Scratch Activecode"}*](javascript:runestoneComponents.popupScratchAC())]{#scratch_ac_link}
-   
-   [*[Help]{.visuallyhidden aria-label="Help"}*](#){.dropdown-toggle}
    -   [FAQ](http://runestoneinteractive.org/pages/faq.html)
    -   [Instructors Guide](https://guide.runestone.academy)
    -   
    -   [About Runestone](http://runestoneinteractive.org)
    -   [Report A
        Problem](/runestone/default/reportabug?course=fopp&page=FormalandNaturalLanguages)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [1.1 Introduction: The Way of the
        Program](intro-TheWayoftheProgram.html){.reference .internal}
    -   [1.2 Algorithms](Algorithms.html){.reference .internal}
    -   [1.3 The Python Programming
        Language](ThePythonProgrammingLanguage.html){.reference
        .internal}
    -   [1.4 Special Ways to Execute Python in this
        Book](SpecialWaystoExecutePythoninthisBook.html){.reference
        .internal}
    -   [1.5 More About Programs](MoreAboutPrograms.html){.reference
        .internal}
    -   [1.6 Formal and Natural
        Languages](FormalandNaturalLanguages.html){.reference .internal}
    -   [1.7 A Typical First
        Program](ATypicalFirstProgram.html){.reference .internal}
    -   [1.8 👩‍💻 Predict Before You
        Run!](WPPredictBeforeYouRun.html){.reference .internal}
    -   [1.9 👩‍💻 To Understand a Program, Change
        It!](WPToUnderstandaProgramChangeIt.html){.reference .internal}
    -   [1.10 Comments](Comments.html){.reference .internal}
    -   [1.11 Glossary](Glossary.html){.reference .internal}
    -   [1.12 Chapter Assessment](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#formal-and-natural-languages .section}
[1.6. ]{.section-number}Formal and Natural Languages[¶](#formal-and-natural-languages "Permalink to this heading"){.headerlink}
===============================================================================================================================

**Natural languages** are the languages that people speak, such as
English, Spanish, Korean, and Mandarin Chinese. They were not designed
by people (although people try to impose some order on them); they
evolved naturally.

**Formal languages** are languages that are designed by people for
specific applications. For example, the notation that mathematicians use
is a formal language that is particularly good at denoting relationships
among numbers and symbols. Chemists use a formal language to represent
the chemical structure of molecules. And most importantly:

> <div>
>
> *Programming languages are formal languages that have been designed to
> express computations.*
>
> </div>

Formal languages tend to have strict rules about syntax. For example,
`3+3=6`{.docutils .literal .notranslate} is a syntactically correct
mathematical statement, but `3=+6$`{.docutils .literal .notranslate} is
not. H~2~O is a syntactically correct chemical name, but ~2~Zz is not.

Syntax rules come in two flavors, pertaining to **tokens** and
structure. Tokens are the basic elements of the language, such as words,
numbers, and chemical elements. One of the problems with
`3=+6$`{.docutils .literal .notranslate} is that `$`{.docutils .literal
.notranslate} is not a legal token in mathematics (at least as far as we
know). Similarly, ~2~Zz is not legal because there is no element with
the abbreviation `Zz`{.docutils .literal .notranslate}.

The second type of syntax rule pertains to the **structure** of a
statement--- that is, the way the tokens are arranged. The statement
`3=+6$`{.docutils .literal .notranslate} is structurally illegal because
you can't place a plus sign immediately after an equal sign. Similarly,
molecular formulas have to have subscripts after the element name, not
before.

When you read a sentence in English or a statement in a formal language,
you have to figure out what the structure of the sentence is (although
in a natural language you do this subconsciously). This process is
called **parsing**.

For example, when you hear the sentence, "The other shoe fell", you
understand that the other shoe is the subject and fell is the verb. Once
you have parsed a sentence, you can figure out what it means, or the
**semantics** of the sentence. Assuming that you know what a shoe is and
what it means to fall, you will understand the general implication of
this sentence.

Although formal and natural languages have many features in common ---
tokens, structure, syntax, and semantics --- there are many differences:

ambiguity[¶](#term-ambiguity "Permalink to this term"){.headerlink}

:   Natural languages are full of ambiguity, which people deal with by
    using contextual clues and other information. Formal languages are
    designed to be nearly or completely unambiguous, which means that
    any statement has exactly one meaning, regardless of context.

redundancy[¶](#term-redundancy "Permalink to this term"){.headerlink}

:   In order to make up for ambiguity and reduce misunderstandings,
    natural languages employ lots of redundancy. As a result, they are
    often verbose. Formal languages are less redundant and more concise.

literalness[¶](#term-literalness "Permalink to this term"){.headerlink}

:   Formal languages mean exactly what they say. On the other hand,
    natural languages are full of idiom and metaphor. If someone says,
    "The other shoe fell", there is probably no shoe and nothing
    falling.

    ::: {.admonition .tip}
    Tip

    You'll need to find the original joke to understand the idiomatic
    meaning of the other shoe falling. *Yahoo! Answers* thinks it knows!
    :::

People who grow up speaking a natural language---that is,
everyone---often have a hard time adjusting to formal languages. In some
ways, the difference between natural and formal language is like the
difference between poetry and prose, but more so:

poetry[¶](#term-poetry "Permalink to this term"){.headerlink}

:   Words are used for their sounds as well as for their meaning, and
    the whole poem together creates an effect or emotional response.
    Ambiguity is not only common but often deliberate.

prose[¶](#term-prose "Permalink to this term"){.headerlink}

:   The literal meaning of words is more important, and the structure
    contributes more meaning. Prose is more amenable to analysis than
    poetry but still often ambiguous.

program[¶](#term-program "Permalink to this term"){.headerlink}

:   The meaning of a computer program is unambiguous and literal, and
    can be understood entirely by analysis of the tokens and structure.

Here are some suggestions for reading programs (and other formal
languages). First, remember that formal languages are much more dense
than natural languages, so it takes longer to read them. Also, the
structure is very important, so it is usually not a good idea to read
from top to bottom, left to right. Instead, learn to parse the program
in your head, identifying the tokens and interpreting the structure.
Finally, the details matter. Little things like spelling errors and bad
punctuation, which you can get away with in natural languages, can make
a big difference in a formal language.

**Check your understanding**

::: {.runestone}
-   [natural languages can be parsed while formal languages
    cannot.]{#question1_6_1_opt_a}
-   Actually both languages can be parsed (determining the structure of
    the sentence), but formal languages can be parsed more easily in
    software.
-   [ambiguity, redundancy, and literalness.]{#question1_6_1_opt_b}
-   All of these can be present in natural languages, but cannot exist
    in formal languages.
-   [there are no differences between natural and formal
    languages.]{#question1_6_1_opt_c}
-   There are several differences between the two but they are also
    similar.
-   [tokens, structure, syntax, and semantics.]{#question1_6_1_opt_d}
-   These are the similarities between the two.
:::

::: {.runestone}
-   [True]{#question1_6_2_opt_a}
-   It usually takes longer to read a program because the structure is
    as important as the content and must be interpreted in smaller
    pieces for understanding.
-   [False]{#question1_6_2_opt_b}
-   It usually takes longer to read a program because the structure is
    as important as the content and must be interpreted in smaller
    pieces for understanding.
:::
:::

::: {style="width: 100%"}
::: {ea-publisher="runestoneacademy" ea-type="image" style="display: flex; justify-content: center"}
:::
:::

::: {#scprogresscontainer}
You have attempted []{#scprogresstotal} of []{#scprogressposs}
activities on this page

::: {#subchapterprogress aria-label="Page progress"}
:::
:::

-   [[](MoreAboutPrograms.html)]{#relations-prev}
-   [[](ATypicalFirstProgram.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
