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
        Problem](/runestone/default/reportabug?course=fopp&page=UnpackingArgumentsToFunctions)
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
::: {#unpacking-tuples-as-arguments-to-function-calls .section}
[13.5. ]{.section-number}Unpacking Tuples as Arguments to Function Calls[¶](#unpacking-tuples-as-arguments-to-function-calls "Permalink to this heading"){.headerlink}
======================================================================================================================================================================

Python even provides a way to pass a single tuple to a function and have
it be unpacked for assignment to the named parameters.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_6 component="activecode" question_label="13.5.1"}
::: {#ac12_4_6_question .ac_question}
:::
:::
:::

This won't quite work. It will cause an error, because the function add
is expecting two parameters, but you're only passing one parameter (a
tuple). If only there was a way to tell python to unpack that tuple and
use the first element to assign to x and the second to y.

Actually, there is a way.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_6b component="activecode" question_label="13.5.2"}
::: {#ac12_4_6b_question .ac_question}
:::
:::
:::

Don't worry about mastering this idea yet. But later in the course, if
you come across some code that someone else has written that uses the \*
notation inside a parameter list, come back and look at this again.
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

-   [[](TuplesasReturnValues.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
