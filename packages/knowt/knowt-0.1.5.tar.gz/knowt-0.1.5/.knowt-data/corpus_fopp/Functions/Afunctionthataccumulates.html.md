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
        Problem](/runestone/default/reportabug?course=fopp&page=Afunctionthataccumulates)
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
::: {#a-function-that-accumulates .section}
[12.8. ]{.section-number}A function that accumulates[¶](#a-function-that-accumulates "Permalink to this heading"){.headerlink}
==============================================================================================================================

We have used the `len`{.docutils .literal .notranslate} function a lot
already. If it weren't part of python, our lives as programmers would
have been a lot harder.

Well, actually, not that much harder. Now that we know how to define
functions, we could define `len`{.docutils .literal .notranslate}
ourselves if it did not exist. Previously, we have used the accumlator
pattern to count the number of lines in a file. Let's use that same idea
and just wrap it in a function definition. We'll call it
`mylen`{.docutils .literal .notranslate} to distinguish it from the real
`len`{.docutils .literal .notranslate} which already exists. We actually
*could* call it len, but that wouldn't be a very good idea, because it
would replace the original len function, and our implementation may not
be a very good one.

::: {.runestone .explainer .ac_section}
::: {#ac11_5_1 component="activecode" question_label="12.8.1"}
::: {#ac11_5_1_question .ac_question}
:::
:::
:::

::: {.runestone .parsons-container}
::: {#pp11_5_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Rearrange the code statements to match the activecode window above.
(This is an exercise in noticing where the indenting and outdenting
happens, and where the return statement goes.)
:::

``` {.parsonsblocks question_label="12.8.2" style="visibility: hidden;"}
        def mylen(x):
---
    c = 0 # initialize count variable to 0
---
    for y in x:
---
        c = c + 1   # increment the counter for each item in x
---
    return c
---
print(mylen("hello"))
print(mylen([1, 2, 7]))
        
```
:::
:::

**Check your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac11_5_2 component="activecode" question_label="12.8.3"}
::: {#ac11_5_2_question .ac_question}
**1.** Write a function named `total`{.docutils .literal .notranslate}
that takes a list of integers as input, and returns the total value of
all those integers added together.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_5_3 component="activecode" question_label="12.8.4"}
::: {#ac11_5_3_question .ac_question}
**2.** Write a function called `count`{.docutils .literal .notranslate}
that takes a list of numbers as input and returns a count of the number
of elements in the list.
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

-   [[](TypeAnnotations.html)]{#relations-prev}
-   [[](Variablesandparametersarelocal.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
