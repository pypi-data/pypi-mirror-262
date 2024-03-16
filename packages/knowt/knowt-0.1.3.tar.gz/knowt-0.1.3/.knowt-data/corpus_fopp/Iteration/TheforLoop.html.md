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
        Problem](/runestone/default/reportabug?course=fopp&page=TheforLoop)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [7.1 Introduction: Iteration](intro-Iteration.html){.reference
        .internal}
    -   [7.2 The for Loop](TheforLoop.html){.reference .internal}
    -   [7.3 Flow of Execution of the for
        Loop](FlowofExecutionoftheforLoop.html){.reference .internal}
    -   [7.4 Strings and for loops](Stringsandforloops.html){.reference
        .internal}
    -   [7.5 Lists and for loops](Listsandforloops.html){.reference
        .internal}
    -   [7.6 The Accumulator
        Pattern](TheAccumulatorPattern.html){.reference .internal}
    -   [7.7 Traversal and the for Loop: By
        Index](TraversalandtheforLoopByIndex.html){.reference .internal}
    -   [7.8 Nested Iteration: Image
        Processing](NestedIterationImageProcessing.html){.reference
        .internal}
    -   [7.9 👩‍💻 Printing Intermediate
        Results](WPPrintingIntermediateResults.html){.reference
        .internal}
    -   [7.10 👩‍💻 Naming Variables in For
        Loops](WPNamingVariablesinForLoops.html){.reference .internal}
    -   [7.11 The Gory Details:
        Iterables](GeneralizedSequences.html){.reference .internal}
    -   [7.12 👩‍💻 Keeping Track of Your Iterator Variable and Your
        Iterable](WPKeepingTrackofYourIteratorVariableYourIterable.html){.reference
        .internal}
    -   [7.13 Glossary](Glossary.html){.reference .internal}
    -   [7.14 Exercises](Exercises.html){.reference .internal}
    -   [7.15 Chapter Assessment](week2a2.html){.reference .internal}
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

::: {#the-for-loop .section}
[]{#index-0}

[7.2. ]{.section-number}The **for** Loop[¶](#the-for-loop "Permalink to this heading"){.headerlink}
===================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#forloopvid .align-left .youtube-video component="youtube" video-height="315" question_label="7.2.1" video-width="560" video-videoid="X1-UNHUajfk" video-divid="forloopvid" video-start="0" video-end="-1"}
:::
:::

Back when we drew the images with turtle it could be quite tedious. If
we wanted to draw a square then we had to move then turn, move then
turn, etc. etc. four times. If we were drawing a hexagon, or an octagon,
or a polygon with 42 sides, it would have been a nightmare to duplicate
all that code.

A basic building block of all programs is to be able to repeat some code
over and over again. We refer to this repetitive idea as **iteration**.
In this section, we will explore some mechanisms for basic iteration.

In Python, the **for** statement allows us to write programs that
implement iteration. As a simple example, let's say we have some
friends, and we'd like to send them each an email inviting them to our
party. We don't quite know how to send email yet, so for the moment
we'll just print a message for each friend.

::: {.runestone .explainer .ac_section}
::: {#ac6_2_1 component="activecode" question_label="7.2.2"}
::: {#ac6_2_1_question .ac_question}
:::
:::
:::

Take a look at the output produced when you press the `run`{.docutils
.literal .notranslate} button. There is one line printed for each
friend. Here's how it works:

-   **name** in this `for`{.docutils .literal .notranslate} statement is
    called the **loop variable** or, alternatively, the **iterator
    variable**.

-   The list of names in the square brackets is the sequence over which
    we will iterate.

-   Line 2 is the **loop body**. The loop body is always indented. The
    indentation determines exactly what statements are "in the loop".
    The loop body is performed one time for each name in the list.

-   On each *iteration* or *pass* of the loop, first a check is done to
    see if there are still more items to be processed. If there are none
    left (this is called the **terminating condition** of the loop), the
    loop has finished. Program execution continues at the next statement
    after the loop body.

-   If there are items still to be processed, the loop variable is
    updated to refer to the next item in the list. This means, in this
    case, that the loop body is executed here 7 times, and each time
    `name`{.docutils .literal .notranslate} will refer to a different
    friend.

-   At the end of each execution of the body of the loop, Python returns
    to the `for`{.docutils .literal .notranslate} statement, to see if
    there are more items to be handled.

The overall syntax is `for <loop_var_name> in <sequence>:`{.docutils
.literal .notranslate}

-   Between the words for and in, there must be a variable name for the
    loop variable. You can't put a whole expression there.

-   A colon is required at the end of the line

-   After the word in and before the colon is an expression that must
    evaluate to a sequence (e.g, a string or a list or a tuple). It
    could be a literal, or a variable name, or a more complex
    expression.
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

-   [[](intro-Iteration.html)]{#relations-prev}
-   [[](FlowofExecutionoftheforLoop.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
