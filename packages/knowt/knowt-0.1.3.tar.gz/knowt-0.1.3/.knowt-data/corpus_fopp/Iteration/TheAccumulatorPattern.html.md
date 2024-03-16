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
        Problem](/runestone/default/reportabug?course=fopp&page=TheAccumulatorPattern)
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

::: {#the-accumulator-pattern .section}
[]{#accum-pattern}

[7.6. ]{.section-number}The Accumulator Pattern[¶](#the-accumulator-pattern "Permalink to this heading"){.headerlink}
=====================================================================================================================

One common programming "pattern" is to traverse a sequence,
**accumulating** a value as we go, such as the sum-so-far or the
maximum-so-far. That way, at the end of the traversal we have
accumulated a single value, such as the sum total of all the items or
the largest item.

The anatomy of the accumulation pattern includes:

:   -   **initializing** an "accumulator" variable to an initial value
        (such as 0 if accumulating a sum)

    -   **iterating** (e.g., traversing the items in a sequence)

    -   **updating** the accumulator variable on each iteration (i.e.,
        when processing each item in the sequence)

For example, consider the following code, which computes the sum of the
numbers in a list.

::: {.runestone .explainer .ac_section}
::: {#ac6_6_1 component="activecode" question_label="7.6.1"}
::: {#ac6_6_1_question .ac_question}
:::
:::
:::

In the program above, notice that the variable `accum`{.docutils
.literal .notranslate} starts out with a value of 0. Next, the iteration
is performed 10 times. Inside the for loop, the update occurs.
`w`{.docutils .literal .notranslate} has the value of current item (1
the first time, then 2, then 3, etc.). `accum`{.docutils .literal
.notranslate} is reassigned a new value which is the old value plus the
current value of `w`{.docutils .literal .notranslate}.

This pattern of iterating the updating of a variable is commonly
referred to as the **accumulator pattern**. We refer to the variable as
the **accumulator**. This pattern will come up over and over again.
Remember that the key to making it work successfully is to be sure to
initialize the variable before you start the iteration. Once inside the
iteration, it is required that you update the accumulator.

Here is the same program in codelens. Step through the function and
watch the "running total" accumulate the result.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="7.6.2"}
::: {#clens6_6_1_question .ac_question}
:::

::: {#clens6_6_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 7.6.2 (clens6\_6\_1)]{.runestone_caption_text}
:::
:::

::: {.admonition .note}
Note

What would happen if we indented the print accum statement? Not sure?
Make a prediction, then try it and find out.
:::

We can utilize the range function in this situation as well. Previously,
you've seen it used when we wanted to draw in turtle. There we used it
to iterate a certain number of times. We can do more than that though.
The `range`{.docutils .literal .notranslate} function takes at least one
input - which should be an integer - and returns a list as long as your
input. While you can provide two inputs, we will focus on using range
with just one input. With one input, range will start at zero and go up
to - but not include - the input. Here are the examples:

::: {.runestone .explainer .ac_section}
::: {#ac6_8_10 component="activecode" question_label="7.6.3"}
::: {#ac6_8_10_question .ac_question}
:::
:::
:::

Here's how you could use the range function in the previous problem.

::: {.runestone .explainer .ac_section}
::: {#ac6_6_2 component="activecode" question_label="7.6.4"}
::: {#ac6_6_2_question .ac_question}
:::
:::
:::

Because the range function is exclusive of the ending number, we have to
use 11 as the function input.

We can use the accumulation pattern to count the number of things or to
sum up a total. The above examples only covered how to get the sum for a
list, but we can also count how many items are in the list if we wanted
to.

::: {.runestone .explainer .ac_section}
::: {#ac6_6_3 component="activecode" question_label="7.6.5"}
::: {#ac6_6_3_question .ac_question}
:::
:::
:::

In this example we don't make use of `w`{.docutils .literal
.notranslate} even though the iterator variable (loop variable) is a
necessary part of constructing a for loop. Instead of adding the value
of `w`{.docutils .literal .notranslate} to `count`{.docutils .literal
.notranslate} we add a 1 to it, because we're incrementing the value of
count when we iterate each time through the loop. Though in this
scenario we could have used the `len`{.docutils .literal .notranslate}
function, there are other cases later on where len won't be useful but
we will still need to count.

**Check your understanding**

::: {.runestone}
-   [It will print out 10 instead of 55]{#question6_6_1_opt_a}
-   The variable accum will be reset to 0 each time through the loop.
    Then it will add the current item. Only the last item will count.
-   [It will cause a run-time error]{#question6_6_1_opt_b}
-   Assignment statements are perfectly legal inside loops and will not
    cause an error.
-   [It will print out 0 instead of 55]{#question6_6_1_opt_c}
-   Good thought: the variable accum will be reset to 0 each time
    through the loop. But then it adds the current item.
:::

::: {.runestone .parsons-container}
::: {#pp6_6_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Rearrange the code statements so that the program will add up the first
n odd numbers where n is provided by the user.
:::

``` {.parsonsblocks question_label="7.6.7" style="visibility: hidden;"}
        n = int(input('How many odd numbers would you like to add together?'))
thesum = 0
oddnumber = 1
---
for counter in range(n):
---
   thesum = thesum + oddnumber
   oddnumber = oddnumber + 2
---
print(thesum)
        
```
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac6_6_4 component="activecode" question_label="7.6.8"}
::: {#ac6_6_4_question .ac_question}
Write code to create a list of integers from 0 through 52 and assign
that list to the variable `numbers`{.docutils .literal .notranslate}.
You should use the Python range function and don't forget to covert the
result to a list -- do not type out the whole list yourself.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac6_6_10 component="activecode" question_label="7.6.9"}
::: {#ac6_6_10_question .ac_question}
Count the number of characters in string `str1`{.docutils .literal
.notranslate}. Do not use `len()`{.docutils .literal .notranslate}. Save
the number in variable `numbs`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac6_8_9 component="activecode" question_label="7.6.10"}
::: {#ac6_8_9_question .ac_question}
Create a list of numbers 0 through 40 and assign this list to the
variable `numbers`{.docutils .literal .notranslate}. Then, accumulate
the total of the list's values and assign that sum to the variable
`sum1`{.docutils .literal .notranslate}.
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

-   [[](Listsandforloops.html)]{#relations-prev}
-   [[](TraversalandtheforLoopByIndex.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
