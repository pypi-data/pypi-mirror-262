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
        Problem](/runestone/default/reportabug?course=fopp&page=TestingOptionalParameters)
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
::: {#testing-optional-parameters .section}
[18.7. ]{.section-number}Testing Optional Parameters[¶](#testing-optional-parameters "Permalink to this heading"){.headerlink}
==============================================================================================================================

If a function takes an optional parameter, one of the edge cases to test
for is when no parameter value is supplied during execution. That will
test whether the default value is being set correctly when the parameter
is omitted.

Consider the following function, which counts the number of "long
enough" words in a list. What counts as long enough is determined by an
optional parameter, `min_length`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac19_2_3 component="activecode" question_label="18.7.1"}
::: {#ac19_2_3_question .ac_question}
:::
:::
:::

What return value tests could we write to check whether it is
implemented correctly? First, we could construct a list of words that
has words of many lengths, including a degenerate empty string that has
length 0. One return value test would omit `min_length`{.docutils
.literal .notranslate} and check that we got the right count. Other
return value tests would supply `min_length`{.docutils .literal
.notranslate} and would include the edge case where
`min_length`{.docutils .literal .notranslate} is 0 and one where it is
very large.

::: {.runestone .explainer .ac_section}
::: {#ac19_2_3b component="activecode" question_label="18.7.2"}
::: {#ac19_2_3b_question .ac_question}
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

-   [[](Testingfunctions.html)]{#relations-prev}
-   [[](WPProgramDevelopment.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
