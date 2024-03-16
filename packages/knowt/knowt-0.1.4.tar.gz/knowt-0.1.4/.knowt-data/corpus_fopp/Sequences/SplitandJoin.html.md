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
        Problem](/runestone/default/reportabug?course=fopp&page=SplitandJoin)
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
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#splitting-and-joining-strings .section}
[6.9. ]{.section-number}Splitting and Joining Strings[¶](#splitting-and-joining-strings "Permalink to this heading"){.headerlink}
=================================================================================================================================

Two of the most useful methods on strings involve lists of strings. The
`split`{.docutils .literal .notranslate} method breaks a string into a
list of words. By default, any number of whitespace characters is
considered a word boundary.

![shows the phrase \"leaders and best\" being split on
spaces](../_images/split_default.gif)

::: {.runestone .explainer .ac_section}
::: {#ac5_9_1 component="activecode" question_label="6.9.1"}
::: {#ac5_9_1_question .ac_question}
:::
:::
:::

An optional argument called a **delimiter** can be used to specify which
characters to use as word boundaries.

![shows example of splitting \"leaders and best\" on
\"e\"](../_images/split_on_e.jpeg)

The following example uses the string `ai`{.docutils .literal
.notranslate} as the delimiter:

::: {.runestone .explainer .ac_section}
::: {#ac5_9_2 component="activecode" question_label="6.9.2"}
::: {#ac5_9_2_question .ac_question}
:::
:::
:::

Notice that the delimiter doesn't appear in the result.

The inverse of the `split`{.docutils .literal .notranslate} method is
`join`{.docutils .literal .notranslate}. You choose a desired
**separator** string, (often called the *glue*) and join the list with
the glue between each of the elements.

![shows process of a \"/\" separating the words \"leaders\", \"and\",
\"best\"](../_images/join.gif)

::: {.runestone .explainer .ac_section}
::: {#ac5_9_3 component="activecode" question_label="6.9.3"}
::: {#ac5_9_3_question .ac_question}
:::
:::
:::

The list that you glue together (`wds`{.docutils .literal .notranslate}
in this example) is not modified. Also, you can use empty glue or
multi-character strings as glue.

**Check your understanding**

::: {.runestone .explainer .ac_section}
::: {#ac5_9_4 component="activecode" question_label="6.9.4"}
::: {#ac5_9_4_question .ac_question}
Create a new list of the 6th through 13th elements of `lst`{.docutils
.literal .notranslate} (eight items in all) and assign it to the
variable `output`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_9_5 component="activecode" question_label="6.9.5"}
::: {#ac5_9_5_question .ac_question}
Create a variable `output`{.docutils .literal .notranslate} and assign
to it a list whose elements are the words in the string `str1`{.docutils
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

-   [[](CountandIndex.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
