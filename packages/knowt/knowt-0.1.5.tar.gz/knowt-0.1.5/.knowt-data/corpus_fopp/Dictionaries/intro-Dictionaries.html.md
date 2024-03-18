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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-Dictionaries)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [11.1 Introduction:
        Dictionaries](intro-DictionaryGoals.html){.reference .internal}
    -   [11.2 Getting Started with
        Dictionaries](intro-Dictionaries.html){.reference .internal}
    -   [11.3 Dictionary
        operations](Dictionaryoperations.html){.reference .internal}
    -   [11.4 Dictionary methods](Dictionarymethods.html){.reference
        .internal}
    -   [11.5 Aliasing and copying](Aliasingandcopying.html){.reference
        .internal}
    -   [11.6 Introduction: Accumulating Multiple Results In a
        Dictionary](intro-AccumulatingMultipleResultsInaDictionary.html){.reference
        .internal}
    -   [11.7 Accumulating Results From a
        Dictionary](AccumulatingResultsFromaDictionary.html){.reference
        .internal}
    -   [11.8 Accumulating the Best
        Key](AccumulatingtheBestKey.html){.reference .internal}
    -   [11.9 👩‍💻 When to use a
        dictionary](WPChoosingDictionaries.html){.reference .internal}
    -   [11.10 Glossary](Glossary.html){.reference .internal}
    -   [11.11 Exercises](Exercises.html){.reference .internal}
    -   [11.12 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#getting-started-with-dictionaries .section}
[]{#index-0}

[11.2. ]{.section-number}Getting Started with Dictionaries[¶](#getting-started-with-dictionaries "Permalink to this heading"){.headerlink}
==========================================================================================================================================

Here is a video to help introduce you to the important concepts in
creating and using Python dictionaries.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#goog_keyvalpairs .align-left .youtube-video component="youtube" video-height="315" question_label="11.2.1" video-width="560" video-videoid="eDQ19ahXsSk" video-divid="goog_keyvalpairs" video-start="0" video-end="-1"}
:::
:::

Let us look at an example of using a dictionary for a simple problem. We
will create a dictionary to translate English words into Spanish. For
this dictionary, the keys are strings and the values will also be
strings.

One way to create a dictionary is to start with the empty dictionary and
add **key-value pairs**. The empty dictionary is denoted `{}`{.docutils
.literal .notranslate}.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.2.2"}
::: {#clens10_1_1_question .ac_question}
:::

::: {#clens10_1_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.2.2 (clens10\_1\_1)]{.runestone_caption_text}
:::
:::

The first assignment creates an empty dictionary named
`eng2sp`{.docutils .literal .notranslate}. The other assignments add new
key-value pairs to the dictionary. The left hand side gives the
dictionary and the key being associated. The right hand side gives the
value being associated with that key. We can print the current value of
the dictionary in the usual way. The key-value pairs of the dictionary
are separated by commas. Each pair contains a key and a value separated
by a colon.

The order of the pairs may not be what you expected. Python uses complex
algorithms, designed for very fast access, to determine where the
key-value pairs are stored in a dictionary. For our purposes we can
think of this ordering as unpredictable
[[\[]{.fn-bracket}\*[\]]{.fn-bracket}](#id2){#id1 .footnote-reference
.brackets} .

Another way to create a dictionary is to provide a bunch of key-value
pairs using the same syntax as the previous output.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.2.3"}
::: {#clens10_1_2_question .ac_question}
:::

::: {#clens10_1_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.2.3 (clens10\_1\_2)]{.runestone_caption_text}
:::
:::

It doesn't matter what order we write the pairs. The values in a
dictionary are accessed with keys, not with indices, so there is no need
to care about ordering.

Here is how we use a key to look up the corresponding value.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.2.4"}
::: {#clens10_1_3_question .ac_question}
:::

::: {#clens10_1_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.2.4 (clens10\_1\_3)]{.runestone_caption_text}
:::
:::

The key `'two'`{.docutils .literal .notranslate} yields the value
`'dos'`{.docutils .literal .notranslate}. The key `one`{.docutils
.literal .notranslate} yields the value `uno`{.docutils .literal
.notranslate}.

**Check your understanding**

::: {.runestone}
-   [False]{#question10_1_1_opt_a}
-   Dictionaries associate keys with values but there is no assumed
    order for the entries.
-   [True]{#question10_1_1_opt_b}
-   Yes, dictionaries are associative collections meaning that they
    store key-value pairs.
:::

::: {.runestone}
-   [12]{#question10_1_2_opt_a}
-   12 is associated with the key cat.
-   [6]{#question10_1_2_opt_b}
-   Yes, 6 is associated with the key dog.
-   [23]{#question10_1_2_opt_c}
-   23 is associated with the key elephant.
-   [Error, you cannot use the index operator with a
    dictionary.]{#question10_1_2_opt_d}
-   The \[ \] operator, when used with a dictionary, will look up a
    value based on its key.
:::

::: {.runestone .explainer .ac_section}
::: {#ac10_1_1 component="activecode" question_label="11.2.7"}
::: {#ac10_1_1_question .ac_question}
**3.** Create a dictionary that keeps track of the USA's Olympic medal
count. Each key of the dictionary should be the type of medal (gold,
silver, or bronze) and each key's value should be the number of that
type of medal the USA's won. Currently, the USA has 33 gold medals, 17
silver, and 12 bronze. Create a dictionary saved in the variable
`medals`{.docutils .literal .notranslate} that reflects this
information.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac10_1_2 component="activecode" question_label="11.2.8"}
::: {#ac10_1_2_question .ac_question}
**4.** You are keeping track of olympic medals for Italy in the 2016 Rio
Summer Olympics! At the moment, Italy has 7 gold medals, 8 silver
medals, and 6 bronze medals. Create a dictionary called
`olympics`{.docutils .literal .notranslate} where the keys are the types
of medals, and the values are the number of that type of medals that
Italy has won so far.
:::
:::
:::

::: {#tabbed_ac10_3_6 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac10_3_6 component="activecode" question_label="11.2.9"}
::: {#ac10_3_6_question .ac_question}
Every four years, the summer Olympics are held in a different country.
Add a key-value pair to the dictionary `places`{.docutils .literal
.notranslate} that reflects that the 2016 Olympics were held in Brazil.
Do not rewrite the entire dictionary to do this!
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
Add the following line:

::: {.highlight-python .notranslate}
::: {.highlight}
    places['Brazil'] = 2016
:::
:::
:::
:::

[[\[]{.fn-bracket}[\*](#id1)[\]]{.fn-bracket}]{.label}

Instructors note: Python version 3.7 and later [provide ordering
guarantees](https://mail.python.org/pipermail/python-dev/2017-December/151283.html){.reference
.external}. However, it is best practice to write code that does not
rely on any particular key order so this book will treat key-value pairs
as unordered.
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

-   [[](intro-DictionaryGoals.html)]{#relations-prev}
-   [[](Dictionaryoperations.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
