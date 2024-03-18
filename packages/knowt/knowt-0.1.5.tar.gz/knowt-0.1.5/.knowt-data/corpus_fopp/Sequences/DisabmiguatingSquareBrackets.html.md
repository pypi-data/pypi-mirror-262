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
        Problem](/runestone/default/reportabug?course=fopp&page=DisabmiguatingSquareBrackets)
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

::: {#disambiguating-creation-vs-indexing .section}
[6.4. ]{.section-number}Disambiguating \[\]: creation vs indexing[¶](#disambiguating-creation-vs-indexing "Permalink to this heading"){.headerlink}
===================================================================================================================================================

Square brackets `[]`{.docutils .literal .notranslate} are used in quite
a few ways in python. When you're first learning how to use them it may
be confusing, but with practice and repetition they'll be easy to
incorporate!

You have currently encountered two instances where we have used square
brackets. The first is creating lists and the second is indexing. At
first glance, creating and indexing are difficult to distinguish.
However, indexing requires referencing an already created list while
simply creating a list does not.

::: {.runestone .explainer .ac_section}
::: {#ac5_4_1 component="activecode" question_label="6.4.1"}
::: {#ac5_4_1_question .ac_question}
:::
:::
:::

In the code above, a new list is created using the empty brackets. Since
there's nothing in it though, we can't index into it.

::: {.runestone .explainer .ac_section}
::: {#ac5_4_2 component="activecode" question_label="6.4.2"}
::: {#ac5_4_2_question .ac_question}
:::
:::
:::

In the code above, you'll see how, now that we have elements inside of
`new_lst`{.docutils .literal .notranslate}, we can index into it. In
order to extract an element of the list, we do use `[]`{.docutils
.literal .notranslate}, but we first have to specify which list we are
indexing. Imagine if there was another list in the activecode. How would
python know which list we want to index into if we don't tell it?
Additionally, we have to specify what element we want to extract. This
belongs inside of the brackets.

Though it may be easier to distinguish in this above activecode, below
may be a bit more difficult.

::: {.runestone .explainer .ac_section}
::: {#ac5_4_3 component="activecode" question_label="6.4.3"}
::: {#ac5_4_3_question .ac_question}
:::
:::
:::

Here, we see a list called `lst`{.docutils .literal .notranslate} being
assigned to a list with one element, zero. Then, we see how
`n_lst`{.docutils .literal .notranslate} is assigned the value
associated with the first element of lst. Dispite the variable names,
only one of the above variables is assigned to a list. Note that in this
example, what sets creating apart from indexing is the reference to the
list to let python know that you are extracting an element from another
list.

::: {.runestone}
-   [w = \[a\]]{#question5_4_1_opt_a}
-   No, due to the way the code was written it creates a list. This list
    would have one element which is the value assigned to the
    variable a.
-   [y = a\[\]]{#question5_4_1_opt_b}
-   Though this tries to use indexing, it does not specify what element
    should be taken from a.
-   [x = \[8\]]{#question5_4_1_opt_c}
-   No, this is an example of creating a list.
-   [t = a\[0\]]{#question5_4_1_opt_d}
-   Yes, this will using indexing to get the value of the first element
    of a.
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

-   [[](IndexOperatorWorkingwiththeCharactersofaString.html)]{#relations-prev}
-   [[](Length.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
