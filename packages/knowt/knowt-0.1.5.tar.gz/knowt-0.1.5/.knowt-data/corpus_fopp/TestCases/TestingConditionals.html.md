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
        Problem](/runestone/default/reportabug?course=fopp&page=TestingConditionals)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [18.1 Introduction: Test Cases](intro-TestCases.html){.reference
        .internal}
    -   [18.2 Checking Assumptions About Data
        Types](TestingTypes.html){.reference .internal}
    -   [18.3 Checking Other
        Assumptions](CheckingOtherAssumptions.html){.reference
        .internal}
    -   [18.4 Testing Conditionals](TestingConditionals.html){.reference
        .internal}
    -   [18.5 Testing Loops](TestingLoops.html){.reference .internal}
    -   [18.6 Writing Test Cases for
        Functions](Testingfunctions.html){.reference .internal}
    -   [18.7 Testing Optional
        Parameters](TestingOptionalParameters.html){.reference
        .internal}
    -   [18.8 👩‍💻 Test Driven
        Development](WPProgramDevelopment.html){.reference .internal}
    -   [18.9 Glossary](Glossary.html){.reference .internal}
    -   [18.10 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [18.11 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#testing-conditionals .section}
[18.4. ]{.section-number}Testing Conditionals[¶](#testing-conditionals "Permalink to this heading"){.headerlink}
================================================================================================================

Ideally, you want tests that will cover both the typical execution of
your program and tests for unusual things that might happen, which are
called **edge cases**.

If the code has conditional blocks (`if..elif..else`{.docutils .literal
.notranslate}) then you'll want to have tests that check that the right
block executes when you expect it to. For example, in the code below, z
is set to the smaller of x and y, but if they are equal then we set z to
0. Our code even includes a comment to help us keep track of when we
think the final code block should execute.

::: {.highlight-python .notranslate}
::: {.highlight}
    if x < y:
        z = x
    else:
        if x > y:
            z = y
        else:
            ## x must be equal to y
            z = 0
:::
:::

When you start to have complex conditionals, it's helpful to add
comments like that, and once you do you might as well add an assert
statement. If the assert ever causes an error, you'll be grateful to
know right away that something has gone wrong and you'll have a good
start on where to look for debugging. In this case, you'll never get an
error, no matter the values of x and y.

::: {.runestone .explainer .ac_section}
::: {#ac19_1c_1 component="activecode" question_label="18.4.1"}
::: {#ac19_1c_1_question .ac_question}
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

-   [[](CheckingOtherAssumptions.html)]{#relations-prev}
-   [[](TestingLoops.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
