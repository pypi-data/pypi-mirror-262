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
        Problem](/runestone/default/reportabug?course=fopp&page=FlowofExecutionoftheforLoop)
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
::: {#flow-of-execution-of-the-for-loop .section}
[]{#index-0}

[7.3. ]{.section-number}Flow of Execution of the for Loop[¶](#flow-of-execution-of-the-for-loop "Permalink to this heading"){.headerlink}
=========================================================================================================================================

As a program executes, the interpreter always keeps track of which
statement is about to be executed. We call this the **control flow**, or
the **flow of execution** of the program. When humans execute programs,
they often use their finger to point to each statement in turn. So you
could think of control flow as "Python's moving finger".

Control flow until now has been strictly top to bottom, one statement at
a time. We call this type of control **sequential**. Sequential flow of
control is always assumed to be the default behavior for a computer
program. The `for`{.docutils .literal .notranslate} statement changes
this.

Flow of control is often easy to visualize and understand if we draw a
flowchart. This flowchart shows the exact steps and logic of how the
`for`{.docutils .literal .notranslate} statement executes.

[![](../_images/new_flowchart_for.png){.align-center}](../_images/new_flowchart_for.png){.reference
.internal .image-reference}

::: {.admonition .note}
Note

Not sure what a flowchart is? Check out this funny take on it, in
[XKCD](http://xkcd.com/518/){.reference .external}. [And this
one](http://xkcd.com/1195/){.reference .external}.
:::

A codelens demonstration is a good way to help you visualize exactly how
the flow of control works with the for loop. Try stepping forward and
backward through the program by pressing the buttons. You can see the
value of `name`{.docutils .literal .notranslate} change as the loop
iterates through the list of friends.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="7.3.1"}
::: {#vtest_question .ac_question}
:::

::: {#vtest .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 7.3.1 (vtest)]{.runestone_caption_text}
:::
:::

While loops may not seem to be necessary when you're iterating over a
few items, it is extremely helpful when iterating over lots of items.
Imagine if you needed to change what happened in the code block. On the
left, when you use iteration, this is easy. On the right, when you have
hard coded the process, this is more difficult.

[![Demonstration of using iteration over hard coding the
iteration.](../_images/iteration_vs_hardcoding.png){.align-center}](../_images/iteration_vs_hardcoding.png){.reference
.internal .image-reference}
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

-   [[](TheforLoop.html)]{#relations-prev}
-   [[](Stringsandforloops.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
