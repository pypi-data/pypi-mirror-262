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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-Sequences)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [6.1 Introduction: Sequences](intro-Sequences.html){.reference
        .internal}
    -   [6.2 Strings, Lists, and
        Tuples](StringsandLists.html){.reference .internal}
    -   [6.3 Index Operator: Working with the Characters of a
        String](IndexOperatorWorkingwiththeCharactersofaString.html){.reference
        .internal}
    -   [6.4 Disambiguating \[\]: creation vs
        indexing](DisabmiguatingSquareBrackets.html){.reference
        .internal}
    -   [6.5 Length](Length.html){.reference .internal}
    -   [6.6 The Slice Operator](TheSliceOperator.html){.reference
        .internal}
    -   [6.7 Concatenation and
        Repetition](ConcatenationandRepetition.html){.reference
        .internal}
    -   [6.8 Count and Index](CountandIndex.html){.reference .internal}
    -   [6.9 Splitting and Joining
        Strings](SplitandJoin.html){.reference .internal}
    -   [6.10 Exercises](Exercises.html){.reference .internal}
    -   [6.11 Chapter Assessment](week2a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#introduction-sequences .section}
[6.1. ]{.section-number}Introduction: Sequences[¶](#introduction-sequences "Permalink to this heading"){.headerlink}
====================================================================================================================

In the real world most of the data we care about doesn't exist on its
own. Usually data is in the form of some kind of collection or sequence.
For example, a grocery list helps us keep track of the individual food
items we need to buy, and our todo list organizes the things we need to
do each day. Notice that both the grocery list and the todo list are not
even concerned with numbers as much as they are concerned with words.
This is true of much of our daily life, and so Python provides us with
many features to work with lists of all kinds of objects (numbers,
words, etc.) as well as special kind of sequence, the character string,
which you can think of as a sequence of individual letters.

So far we have seen built-in types like: `int`{.docutils .literal
.notranslate}, `float`{.docutils .literal .notranslate}, and
`str`{.docutils .literal .notranslate}. `int`{.docutils .literal
.notranslate} and `float`{.docutils .literal .notranslate} are
considered to be simple or primitive or atomic data types because their
values are not composed of any smaller parts. They cannot be broken
down.

On the other hand, strings and lists are different from the others
because they are made up of smaller pieces. In the case of strings, they
are made up of smaller strings each containing one **character**.

Types that are comprised of smaller pieces are called **collection data
types**. Depending on what we are doing, we may want to treat a
collection data type as a single entity (the whole), or we may want to
access its parts. This ambiguity is useful.

In this chapter we will examine operations that can be performed on
sequences, such as picking out individual elements or subsequences
(called slices) or computing their length. In addition, we'll examine
some special functions that are defined only for strings, and we'll find
out one importance difference between strings and lists, that lists can
be changed (or mutated) while strings are immutable.

::: {#learning-goals .section}
[6.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------

-   To understand different operations that can be performed on strings,
    lists, and tuples

-   To distinguish between different uses of \[\] in Python
:::

::: {#objectives .section}
[6.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

-   Predict the output of split and join operations

-   Read and write expressions that use slices

-   Read and write expressions that use concatenation and repetition
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

-   [[](toctree.html)]{#relations-prev}
-   [[](StringsandLists.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
