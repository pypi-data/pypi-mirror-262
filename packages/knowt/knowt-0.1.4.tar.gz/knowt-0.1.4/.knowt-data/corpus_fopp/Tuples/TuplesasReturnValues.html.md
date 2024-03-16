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
        Problem](/runestone/default/reportabug?course=fopp&page=TuplesasReturnValues)
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
::: {#tuples-as-return-values .section}
[]{#index-0}

[13.4. ]{.section-number}Tuples as Return Values[¶](#tuples-as-return-values "Permalink to this heading"){.headerlink}
======================================================================================================================

Functions can return tuples as return values. This is very useful --- we
often want to know some batsman's highest and lowest score, or we want
to find the mean and the standard deviation, or we want to know the
year, the month, and the day, or if we're doing some ecological modeling
we may want to know the number of rabbits and the number of wolves on an
island at a given time. In each case, a function (which can only return
a single value), can create a single tuple holding multiple elements.

For example, we could write a function that returns both the area and
the circumference of a circle of radius r.

::: {.runestone .explainer .ac_section}
::: {#ac12_3_1 component="activecode" question_label="13.4.1"}
::: {#ac12_3_1_question .ac_question}
:::
:::
:::

Again, we can take advantage of packing to make the code look a little
more readable on line 4

::: {.runestone .explainer .ac_section}
::: {#ac12_3_2 component="activecode" question_label="13.4.2"}
::: {#ac12_3_2_question .ac_question}
:::
:::
:::

It's common to unpack the returned values into multiple variables.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_5 component="activecode" question_label="13.4.3"}
::: {#ac12_4_5_question .ac_question}
:::
:::
:::

**Check your Understanding**

::: {.runestone}
-   [Make the last two lines of the function be \"return x\" and
    \"return y\"]{#question12_4_1_opt_a}
-   As soon as the first return statement is executed, the function
    exits, so the second one will never be executed; only x will be
    returned
-   [Include the statement \"return \[x, y\]\"]{#question12_4_1_opt_b}
-   return \[x,y\] is not the preferred method because it returns x and
    y in a mutable list rather than a tuple which is more efficient. But
    it is workable.
-   [Include the statement \"return (x, y)\"]{#question12_4_1_opt_c}
-   return (x, y) returns a tuple.
-   [Include the statement \"return x, y\"]{#question12_4_1_opt_d}
-   return x, y causes the two values to be packed into a tuple.
-   [It\'s not possible to return two values; make two functions that
    each compute one value.]{#question12_4_1_opt_e}
-   It is possible, and frequently useful, to have one function compute
    multiple values.
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_3_3 component="activecode" question_label="13.4.5"}
::: {#ac12_3_3_question .ac_question}
Define a function called `information`{.docutils .literal .notranslate}
that takes as input, the variables `name`{.docutils .literal
.notranslate}, `birth_year`{.docutils .literal .notranslate},
`fav_color`{.docutils .literal .notranslate}, and `hometown`{.docutils
.literal .notranslate}. It should return a tuple of these variables in
this order.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_3_4 component="activecode" question_label="13.4.6"}
::: {#ac12_3_4_question .ac_question}
Define a function called `info`{.docutils .literal .notranslate} with
the following required parameters: `name`{.docutils .literal
.notranslate}, `age`{.docutils .literal .notranslate},
`birth_year`{.docutils .literal .notranslate},
`year_in_college`{.docutils .literal .notranslate}, and
`hometown`{.docutils .literal .notranslate}. The function should return
a tuple that contains all the inputted information.
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

-   [[](TupleAssignmentwithunpacking.html)]{#relations-prev}
-   [[](UnpackingArgumentsToFunctions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
