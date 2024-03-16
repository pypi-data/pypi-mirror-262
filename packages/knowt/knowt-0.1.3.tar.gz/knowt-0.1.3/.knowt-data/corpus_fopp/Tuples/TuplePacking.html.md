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
        Problem](/runestone/default/reportabug?course=fopp&page=TuplePacking)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [13.1 Introduction](TuplePacking-Intro.html){.reference
        .internal}
    -   [13.2 Tuple Packing](TuplePacking.html){.reference .internal}
    -   [13.3 Tuple Assignment with
        Unpacking](TupleAssignmentwithunpacking.html){.reference
        .internal}
    -   [13.4 Tuples as Return
        Values](TuplesasReturnValues.html){.reference .internal}
    -   [13.5 Unpacking Tuples as Arguments to Function
        Calls](UnpackingArgumentsToFunctions.html){.reference .internal}
    -   [13.6 Glossary](Glossary.html){.reference .internal}
    -   [13.7 Exercises](Exercises.html){.reference .internal}
    -   [13.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#tuple-packing .section}
[13.2. ]{.section-number}Tuple Packing[¶](#tuple-packing "Permalink to this heading"){.headerlink}
==================================================================================================

Wherever python expects a single value, if multiple expressions are
provided, separated by commas, they are automatically **packed** into a
tuple. For example, we can omit the parentheses when assigning a tuple
of values to a single variable.

::: {.runestone .explainer .ac_section}
::: {#ac13-1-1 component="activecode" question_label="13.2.1"}
::: {#ac13-1-1_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [print(julia\[\'city\'\])]{#question12_2_1_opt_a}
-   julia is a tuple, not a dictionary; indexes must be integers.
-   [print(julia\[-1\])]{#question12_2_1_opt_b}
-   \[-1\] picks out the last item in the sequence.
-   [print(julia(-1))]{#question12_2_1_opt_c}
-   Index into tuples using square brackets. julia(-1) will try to treat
    julia as a function call, with -1 as the parameter value.
-   [print(julia(6))]{#question12_2_1_opt_d}
-   Index into tuples using square brackets. julia(-1) will try to treat
    julia as a function call, with -1 as the parameter value.
-   [print(julia\[7\])]{#question12_2_1_opt_e}
-   Indexing starts at 0. You want the seventh item, which is julia\[6\]
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_2_1 component="activecode" question_label="13.2.3"}
::: {#ac12_2_1_question .ac_question}
**2.** Create a tuple called `practice`{.docutils .literal .notranslate}
that has four elements: 'y', 'h', 'z', and 'x'.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_2_2 component="activecode" question_label="13.2.4"}
::: {#ac12_2_2_question .ac_question}
**3.** Create a tuple named `tup1`{.docutils .literal .notranslate} that
has three elements: 'a', 'b', and 'c'.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_2_3 component="activecode" question_label="13.2.5"}
::: {#ac12_2_3_question .ac_question}
**4.** Provided is a list of tuples. Create another list called
`t_check`{.docutils .literal .notranslate} that contains the third
element of every tuple.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_2_4 component="activecode" question_label="13.2.6"}
::: {#ac12_2_4_question .ac_question}
**5.** Below, we have provided a list of tuples. Write a for loop that
saves the second element of each tuple into a list called
`seconds`{.docutils .literal .notranslate}.
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

-   [[](TuplePacking-Intro.html)]{#relations-prev}
-   [[](TupleAssignmentwithunpacking.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
