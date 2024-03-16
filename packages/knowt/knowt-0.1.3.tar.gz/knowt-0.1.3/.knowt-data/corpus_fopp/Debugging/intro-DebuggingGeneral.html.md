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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-DebuggingGeneral)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [3.1 Introduction to
        Debugging](intro-DebuggingGeneral.html){.reference .internal}
    -   [3.2 👩‍💻 Programming in the Real
        World](intro-HowtobeaSuccessfulProgrammer.html){.reference
        .internal}
    -   [3.4 👩‍💻 Beginning tips for
        Debugging](BeginningtipsforDebugging.html){.reference .internal}
    -   [3.5 Syntax errors](Syntaxerrors.html){.reference .internal}
    -   [3.6 Runtime Errors](RuntimeErrors.html){.reference .internal}
    -   [3.7 Semantic Errors](SemanticErrors.html){.reference .internal}
    -   [3.8 👩‍💻 Know Your Error
        Messages](KnowyourerrorMessages.html){.reference .internal}
    -   [3.9 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#introduction-to-debugging .section}
[3.1. ]{.section-number}Introduction to Debugging[¶](#introduction-to-debugging "Permalink to this heading"){.headerlink}
=========================================================================================================================

"The art of debugging is figuring out what you really told your program
to do rather than what you thought you told it to do."  --- Andrew
Singer

This chapter will spend some time talking about what happens when errors
occur as well as how to fix the errors that you will inevitably come
across.

Before computers became digital, debugging could mean looking for
insects impeding the functioning of physical relays as in this somewhat
[apocryphal
tale](https://www.computerworld.com/article/2515435/app-development/moth-in-the-machine--debugging-the-origins-of--bug-.html){.reference
.external} about [Admiral Grace
Hopper](https://en.wikipedia.org/wiki/Admiral_Grace_Hopper){.reference
.external}, a pioneer of computer programming.

Nowadays, debugging doesn't involve bug guts all over your computer but
it can still be just as frustrating. To cope with this frustration, this
chapter will present some strategies to help you understand why the
program you wrote does not behave as intended.

Many people think debugging is some kind of punishment for not being
smart enough to write code correctly the first time. But nobody does
that, failure in programming is part of the deal. Here's a fun video to
keep in mind as you learn to program.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#c0bsKc4tiuY .align-left .youtube-video component="youtube" video-height="315" question_label="3.1.1" video-width="560" video-videoid="c0bsKc4tiuY" video-divid="c0bsKc4tiuY" video-start="0" video-end="-1"}
:::
:::

CC BY--NC--ND 4.0 International [Ted.com](ted.com){.reference .external}

::: {#learning-goals .section}
[3.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------

-   To understand good programming strategies to avoid errors

-   To understand common kinds of exceptions and their likely causes
:::

::: {#objectives .section}
[3.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

-   Given a piece of code identify the Syntax errors based on error
    messages

-   Given a piece of code find the (ValueError, TypeError, SyntaxError,
    ParseError, NameError)
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

-   [[](toctree.html)]{#relations-prev}
-   [[](intro-HowtobeaSuccessfulProgrammer.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
