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
        Problem](/runestone/default/reportabug?course=fopp&page=SpecialWaystoExecutePythoninthisBook)
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
::: {#special-ways-to-execute-python-in-this-book .section}
[1.4. ]{.section-number}Special Ways to Execute Python in this Book[¶](#special-ways-to-execute-python-in-this-book "Permalink to this heading"){.headerlink}
=============================================================================================================================================================

This book provides two additional ways to execute Python programs. Both
techniques are designed to assist you as you learn the Python
programming language. They will help you increase your understanding of
how Python programs work.

First, you can write, modify, and execute programs using a unique
**activecode** interpreter that allows you to execute Python code right
in the text itself (right from the web browser). Although this is
certainly not the way real programs are written, it provides an
excellent environment for learning a programming language like Python
since you can experiment with the language as you are reading.

Take a look at the activecode interpreter in action. Try pressing the
*Save & Run* button below. (If you are not logged in, it will just say
*Run*.)

::: {.runestone .explainer .ac_section}
::: {#ac1_4_1 component="activecode" question_label="1.4.1"}
::: {#ac1_4_1_question .ac_question}
:::
:::
:::

Now try modifying the program shown above. First, modify the string in
the first print statement by changing the word *adds* to the word
*multiplies*. Now press *Save & Run* again. You can see that the result
of the program has changed. However, it still prints "5" as the answer.
Modify the second print statement by changing the addition symbol, the
`+`{.docutils .literal .notranslate}, to the multiplication symbol,
`*`{.docutils .literal .notranslate}. Press *Save & Run* again to see
the new results.

As the name suggests, *Save & Run* also *saves* your latest version of
the code, and you can recover it even in later sessions when *logged
in*. If *not* logged in, *Run* saves versions *only until your browser
leaves the current web page*, and then you lose all modifications.

If you are logged in, when a page first loads, each activecode window
will have a *Load History* button, to the right of the *Save & Run*
button. If you click on it, or if you run any code, that button turns
into a slider. If you click on the slider location box, you can use your
left and right arrow buttons to switch to other versions you ran.
Alternately you can drag the box on the slider. Now move the slider to
see a previously saved version of your code. You can edit or run any
version.

In addition to activecode, you can also execute Python code with the
assistance of a unique visualization tool. This tool, known as
**codelens**, allows you to control the step by step execution of a
program. It also lets you see the values of all variables as they are
created and modified. In activecode, the source code executes from
beginning to end and you can see the final result. In codelens you can
see and control the step by step progress. Note that the red arrow
always points to the next line of code that is going to be executed. The
light green arrow points to the line that was just executed. Click on
the "Show in Codelens" button to make the codelens window show up, and
then click on the Forward button a few times to step through the
execution.

Sometimes, we will present code examples explicitly in a codelens window
in the textbook, as below. When we do, think of it as an encouragement
to use the codelens features to step through the execution of the
program.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="1.4.2"}
::: {#clens1_4_1_question .ac_question}
:::

::: {#clens1_4_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 1.4.2 (clens1\_4\_1)]{.runestone_caption_text}
:::
:::

**Check your understanding**

::: {.runestone}
-   [save programs and reload saved programs.]{#question1_4_1_opt_a}
-   You can (and should) save the contents of the activecode window.
-   [type in Python source code.]{#question1_4_1_opt_b}
-   You are not limited to running the examples that are already there.
    Try adding to them and creating your own.
-   [execute Python code right in the text itself within the web
    browser.]{#question1_4_1_opt_c}
-   The activecode interpreter will allow you type Python code into the
    textbox and then you can see it execute as the interpreter
    interprets and executes the source code.
-   [receive a yes/no answer about whether your code is correct or
    not.]{#question1_4_1_opt_d}
-   Although you can (and should) verify that your code is correct by
    examining its output, activecode will not directly tell you whether
    you have correctly implemented your program.
:::

::: {.runestone}
-   [measure the speed of a program's execution.]{#question1_4_2_opt_a}
-   In fact, codelens steps through each line one by one as you click,
    which is MUCH slower than the Python interpreter.
-   [control the step by step execution of a
    program.]{#question1_4_2_opt_b}
-   By using codelens, you can control the execution of a program step
    by step. You can even go backwards!
-   [write and execute your own Python code.]{#question1_4_2_opt_c}
-   Codelens works only for the pre-programmed examples.
-   [execute the Python code that is in codelens.]{#question1_4_2_opt_d}
-   By stepping forward through the Python code in codelens, you are
    executing the Python program.
:::

[]{#index-0 .target}
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

-   [[](ThePythonProgrammingLanguage.html)]{#relations-prev}
-   [[](MoreAboutPrograms.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
