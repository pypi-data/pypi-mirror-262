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
        Problem](/runestone/default/reportabug?course=fopp&page=WPProgramDevelopment)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [18.1 Introduction: Test Cases](intro-TestCases.html){.reference
        .internal}
    -   [18.2 Checking Assumptions About Data
        Types](TestingTypes.html){.reference .internal}
    -   [18.3 Checking Other
        Assumptions](CheckingOtherAssumptions.html){.reference
        .internal}
    -   [18.4 Testing Conditionals](TestingConditionals.html){.reference
        .internal}
    -   [18.5 Testing Loops](TestingLoops.html){.reference .internal}
    -   [18.6 Writing Test Cases for
        Functions](Testingfunctions.html){.reference .internal}
    -   [18.7 Testing Optional
        Parameters](TestingOptionalParameters.html){.reference
        .internal}
    -   [18.8 👩‍💻 Test Driven
        Development](WPProgramDevelopment.html){.reference .internal}
    -   [18.9 Glossary](Glossary.html){.reference .internal}
    -   [18.10 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [18.11 Exercises](Exercises.html){.reference .internal}
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

::: {#test-driven-development .section}
[18.8. ]{.section-number}👩‍💻 Test Driven Development[¶](#test-driven-development "Permalink to this heading"){.headerlink}
==========================================================================================================================

At this point, you should be able to look at complete functions and tell
what they do. Also, if you have been doing the exercises, you have
written some small functions. As you write larger functions, you might
start to have more difficulty, especially with runtime and semantic
errors.

To deal with increasingly complex programs, we are going to suggest a
technique called **incremental development**. The goal of incremental
development is to avoid long debugging sessions by adding and testing
only a small amount of code at a time.

If you write unit tests before doing the incremental development, you will be able to track your progress as the code passes more and more of the tests. Alternatively, you can write additional tests at each stage of incremental development.

:   Then you will be able to check whether any code change you make at a
    later stage of development causes one of the earlier tests, which
    used to pass, to not pass any more.

As an example, suppose you want to find the distance between two points,
given by the coordinates (x~1~, y~1~) and (x~2~, y~2~). By the
Pythagorean theorem, the distance is:

![Distance formula](../_images/distance_formula.png)

The first step is to consider what a `distance`{.docutils .literal
.notranslate} function should look like in Python. In other words, what
are the inputs (parameters) and what is the output (return value)?

In this case, the two points are the inputs, which we can represent
using four parameters. The return value is the distance, which is a
floating-point value.

Already we can write an outline of the function that captures our
thinking so far.

::: {.highlight-python .notranslate}
::: {.highlight}
    def distance(x1, y1, x2, y2):
        return None
:::
:::

Obviously, this version of the function doesn't compute distances; it
always returns None. But it is syntactically correct, and it will run,
which means that we can test it before we make it more complicated.

The distance between any point and itself should be 0.

::: {.runestone .explainer .ac_section}
::: {#ac400_1_1 component="activecode" question_label="18.8.1"}
::: {#ac400_1_1_question .ac_question}
:::
:::
:::

We call the distance function with sample inputs: (1,2, 1,2). The first
1,2 are the coordinates of the first point and the second 1,2 are the
coordinates of the second point. What is the distance between these two
points? Zero.

It's not returning the correct answer, so we don't pass the test. Let's
fix that.

::: {.runestone .explainer .ac_section}
::: {#ac400_1_2 component="activecode" question_label="18.8.2"}
::: {#ac400_1_2_question .ac_question}
:::
:::
:::

Now we pass the test. But really, that's not a sufficient test.

::: {.admonition-extend-the-program .admonition}
Extend the program ...

On line 6, write another unit test (assert statement). Use (1,2, 4,6) as
the parameters to the distance function. How far apart are these two
points? Use that value (instead of 0) as the correct answer for this
unit test.

On line 7, write another unit test. Use (0,0, 1,1) as the parameters to
the distance function. How far apart are these two points? Use that
value as the correct answer for this unit test.

Are there any other edge cases that you think you should consider?
Perhaps points with negative numbers for x-values or y-values?
:::

**When testing a function, it is essential to know the right answer.**

For the second test the horizontal distance equals 3 and the vertical
distance equals 4; that way, the result is 5 (the hypotenuse of a 3-4-5
triangle). For the third test, we have a 1-1-sqrt(2) triangle.

::: {.runestone .explainer .ac_section}
::: {#ac400_1_3 component="activecode" question_label="18.8.3"}
::: {#ac400_1_3_question .ac_question}
:::
:::
:::

The first test passes but the others fail since the distance function
does not yet contain all the necessary steps.

At this point we have confirmed that the function is syntactically
correct, and we can start adding lines of code. After each incremental
change, we test the function again. If an error occurs at any point, we
know where it must be --- in the last line we added.

A logical first step in the computation is to find the differences x~2~-
x~1~ and y~2~- y~1~. We will store those values in temporary variables
named `dx`{.docutils .literal .notranslate} and `dy`{.docutils .literal
.notranslate}.

::: {.highlight-python .notranslate}
::: {.highlight}
    def distance(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return 0.0
:::
:::

Next we compute the sum of squares of `dx`{.docutils .literal
.notranslate} and `dy`{.docutils .literal .notranslate}.

::: {.highlight-python .notranslate}
::: {.highlight}
    def distance(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        dsquared = dx**2 + dy**2
        return 0.0
:::
:::

Again, we could run the program at this stage and check the value of
`dsquared`{.docutils .literal .notranslate} (which should be 25).

Finally, using the fractional exponent `0.5`{.docutils .literal
.notranslate} to find the square root, we compute and return the result.

::: {.runestone .explainer .ac_section}
::: {#ac400_1_4 component="activecode" question_label="18.8.4"}
::: {#ac400_1_4_question .ac_question}
:::
:::
:::

When you start out, you might add only a line or two of code at a time.
As you gain more experience, you might find yourself writing and
debugging bigger conceptual chunks. As you improve your programming
skills you should find yourself managing bigger and bigger chunks: this
is very similar to the way we learned to read letters, syllables, words,
phrases, sentences, paragraphs, etc., or the way we learn to chunk music
--- from individual notes to chords, bars, phrases, and so on.

The key aspects of the process are:

1.  Make sure you know what you are trying to accomplish. Then you can
    write appropriate unit tests.

2.  Start with a working skeleton program and make small incremental
    changes. At any point, if there is an error, you will know exactly
    where it is.

3.  Use temporary variables to hold intermediate values so that you can
    easily inspect and check them.

4.  Once the program is working, you might want to consolidate multiple
    statements into compound expressions, but only do this if it does
    not make the program more difficult to read.
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

-   [[](TestingOptionalParameters.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
