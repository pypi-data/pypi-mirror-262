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
        Problem](/runestone/default/reportabug?course=fopp&page=StringsandLists)
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
::: {#strings-lists-and-tuples .section}
[6.2. ]{.section-number}Strings, Lists, and Tuples[¶](#strings-lists-and-tuples "Permalink to this heading"){.headerlink}
=========================================================================================================================

Throughout the first chapters of this book we have used strings to
represent words or phrases that we wanted to print out. Our definition
was simple: a string is simply some characters inside quotes. In this
chapter we explore strings in much more detail.

Additionally, we explore lists and tuples, which are very much like
strings but can hold different types.

::: {#strings .section}
[6.2.1. ]{.section-number}Strings[¶](#strings "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#stringintro .align-left .youtube-video component="youtube" video-height="315" question_label="6.2.1.1" video-width="560" video-videoid="T435lvYXE_w" video-divid="stringintro" video-start="0" video-end="-1"}
:::
:::

Strings can be defined as sequential collections of characters. This
means that the individual characters that make up a string are in a
particular order from left to right.

A string that contains no characters, often referred to as the **empty
string**, is still considered to be a string. It is simply a sequence of
zero characters and is represented by '' or "" (two single or two double
quotes with nothing in between).
:::

::: {#lists .section}
[6.2.2. ]{.section-number}Lists[¶](#lists "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#listintro .align-left .youtube-video component="youtube" video-height="315" question_label="6.2.2.1" video-width="560" video-videoid="mrwSbE5MDn0" video-divid="listintro" video-start="0" video-end="-1"}
:::
:::

A **list** is a sequential collection of Python data values, where each
value is identified by an index. The values that make up a list are
called its **elements**. Lists are similar to strings, which are ordered
collections of characters, except that the elements of a list can have
any type and for any one list, the items can be of different types.

There are several ways to create a new list. The simplest is to enclose
the elements in square brackets ( `[`{.docutils .literal .notranslate}
and `]`{.docutils .literal .notranslate}).

::: {.highlight-python .notranslate}
::: {.highlight}
    [10, 20, 30, 40]
    ["spam", "bungee", "swallow"]
:::
:::

The first example is a list of four integers. The second is a list of
three strings. As we said above, the elements of a list don't have to be
the same type. The following list contains a string, a float, an
integer, and another list.

::: {.highlight-python .notranslate}
::: {.highlight}
    ["hello", 2.0, 5, [10, 20]]
:::
:::

::: {.admonition .note}
Note

WP: Don't Mix Types!

You'll likely see us do this in the textbook to give you odd
combinations, but when you create lists you should generally not mix
types together. A list of just strings or just integers or just floats
is generally easier to deal with.
:::
:::

::: {#tuples .section}
[6.2.3. ]{.section-number}Tuples[¶](#tuples "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------

A **tuple**, like a list, is a sequence of items of any type. The
printed representation of a tuple is a comma-separated sequence of
values, enclosed in parentheses. In other words, the representation is
just like lists, except with parentheses () instead of square brackets
\[\].

One way to create a tuple is to write an expression, enclosed in
parentheses, that consists of multiple other expressions, separated by
commas.

::: {.highlight-python .notranslate}
::: {.highlight}
    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
:::
:::

The key difference between lists and tuples is that a tuple is
immutable, meaning that its contents can't be changed after the tuple is
created. We will examine the mutability of lists in detail in the
chapter on [[Mutability]{.std
.std-ref}](../TransformingSequences/Mutability.html#mutability){.reference
.internal}.

To create a tuple with a single element (but you're probably not likely
to do that too often), we have to include the final comma, because
without the final comma, Python treats the `(5)`{.docutils .literal
.notranslate} below as an integer in parentheses:

::: {.runestone .explainer .ac_section}
::: {#ac5_2_1 component="activecode" question_label="6.2.3.1"}
::: {#ac5_2_1_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [False]{#question5_2_1_opt_a}
-   Yes, unlike strings, lists can consist of any type of Python data.
-   [True]{#question5_2_1_opt_b}
-   Lists are heterogeneous, meaning they can have different types of
    data.
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

-   [[](intro-Sequences.html)]{#relations-prev}
-   [[](IndexOperatorWorkingwiththeCharactersofaString.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
