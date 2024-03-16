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
        Problem](/runestone/default/reportabug?course=fopp&page=Algorithms)
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

::: {#algorithms .section}
[]{#index-0}

[1.2. ]{.section-number}Algorithms[¶](#algorithms "Permalink to this heading"){.headerlink}
===========================================================================================

If problem solving is a central part of computer science, then the
solutions that you create through the problem solving process are also
important. In computer science, we refer to these solutions as
**algorithms**. An algorithm is a step by step list of instructions that
if followed exactly will solve the problem under consideration.

For example, an algorithm to compute the area of a circle given its
radius might look like this:

::: {.admonition-algorithm-example-1-english .admonition}
Algorithm Example 1 (English)

1.  Ask for radius

2.  Compute area by squaring radius and multiplying the result by pi

3.  Display the computed area
:::

Notice that this algorithm consists of a set of numbered steps. It is
written in English, for ease of understanding. Although simple
algorithms are easily understood when written in English, more
complicated algorithms need more precise notation. For improved
precision, algorithms are often written in pseudocode. **Pseudocode** is
a notation that is more precise than English but generally not as
precise as a programming language. The same algorithm expressed in
pseudocode might look something like this:

::: {.admonition-algorithm-example-2-pseudocode .admonition}
Algorithm Example 2 (Pseudocode)

1.  Ask for radius

2.  let area = (radius^2^) × π

3.  Display area
:::

Note how the pseudocode example expresses step 2 more precisely,
specifying the formula in mathematical terms.

Our goal in computer science is to take a problem and develop an
algorithm that can serve as a general solution. Once we have such a
solution, we can use our computer to automate its execution using
programming. Programming is a skill that allows a computer scientist to
take an algorithm and represent it in a notation (a program) that can be
followed by a computer. A program is written in a **programming
language** such as Python, the language you will learn in this book.

To help you understand the difference between an algorithm and a
program, consider this program to compute the area of a circle:

::: {.runestone .explainer .ac_section}
::: {#alg_impl component="activecode" question_label="1.2.1"}
::: {#alg_impl_question .ac_question}
:::
:::
:::

A **program** is an algorithm expressed in a programming language. We
might also say that a program is an *implementation* of an algorithm. In
this example, both the algorithm and the program have three steps. The
first step gets some input from the user and the input into something
the computer can do math with; the second step performs a calculation
using the information obtained in the first step; and the final step
displays the result to the user. Even though we haven't covered any
details of Python, hopefully you can see the correspondence between the
steps of the algorithm, which could be followed by a human (but not
executed by a computer), and the steps of the program, which can be
executed by a computer (try executing this one using the Run button).

Algorithms are important because the process of solving a problem
through programming often begins by designing an algorithm. The
programmer often expresses the algorithm in pseudocode, then converts
the algorithm to a program for the computer to execute. In the next
section, you will learn how to execute Python programs on a computer.

**Check your understanding**

::: {.runestone}
-   [A solution to a problem that can be solved by a
    computer.]{#question1_2_2_opt_a}
-   While it is true that algorithms often do solve problems, this is
    not the best answer. An algorithm is more than just the solution to
    the problem for a computer. An algorithm can be used to solve all
    sorts of problems, including those that have nothing to do with
    computers.
-   [A step by step sequence of instructions that if followed exactly
    will solve the problem under consideration.]{#question1_2_2_opt_b}
-   Algorithms are like recipes: they must be followed exactly, they
    must be clear and unambiguous, and they must end.
-   [A series of instructions implemented in a programming
    language.]{#question1_2_2_opt_c}
-   Programming languages are used to express algorithms, but an
    algorithm does not have to be expressed in terms of a programming
    language.
-   [A special kind of notation used by
    programmers.]{#question1_2_2_opt_d}
-   Programmers sometimes use a special notation to illustrate or
    document an algorithm, but this is not the definition of an
    algorithm.
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

-   [[](intro-TheWayoftheProgram.html)]{#relations-prev}
-   [[](ThePythonProgrammingLanguage.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
