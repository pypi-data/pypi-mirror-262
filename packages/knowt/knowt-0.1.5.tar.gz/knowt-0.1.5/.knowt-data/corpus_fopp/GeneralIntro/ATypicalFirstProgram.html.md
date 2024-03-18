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
        Problem](/runestone/default/reportabug?course=fopp&page=ATypicalFirstProgram)
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

::: {#a-typical-first-program .section}
[]{#index-0}

[1.7. ]{.section-number}A Typical First Program[¶](#a-typical-first-program "Permalink to this heading"){.headerlink}
=====================================================================================================================

Traditionally, the first program written in a new language is called
*Hello, World!* because all it does is display the words, Hello, World!
In Python, the source code looks like this.

::: {.highlight-python .notranslate}
::: {.highlight}
    print("Hello, World!")
:::
:::

This is an example of using the **print function**, which doesn't
actually print anything on paper. It displays a value on the screen. In
this case, the result is the phrase:

::: {.highlight-default .notranslate}
::: {.highlight}
    Hello, World!
:::
:::

Here is the example in an activecode window, where you can run it and
modify it.

::: {.runestone .explainer .ac_section}
::: {#ac1_7_1 component="activecode" question_label="1.7.1"}
::: {#ac1_7_1_question .ac_question}
:::
:::
:::

The quotation marks in the program mark the beginning and end of the
value. They don't appear in the result. You'll learn more about why in
the next chapter.

Some people judge the quality of a programming language by the
simplicity of the Hello, World! program. By this standard, Python does
about as well as possible.

**Check your understanding**

::: {.runestone}
-   [sends information to the printer to be printed on
    paper.]{#question1_7_1_opt_a}
-   Within the Python programming language, the print statement has
    nothing to do with the printer.
-   [displays a value on the screen.]{#question1_7_1_opt_b}
-   Yes, the print statement is used to display the value of the thing
    being printed.
-   [tells the computer to put the information in print, rather than
    cursive, format.]{#question1_7_1_opt_c}
-   The format of the information is called its font and has nothing to
    do with the print statement.
-   [tells the computer to speak the information.]{#question1_7_1_opt_d}
-   That would be nice! But no\...
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

-   [[](FormalandNaturalLanguages.html)]{#relations-prev}
-   [[](WPPredictBeforeYouRun.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
