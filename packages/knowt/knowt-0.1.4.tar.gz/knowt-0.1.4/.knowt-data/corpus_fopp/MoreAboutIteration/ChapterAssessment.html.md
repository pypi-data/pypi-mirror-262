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
::: {#chapter-assessment .section}
[14.8. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac14_10_1 component="activecode" question_label="14.8.1"}
::: {#ac14_10_1_question .ac_question}
Write a function, `sublist`{.docutils .literal .notranslate}, that takes
in a list of numbers as the parameter. In the function, use a while loop
to return a sublist of the input list. The sublist should contain the
same values of the original list up until it reaches the number 5 (it
should not contain the number 5).
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_10_2 component="activecode" question_label="14.8.2"}
::: {#ac14_10_2_question .ac_question}
Write a function called `check_nums`{.docutils .literal .notranslate}
that takes a list as its parameter, and contains a while loop that only
stops once the element of the list is the number 7. What is returned is
a list of all of the numbers up until it reaches 7.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_10_3 component="activecode" question_label="14.8.3"}
::: {#ac14_10_3_question .ac_question}
Write a function, `sublist`{.docutils .literal .notranslate}, that takes
in a list of strings as the parameter. In the function, use a while loop
to return a sublist of the input list. The sublist should contain the
same values of the original list up until it reaches the string "STOP"
(it should not contain the string "STOP").
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_10_4 component="activecode" question_label="14.8.4"}
::: {#ac14_10_4_question .ac_question}
Write a function called `stop_at_z`{.docutils .literal .notranslate}
that iterates through a list of strings. Using a while loop, append each
string to a new list until the string that appears is "z". The function
should return the new list.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_10_5 component="activecode" question_label="14.8.5"}
::: {#ac14_10_5_question .ac_question}
Below is a for loop that works. Underneath the for loop, rewrite the
problem so that it does the same thing, but using a while loop instead
of a for loop. Assign the accumulated total in the while loop code to
the variable `sum2`{.docutils .literal .notranslate}. Once complete,
sum2 should equal sum1.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_10_6 component="activecode" question_label="14.8.6"}
::: {#ac14_10_6_question .ac_question}
**Challenge:** Write a function called `beginning`{.docutils .literal
.notranslate} that takes a list as input and contains a loop that only
stops once the element of the list is the string 'bye'. What is returned
is a list that contains up to the first 10 strings, regardless of where
the loop stops. (i.e., if it stops on the 32nd element, the first 10 are
returned. If "bye" is the 5th element, the first 4 are returned.) *If
you want to make this even more of a challenge, do this without slicing*
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
-   [[](../AdvancedFunctions/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
