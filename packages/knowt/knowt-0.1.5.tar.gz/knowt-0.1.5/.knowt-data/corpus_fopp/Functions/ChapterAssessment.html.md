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
        Problem](/runestone/default/reportabug?course=fopp&page=ChapterAssessment)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [12.1 Introduction to
        Functions](intro-Functions.html){.reference .internal}
    -   [12.2 Function Definition](FunctionDefinitions.html){.reference
        .internal}
    -   [12.3 Function Invocation](FunctionInvocation.html){.reference
        .internal}
    -   [12.4 Function Parameters](FunctionParameters.html){.reference
        .internal}
    -   [12.5 Returning a value from a
        function](Returningavaluefromafunction.html){.reference
        .internal}
    -   [12.6 👩‍💻 Decoding a
        Function](DecodingaFunction.html){.reference .internal}
    -   [12.7 Type Annotations](TypeAnnotations.html){.reference
        .internal}
    -   [12.8 A function that
        accumulates](Afunctionthataccumulates.html){.reference
        .internal}
    -   [12.9 Variables and parameters are
        local](Variablesandparametersarelocal.html){.reference
        .internal}
    -   [12.10 Global Variables](GlobalVariables.html){.reference
        .internal}
    -   [12.11 Functions can call other functions
        (Composition)](Functionscancallotherfunctions.html){.reference
        .internal}
    -   [12.12 Flow of Execution
        Summary](FlowofExecutionSummary.html){.reference .internal}
    -   [12.13 👩‍💻 Print vs. return](Printvsreturn.html){.reference
        .internal}
    -   [12.14 Passing Mutable
        Objects](PassingMutableObjects.html){.reference .internal}
    -   [12.15 Side Effects](SideEffects.html){.reference .internal}
    -   [12.16 Glossary](Glossary.html){.reference .internal}
    -   [12.17 Exercises](Exercises.html){.reference .internal}
    -   [12.18 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#chapter-assessment .section}
[12.18. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
=============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac11_15_1 component="activecode" question_label="12.18.1"}
::: {#ac11_15_1_question .ac_question}
Write a function called `int_return`{.docutils .literal .notranslate}
that takes an integer as input and returns the same integer.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_15_2 component="activecode" question_label="12.18.2"}
::: {#ac11_15_2_question .ac_question}
Write a function called `add`{.docutils .literal .notranslate} that
takes any number as its input and returns that sum with 2 added.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_15_3 component="activecode" question_label="12.18.3"}
::: {#ac11_15_3_question .ac_question}
Write a function called `change`{.docutils .literal .notranslate} that
takes any string, adds "Nice to meet you!" to the end of the argument
given, and returns that new string.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_15_4 component="activecode" question_label="12.18.4"}
::: {#ac11_15_4_question .ac_question}
Write a function, `accum`{.docutils .literal .notranslate}, that takes a
list of integers as input and returns the sum of those integers.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_15_5 component="activecode" question_label="12.18.5"}
::: {#ac11_15_5_question .ac_question}
Write a function, `length`{.docutils .literal .notranslate}, that takes
in a list as the input. If the length of the list is greater than or
equal to 5, return "Longer than 5". If the length is less than 5, return
"Less than 5".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_15_6 component="activecode" question_label="12.18.6"}
::: {#ac11_15_6_question .ac_question}
You will need to write two functions for this problem. The first
function, `divide`{.docutils .literal .notranslate} that takes in any
number and returns that same number divided by 2. The second function
called `sum`{.docutils .literal .notranslate} should take any number,
divide it by 2, and add 6. It should return this new number. You should
call the `divide`{.docutils .literal .notranslate} function within the
`sum`{.docutils .literal .notranslate} function. Do not worry about
decimals.
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](../Tuples/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
