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
        Problem](/runestone/default/reportabug?course=fopp&page=ThewhileStatement)
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

::: {#the-while-statement .section}
[14.2. ]{.section-number}The `while`{.docutils .literal .notranslate} Statement[¶](#the-while-statement "Permalink to this heading"){.headerlink}
=================================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#whileloop .align-left .youtube-video component="youtube" video-height="315" question_label="14.2.1" video-width="560" video-videoid="iUbToOoAykE" video-divid="whileloop" video-start="0" video-end="-1"}
:::
:::

There is another Python statement that can also be used to build an
iteration. It is called the `while`{.docutils .literal .notranslate}
statement. The `while`{.docutils .literal .notranslate} statement
provides a much more general mechanism for iterating. Similar to the
`if`{.docutils .literal .notranslate} statement, it uses a boolean
expression to control the flow of execution. The body of while will be
repeated as long as the controlling boolean expression evaluates to
`True`{.docutils .literal .notranslate}.

The following two figures show the flow of control. The first focuses on
the flow inside the while loop and the second shows the while loop in
context.

![a diamond at the top has the phrase \"Is the condition True?\". Two
arrows come out it with either the phrase yes or no on the arrows. The
yes arrow points to a box that says \"evaluate the statemenets in the
body of the loop\". It then has an arrow that unconditionally points
back to \"Is the condition True?\" diamond. The no arrow escapes the
loop and points down past the \"evaluate\"
square.](../_images/while_flow.png) ![image showing a rectangle with
\"code block\" written on it on top. Then, text that read \"while
{condition}\": followed by an indented block with \"run if {condition}
is True\" written on it. An arrow points from the bottom of the indented
block to the top of the while loop and says \"run loop again\". At the
bottom of the image is an unindented block that says the phrase \"code
block.\"](../_images/while_loop.png)

We can use the `while`{.docutils .literal .notranslate} loop to create
any type of iteration we wish, including anything that we have
previously done with a `for`{.docutils .literal .notranslate} loop. For
example, the program in the previous section could be rewritten using
`while`{.docutils .literal .notranslate}. Instead of relying on the
`range`{.docutils .literal .notranslate} function to produce the numbers
for our summation, we will need to produce them ourselves. To do this,
we will create a variable called `aNumber`{.docutils .literal
.notranslate} and initialize it to 1, the first number in the summation.
Every iteration will add `aNumber`{.docutils .literal .notranslate} to
the running total until all the values have been used. In order to
control the iteration, we must create a boolean expression that
evaluates to `True`{.docutils .literal .notranslate} as long as we want
to keep adding values to our running total. In this case, as long as
`aNumber`{.docutils .literal .notranslate} is less than or equal to the
bound, we should keep going.

Here is a new version of the summation program that uses a while
statement.

::: {.runestone .explainer .ac_section}
::: {#ac14_2_1 component="activecode" question_label="14.2.2"}
::: {#ac14_2_1_question .ac_question}
:::
:::
:::

You can almost read the `while`{.docutils .literal .notranslate}
statement as if it were in natural language. It means, while
`aNumber`{.docutils .literal .notranslate} is less than or equal to
`aBound`{.docutils .literal .notranslate}, continue executing the body
of the loop. Within the body, each time, update `theSum`{.docutils
.literal .notranslate} using the accumulator pattern and increment
`aNumber`{.docutils .literal .notranslate}. After the body of the loop,
we go back up to the condition of the `while`{.docutils .literal
.notranslate} and reevaluate it. When `aNumber`{.docutils .literal
.notranslate} becomes greater than `aBound`{.docutils .literal
.notranslate}, the condition fails and flow of control continues to the
`return`{.docutils .literal .notranslate} statement.

The same program in codelens will allow you to observe the flow of
execution.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="14.2.3"}
::: {#clens14_2_1_question .ac_question}
:::

::: {#clens14_2_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 14.2.3 (clens14\_2\_1)]{.runestone_caption_text}
:::
:::

::: {.admonition .note}
Note

The names of the variables have been chosen to help readability.
:::

More formally, here is the flow of execution for a `while`{.docutils
.literal .notranslate} statement:

1.  Evaluate the condition, yielding `False`{.docutils .literal
    .notranslate} or `True`{.docutils .literal .notranslate}.

2.  If the condition is `False`{.docutils .literal .notranslate}, exit
    the `while`{.docutils .literal .notranslate} statement and continue
    execution at the next statement.

3.  If the condition is `True`{.docutils .literal .notranslate}, execute
    each of the statements in the body and then go back to step 1.

The body consists of all of the statements below the header with the
same indentation.

This type of flow is called a **loop** because the third step loops back
around to the top. Notice that if the condition is `False`{.docutils
.literal .notranslate} the first time through the loop, the statements
inside the loop are never executed.

The body of the loop should change the value of one or more variables so
that eventually the condition becomes `False`{.docutils .literal
.notranslate} and the loop terminates. Otherwise the loop will repeat
forever. This is called an **infinite loop**. An endless source of
amusement for computer scientists is the observation that the directions
written on the back of the shampoo bottle (lather, rinse, repeat) create
an infinite loop.

In the case shown above, we can prove that the loop terminates because
we know that the value of `aBound`{.docutils .literal .notranslate} is
finite, and we can see that the value of `aNumber`{.docutils .literal
.notranslate} increments each time through the loop, so eventually it
will have to exceed `aBound`{.docutils .literal .notranslate}. In other
cases, it is not so easy to tell.

::: {.admonition .note}
Note

Introduction of the while statement causes us to think about the types
of iteration we have seen. The `for`{.docutils .literal .notranslate}
statement will always iterate through a sequence of values like the list
of names for the party or the list of numbers created by
`range`{.docutils .literal .notranslate}. Since we know that it will
iterate once for each value in the collection, it is often said that a
`for`{.docutils .literal .notranslate} loop creates a **definite
iteration** because we definitely know how many times we are going to
iterate. On the other hand, the `while`{.docutils .literal .notranslate}
statement is dependent on a condition that needs to evaluate to
`False`{.docutils .literal .notranslate} in order for the loop to
terminate. Since we do not necessarily know when this will happen, it
creates what we call **indefinite iteration**. Indefinite iteration
simply means that we don't know how many times we will repeat but
eventually the condition controlling the iteration will fail and the
iteration will stop. (Unless we have an infinite loop which is of course
a problem)
:::

What you will notice here is that the `while`{.docutils .literal
.notranslate} loop is more work for you --- the programmer --- than the
equivalent `for`{.docutils .literal .notranslate} loop. When using a
`while`{.docutils .literal .notranslate} loop you have to control the
loop variable yourself. You give it an initial value, test for
completion, and then make sure you change something in the body so that
the loop terminates. That also makes a while loop harder to read and
understand than the equivalent for loop. So, while you *can* implement
definite iteration with a while loop, it's not a good idea to do that.
Use a for loop whenever it will be known at the beginning of the
iteration process how many times the block of code needs to be executed.

**Check your understanding**

::: {.runestone}
-   [True]{#question14_2_1_opt_a}
-   Although the while loop uses a different syntax, it is just as
    powerful as a for-loop and often more flexible.
-   [False]{#question14_2_1_opt_b}
-   Often a for-loop is more natural and convenient for a task, but that
    same task can always be expressed using a while loop.
:::

::: {.runestone}
-   [n starts at 10 and is incremented by 1 each time through the loop,
    so it will always be positive]{#question14_2_2_opt_a}
-   The loop will run as long as n is positive. In this case, we can see
    that n will never become non-positive.
-   [answer starts at 1 and is incremented by n each time, so it will
    always be positive]{#question14_2_2_opt_b}
-   While it is true that answer will always be positive, answer is not
    considered in the loop condition.
-   [You cannot compare n to 0 in while loop. You must compare it to
    another variable.]{#question14_2_2_opt_c}
-   It is perfectly valid to compare n to 0. Though indirectly, this is
    what causes the infinite loop.
-   [In the while loop body, we must set n to False, and this code does
    not do that.]{#question14_2_2_opt_d}
-   The loop condition must become False for the loop to terminate, but
    n by itself is not the condition in this case.
:::

::: {.runestone}
-   [a for-loop or a while-loop]{#question14_2_3_opt_a}
-   Although you do not know how many iterations you loop will run
    before the program starts running, once you have chosen your random
    integer, Python knows exactly how many iterations the loop will run,
    so either a for-loop or a while-loop will work.
-   [only a for-loop]{#question14_2_3_opt_b}
-   As you learned in section 7.2, a while-loop can always be used for
    anything a for-loop can be used for.
-   [only a while-loop]{#question14_2_3_opt_c}
-   Although you do not know how many iterations you loop will run
    before the program starts running, once you have chosen your random
    integer, Python knows exactly how many iterations the loop will run,
    so this is an example of definite iteration.
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_2_2 component="activecode" question_label="14.2.7"}
::: {#ac14_2_2_question .ac_question}
Write a while loop that is initialized at 0 and stops at 15. If the
counter is an even number, append the counter to a list called
`eve_nums`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac14_2_3 component="activecode" question_label="14.2.8"}
::: {#ac14_2_3_question .ac_question}
Below, we've provided a for loop that sums all the elements of
`list1`{.docutils .literal .notranslate}. Write code that accomplishes
the same task, but instead uses a while loop. Assign the accumulator
variable to the name `accum`{.docutils .literal .notranslate}.
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

-   [[](intro-indefiniteiteration.html)]{#relations-prev}
-   [[](listenerLoop.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
