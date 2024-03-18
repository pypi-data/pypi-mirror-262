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
        Problem](/runestone/default/reportabug?course=fopp&page=BreakandContinue)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [14.1 Introduction](intro-indefiniteiteration.html){.reference
        .internal}
    -   [14.2 The while Statement](ThewhileStatement.html){.reference
        .internal}
    -   [14.3 The Listener Loop](listenerLoop.html){.reference
        .internal}
    -   [14.4 Randomly Walking
        Turtles](RandomlyWalkingTurtles.html){.reference .internal}
    -   [14.5 Break and Continue](BreakandContinue.html){.reference
        .internal}
    -   [14.6 👩‍💻 Infinite Loops](WPInfiniteLoops.html){.reference
        .internal}
    -   [14.7 Exercises](Exercises.html){.reference .internal}
    -   [14.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
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

::: {#break-and-continue .section}
[14.5. ]{.section-number}Break and Continue[¶](#break-and-continue "Permalink to this heading"){.headerlink}
============================================================================================================

Python provides ways for us to control the flow of iteration with a two
keywords: break and continue.

`break`{.docutils .literal .notranslate} allows the program to
immediately 'break out' of the loop, regardless of the loop's
conditional structure. This means that the program will then skip the
rest of the iteration, without rechecking the condition, and just goes
on to the next outdented code that exists after the whole while loop.

![image showing a rectangle with \"code block\" written on it on top.
Then, text that read \"while {condition}\": followed by an indented
block with \"\...\" written on it. break is then written and another
indented block is placed after the phrase break, which has \"\...
(skipped)\" written on it. Finally, an unindented block belonging to
code outside the while loop is at the bottom. It says \"code block\". An
arrow points from the word break to the unindented block at the bottom
and the phrase \"break out of the loop\" is
written.](../_images/while_and_break.png)

::: {.runestone .explainer .ac_section}
::: {#ac14_5_1 component="activecode" question_label="14.5.1"}
::: {#ac14_5_1_question .ac_question}
:::
:::
:::

We can see here how the print statement right after `break`{.docutils
.literal .notranslate} is not executed. In fact, without using break, we
have no way to stop the while loop because the condition is always set
to True!

`continue`{.docutils .literal .notranslate} is the other keyword that
can control the flow of iteration. Using `continue`{.docutils .literal
.notranslate} allows the program to immediately "continue" with the next
iteration. The program will skip the rest of the iteration, recheck the
condition, and maybe does another iteration depending on the condition
set for the while loop.

![image showing a rectangle with \"code block\" written on it on top.
Then, text that read \"while {condition}\": followed by an indented
block with \"\...\" written on it. continue is then written and another
indented block is placed after the phrase continue, which has \"\...
(skipped)\" written on it. Finally, an unindented block belonging to
code outside the while loop is at the bottom. It says \"code block\". An
arrow points from the word continue to the while conditional statement
at the top of the while loop. The phrase \"continue at the start of the
loop\" is written.](../_images/while_and_continue.png)

::: {.runestone .explainer .ac_section}
::: {#ac14_5_2 component="activecode" question_label="14.5.2"}
::: {#ac14_5_2_question .ac_question}
:::
:::
:::

Try stepping through the above code in codelens to watch the order that
the code is executed in. Notice in the first iteration how the program
doesn't move to evaluate the divisible by 3 statement or add 1 to x.
Instead, it continues to the next iteration.
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

-   [[](RandomlyWalkingTurtles.html)]{#relations-prev}
-   [[](WPInfiniteLoops.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
