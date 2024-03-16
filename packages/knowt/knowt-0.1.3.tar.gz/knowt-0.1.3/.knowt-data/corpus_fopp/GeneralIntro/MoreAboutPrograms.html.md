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
        Problem](/runestone/default/reportabug?course=fopp&page=MoreAboutPrograms)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [1.1 Introduction: The Way of the
        Program](intro-TheWayoftheProgram.html){.reference .internal}
    -   [1.2 Algorithms](Algorithms.html){.reference .internal}
    -   [1.3 The Python Programming
        Language](ThePythonProgrammingLanguage.html){.reference
        .internal}
    -   [1.4 Special Ways to Execute Python in this
        Book](SpecialWaystoExecutePythoninthisBook.html){.reference
        .internal}
    -   [1.5 More About Programs](MoreAboutPrograms.html){.reference
        .internal}
    -   [1.6 Formal and Natural
        Languages](FormalandNaturalLanguages.html){.reference .internal}
    -   [1.7 A Typical First
        Program](ATypicalFirstProgram.html){.reference .internal}
    -   [1.8 👩‍💻 Predict Before You
        Run!](WPPredictBeforeYouRun.html){.reference .internal}
    -   [1.9 👩‍💻 To Understand a Program, Change
        It!](WPToUnderstandaProgramChangeIt.html){.reference .internal}
    -   [1.10 Comments](Comments.html){.reference .internal}
    -   [1.11 Glossary](Glossary.html){.reference .internal}
    -   [1.12 Chapter Assessment](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#more-about-programs .section}
[]{#index-0}

[1.5. ]{.section-number}More About Programs[¶](#more-about-programs "Permalink to this heading"){.headerlink}
=============================================================================================================

A **program** is a sequence of instructions that specifies how to
perform a computation. The computation might be something as complex as
rendering an html page in a web browser or encoding a video and
streaming it across the network. It can also be a symbolic computation,
such as searching for and replacing text in a document or (strangely
enough) compiling a program.

The details look different in different languages, but a few basic
instructions appear in just about every language.

input

:   Get data from the keyboard, a file, or some other device.

output

:   Display data on the screen or send data to a file or other device.

math and logic

:   Perform basic mathematical operations like addition and
    multiplication and logical operations like `and`{.docutils .literal
    .notranslate}, `or`{.docutils .literal .notranslate}, and
    `not`{.docutils .literal .notranslate}.

conditional execution

:   Check for certain conditions and execute the appropriate sequence of
    statements.

repetition

:   Perform some action repeatedly, usually with some variation.

Believe it or not, that's pretty much all there is to it. Every program
you've ever used, no matter how complicated, is made up of instructions
that look more or less like these. Thus, we can describe programming as
the process of breaking a large, complex task into smaller and smaller
subtasks until the subtasks are simple enough to be performed with
sequences of these basic instructions.

::: {#preview-of-control-structures .section}
[1.5.1. ]{.section-number}Preview of Control Structures[¶](#preview-of-control-structures "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------------------------------------

We won't get too much into python control structures yet, but it is good
to mention them early to give you a taste for what you can do with the
language! If these make sense to you now, that's great! However, we
don't expect you to understand these yet - understanding will come
later.

First we have structures that allow us to iterate over something. We can
look at strings character-by-character or lists item-by-item until we've
reached the end of them by using something called a `for`{.docutils
.literal .notranslate} loop.

::: {.runestone .explainer .ac_section}
::: {#ac1_5_1 component="activecode" question_label="1.5.1.1"}
::: {#ac1_5_1_question .ac_question}
:::
:::
:::

We can also iterate without a definite stopping point with
`while`{.docutils .literal .notranslate} loops. You might use this if
you want to receive input from the user of your program but you don't
know how long it'll take for them to be done with your code.

::: {.runestone .explainer .ac_section}
::: {#ac1_5_2 component="activecode" question_label="1.5.1.2"}
::: {#ac1_5_2_question .ac_question}
:::
:::
:::

Other structures will allow us to only run parts of our programs or only
do some task if a certain set of conditions are found. Conditionals, as
they're called, allow us to do that. Check out how adding conditionals
to our code can change what we can write about regarding grocery
shopping.

::: {.runestone .explainer .ac_section}
::: {#ac1_5_3 component="activecode" question_label="1.5.1.3"}
::: {#ac1_5_3_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [a sequence of instructions that specifies how to perform a
    computation.]{#question1_5_1_opt_a}
-   It is just step-by-step instructions that the computer can
    understand and execute. Programs often implement algorithms, but
    note that algorithms are typically less precise than programs and do
    not have to be written in a programming language.
-   [something you follow along at a play or
    concert.]{#question1_5_1_opt_b}
-   True, but not in this context. We mean a program as related to a
    computer.
-   [a computation, even a symbolic computation.]{#question1_5_1_opt_c}
-   A program can perform a computation, but by itself it is not one.
-   [the same thing as an algorithm.]{#question1_5_1_opt_d}
-   Programs often implement algorithms, but they are not the same
    thing. An algorithm is a step by step list of instructions, but
    those instructions are not necessarily precise enough for a computer
    to follow. A program must be written in a programming language that
    the computer knows how to interpret.
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

-   [[](SpecialWaystoExecutePythoninthisBook.html)]{#relations-prev}
-   [[](FormalandNaturalLanguages.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
