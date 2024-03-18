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
        Problem](/runestone/default/reportabug?course=fopp&page=WPInfiniteLoops)
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
::: {#infinite-loops .section}
[14.6. ]{.section-number}👩‍💻 Infinite Loops[¶](#infinite-loops "Permalink to this heading"){.headerlink}
========================================================================================================

Although the textbook has a time limit which prevents an active code
window from running indefinitely, you'll still have to wait a little
while if your program has an ininite loop. If you accidentally make one
outside of the textbook, you won't have that same protection.

So how can you recognize when you are in danger of making an infinite
loop?

First off, if the variable that you are using to determine if the while
loop should continue is never reset inside the while loop, then your
code will have an infinite loop. (Unless of course you use
`break`{.docutils .literal .notranslate} to break out of the loop.)

Additionally, if the while condition is `while True:`{.docutils .literal
.notranslate} and there is no break, then that is another case of an
infinite loop!

::: {.highlight-python .notranslate}
::: {.highlight}
    while True:
        print("Will this stop?")

    print("We have escaped.")
:::
:::

Another case where an infinite loop is likely to occur is when you have
reassigned the value of the variable used in the while statement in a
way that prevents the loop from completing. This is an example below.
We're showing it in codelens, which stops the execution after a certain
number of steps.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="14.6.1"}
::: {#ac14_11_1_question .ac_question}
:::

::: {#ac14_11_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 14.6.1 (ac14\_11\_1)]{.runestone_caption_text}
:::
:::

Notice how in this case, b is initally set to 15 outside of the while
loop, and then reassigned the value of 5 inside, on line 4. By the time
7 has been added to b on line 6, we then have to check if b is less than
60. Because it isn't we again run line 4, and set the value of b to 5
again. There is no way to break out of this loop.

Sometimes programs can take a while to run, so how can you determine if
your code is just talking a while or if it is stuck inside an infinite
loop? Print statements are for people, so take advantage of them! You
can add print statements to keep track of how your variables are
changing as the program processes the instructions given to them. Below
is an example of an infinite loop. Try adding print statements to see
where it's coming from. When you're done, check out the answer to see
what our solution was.

1.  ::: {#q1 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac14_11_2 component="activecode" question_label="14.6.2"}
    ::: {#ac14_11_2_question .ac_question}
    :::
    :::
    :::
    :::

    ::: {component="tab" tabname="Answer"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac14_11_3 component="activecode" question_label="14.6.3"}
    ::: {#ac14_11_3_question .ac_question}
    :::
    :::
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

-   [[](BreakandContinue.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
