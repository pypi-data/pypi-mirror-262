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
        Problem](/runestone/default/reportabug?course=fopp&page=Listsandforloops)
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
::: {#lists-and-for-loops .section}
[7.5. ]{.section-number}Lists and `for`{.docutils .literal .notranslate} loops[¶](#lists-and-for-loops "Permalink to this heading"){.headerlink}
================================================================================================================================================

It is also possible to perform **list traversal** using iteration by
item. A list is a sequence of items, so the `for`{.docutils .literal
.notranslate} loop iterates over each item in the list automatically.

::: {.runestone .explainer .ac_section}
::: {#ac6_5_1 component="activecode" question_label="7.5.1"}
::: {#ac6_5_1_question .ac_question}
:::
:::
:::

It almost reads like natural language: For (every) fruit in (the list
of) fruits, print (the name of the) fruit.

::: {#using-the-range-function-to-generate-a-sequence-to-iterate-over .section}
[7.5.1. ]{.section-number}Using the range Function to Generate a Sequence to Iterate Over[¶](#using-the-range-function-to-generate-a-sequence-to-iterate-over "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

We are now in a position to understand the inner workings we glossed
over previously when we first introduced repeated execution with a for
loop. Here was the example:

::: {.runestone .explainer .ac_section}
::: {#ac_6_5_1a component="activecode" question_label="7.5.1.1"}
::: {#ac_6_5_1a_question .ac_question}
:::
:::
:::

The `range`{.docutils .literal .notranslate} function takes an integer n
as input and returns a sequence of numbers, starting at 0 and going up
to but not including n. Thus, instead of `range(3)`{.docutils .literal
.notranslate}, we could have written `[0, 1, 2]`{.docutils .literal
.notranslate}.

The loop variable `_`{.docutils .literal .notranslate} is bound to 0 the
first time lines 4 and 5 execute. The next time, `_`{.docutils .literal
.notranslate} is bound to 1. Third time, it is bound to 2. `_`{.docutils
.literal .notranslate} is a strange name for a variable but if you look
carefully at the rules about variable names, it is a legal name. By
convention, we use the `_`{.docutils .literal .notranslate} as our loop
variable when we don't intend to ever refer to the loop variable. That
is, we are just trying to repeat the code block some number of times
(once for each item in a sequence), but we are not going to do anything
with the particular items. `_`{.docutils .literal .notranslate} will be
bound to a different item each time, but we won't ever refer to those
particular items in the code.

By contrast, notice that in the previous activecode window, the loop
variable is `afruit`{.docutils .literal .notranslate}. In that for loop,
we *do* refer to each item, with `print(afruit)`{.docutils .literal
.notranslate}.
:::

::: {#iteration-simplifies-our-turtle-program .section}
[7.5.2. ]{.section-number}Iteration Simplifies our Turtle Program[¶](#iteration-simplifies-our-turtle-program "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------------------------------------------------------------

Remember the turtle drawings we made earlier? Let's look again at how we
can use for loops there!

To draw a square we'd like to do the same thing four times --- move the
turtle forward some distance and turn 90 degrees. We previously used 8
lines of Python code to have alex draw the four sides of a square. This
next program does exactly the same thing but, with the help of the for
statement, uses just three lines (not including the setup code).
Remember that the for statement will repeat the `forward`{.docutils
.literal .notranslate} and `left`{.docutils .literal .notranslate} four
times, one time for each value in the list.

::: {.runestone .explainer .ac_section}
::: {#ac6_5_2 component="activecode" question_label="7.5.2.1"}
::: {#ac6_5_2_question .ac_question}
:::
:::
:::

While "saving some lines of code" might be convenient, it is not the big
deal here. What is much more important is that we've found a "repeating
pattern" of statements, and we reorganized our program to repeat the
pattern.

The values \[0,1,2,3\] were provided to make the loop body execute 4
times. We could have used any four values. For example, consider the
following program.

::: {.runestone .explainer .ac_section}
::: {#ac6_5_3 component="activecode" question_label="7.5.2.2"}
::: {#ac6_5_3_question .ac_question}
:::
:::
:::

In the previous example, there were four integers in the list. This time
there are four strings. Since there are four items in the list, the
iteration will still occur four times. `aColor`{.docutils .literal
.notranslate} will take on each color in the list. We can even take this
one step further and use the value of `aColor`{.docutils .literal
.notranslate} as part of the computation.

::: {.runestone .explainer .ac_section}
::: {#ac6_5_4 component="activecode" question_label="7.5.2.3"}
::: {#ac6_5_4_question .ac_question}
:::
:::
:::

In this case, the value of `aColor`{.docutils .literal .notranslate} is
used to change the color attribute of `alex`{.docutils .literal
.notranslate}. Each iteration causes `aColor`{.docutils .literal
.notranslate} to change to the next value in the list.

The for-loop is our first example of a **compound statement**.
Syntactically a compound statement is a statement. The level of
indentation of a (whole) compound statement is the indentation of its
heading. In the example above there are five statements with the same
indentation, executed sequentially: the import, 2 assignments, the
*whole* for-loop, and `wn.exitonclick()`{.docutils .literal
.notranslate}. The for-loop compound statement is executed completely
before going on to the next sequential statement,
`wn.exitonclick()`{.docutils .literal .notranslate}.

**Check your Understanding**

::: {.runestone}
-   [8]{#question6_5_1_opt_a}
-   Iteration by item will process once for each item in the sequence,
    even the empty list.
-   [9]{#question6_5_1_opt_b}
-   Yes, there are nine elements in the list so the for loop will
    iterate nine times.
-   [15]{#question6_5_1_opt_c}
-   Iteration by item will process once for each item in the sequence.
    Each string is viewed as a single item, even if you are able to
    iterate over a string itself.
-   [Error, the for statement needs to use the range
    function.]{#question6_5_1_opt_d}
-   The for statement can iterate over a sequence item by item.
:::

::: {.runestone}
-   [They are indented to the same degree from the loop
    header.]{#question6_5_2_opt_a}
-   The loop body can have any number of lines, all indented from the
    loop header.
-   [There is always exactly one line in the loop
    body.]{#question6_5_2_opt_b}
-   The loop body may have more than one line.
-   [The loop body ends with a semi-colon (;) which is not shown in the
    code above.]{#question6_5_2_opt_c}
-   Python does not need semi-colons in its syntax, but relies mainly on
    indentation.
:::

::: {.runestone}
-   [Draw a square using the same color for each
    side.]{#question6_5_3_opt_a}
-   The question is not asking you to describe the outcome of the entire
    loop, the question is asking you about the outcome of a \*\*single
    iteration\*\* of the loop.
-   [Draw a square using a different color for each
    side.]{#question6_5_3_opt_b}
-   Notice that aColor is never actually used inside the loop.
-   [Draw one side of a square.]{#question6_5_3_opt_c}
-   The body of the loop only draws one side of the square. It will be
    repeated once for each item in the list. However, the color of the
    turtle never changes.
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

-   [[](Stringsandforloops.html)]{#relations-prev}
-   [[](TheAccumulatorPattern.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
