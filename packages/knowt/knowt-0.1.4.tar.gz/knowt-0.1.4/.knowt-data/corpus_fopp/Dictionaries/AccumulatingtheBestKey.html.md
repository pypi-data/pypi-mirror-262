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
        Problem](/runestone/default/reportabug?course=fopp&page=AccumulatingtheBestKey)
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
::: {#accumulating-the-best-key .section}
[]{#accumulating-best-key}

[11.8. ]{.section-number}Accumulating the Best Key[¶](#accumulating-the-best-key "Permalink to this heading"){.headerlink}
==========================================================================================================================

Now what if we want to find the *key* associated with the maximum value?
It would be nice to just find the maximum value as above, and then look
up the key associated with it, but dictionaries don't work that way. You
can look up the value associated with a key, but not the key associated
with a value. (The reason for that is there may be more than one key
that has the same value).

The trick is to have the accumulator keep track of the best key so far
instead of the best value so far. For simplicity, let's assume that
there are at least two keys in the dictionary. Then, similar to our
first version of computing the max of a list, we can initialize the
best-key-so-far to be the first key, and loop through the keys,
replacing the best-so-far whenever we find a better one.

In the exercise below, we have provided skeleton code. See if you can
fill it in. An answer is provided, but you'll learn more if you try to
write it yourself first.

::: {#q0 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac10_7_1 component="activecode" question_label="11.8.1"}
::: {#ac10_7_1_question .ac_question}
Write a program that finds the key in a dictionary that has the maximum
value. If two keys have the same maximum value, it's OK to print out
either one. Fill in the skeleton code
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer10_7_1 component="activecode" question_label="11.8.2"}
::: {#answer10_7_1_question .ac_question}
:::
:::
:::
:::
:::

**Check your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac10_7_2 component="activecode" question_label="11.8.3"}
::: {#ac10_7_2_question .ac_question}
**1.** Create a dictionary called `d`{.docutils .literal .notranslate}
that keeps track of all the characters in the string
`placement`{.docutils .literal .notranslate} and notes how many times
each character was seen. Then, find the key with the lowest value in
this dictionary and assign that key to `key_with_min_value`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac10_7_3 component="activecode" question_label="11.8.4"}
::: {#ac10_7_3_question .ac_question}
**5.** Create a dictionary called `lett_d`{.docutils .literal
.notranslate} that keeps track of all of the characters in the string
`product`{.docutils .literal .notranslate} and notes how many times each
character was seen. Then, find the key with the highest value in this
dictionary and assign that key to `key_with_max_value`{.docutils
.literal .notranslate}.
:::
:::
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

-   [[](AccumulatingResultsFromaDictionary.html)]{#relations-prev}
-   [[](WPChoosingDictionaries.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
