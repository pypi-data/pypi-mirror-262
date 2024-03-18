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
        Problem](/runestone/default/reportabug?course=fopp&page=ThePythonProgrammingLanguage)
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
::: {#the-python-programming-language .section}
[]{#index-0}

[1.3. ]{.section-number}The Python Programming Language[¶](#the-python-programming-language "Permalink to this heading"){.headerlink}
=====================================================================================================================================

The programming language you will be learning is Python. Python is an
example of a **high-level language**; other high-level languages you
might have heard of are C++, PHP, and Java.

As you might infer from the name high-level language, there are also
**low-level languages**, sometimes referred to as machine languages or
assembly languages. Loosely speaking, computers can only execute
programs written in low-level languages. Thus, programs written in a
high-level language have to be processed before they can run. This extra
processing takes some time, which is a small disadvantage of high-level
languages. However, the advantages to high-level languages are enormous.

First, it is much easier to program in a high-level language. Programs
written in a high-level language take less time to write, they are
shorter and easier to read, and they are more likely to be correct.
Second, high-level languages are **portable**, meaning that they can run
on different kinds of computers with few or no modifications. Low-level
programs can run on only one kind of computer and have to be rewritten
to run on another.

Due to these advantages, almost all programs are written in high-level
languages. Low-level languages are used only for a few specialized
applications.

Two kinds of programs process high-level languages into low-level
languages: **interpreters** and **compilers**. An interpreter reads a
high-level program and executes it, meaning that it does what the
program says. It processes the program a little at a time, alternately
reading lines and performing computations.

![Interpret illustration](../_images/interpret.png)

A compiler reads the program and translates it completely before the
program starts running. In this case, the high-level program is called
the **source code**, and the translated program is called the **object
code** or the **executable**. Once a program is compiled, you can
execute it repeatedly without further translation.

![Compile illustration](../_images/compile.png)

Many modern languages use both processes. They are first compiled into a
lower level language, called **byte code**, and then interpreted by a
program called a **virtual machine**. Python uses both processes, but
because of the way programmers interact with it, it is usually
considered an interpreted language.

For the core material in this book, you will not need to install or run
python natively on your computer. Instead, you'll be writing simple
programs and executing them right in your browser.

At some point, you will find it useful to have a complete python
environment, rather than the limited environment available in this
online textbook. To do that, you will either install python on your
computer so that it can run natively, or use a remote server that
provides either a command line shell or a jupyter notebook environment.

**Check your understanding**

::: {.runestone}
-   [the instructions in a program, written in a high-level
    language.]{#question1_3_1_opt_a}
-   If the instructions are strored in a file, it is called the source
    code file.
-   [the language that you are programming in (e.g.,
    Python).]{#question1_3_1_opt_b}
-   This language is simply called the programming language, or simply
    the language. Programs are writte in this language.
-   [the environment/tool in which you are
    programming.]{#question1_3_1_opt_c}
-   The environment may be called the IDE, or integrated development
    environment, though not always.
-   [the number (or "code") that you must input at the top of each
    program to tell the computer how to execute your
    program.]{#question1_3_1_opt_d}
-   There is no such number that you must type in at the start of your
    program.
:::

::: {.runestone}
-   [It is high-level if you are standing and low-level if you are
    sitting.]{#question1_3_2_opt_a}
-   In this case high and low have nothing to do with altitude.
-   [It is high-level if you are programming for a computer and
    low-level if you are programming for a phone or mobile
    device.]{#question1_3_2_opt_b}
-   High and low have nothing to do with the type of device you are
    programming for. Instead, look at what it takes to run the program
    written in the language.
-   [It is high-level if the program must be processed before it can
    run, and low-level if the computer can execute it without additional
    processing.]{#question1_3_2_opt_c}
-   Python is a high level language but must be interpreted into machine
    code (binary) before it can be executed.
-   [It is high-level if it easy to program in and is very short; it is
    low-level if it is really hard to program in and the programs are
    really long.]{#question1_3_2_opt_d}
-   While it is true that it is generally easier to program in a
    high-level language and programs written in a high-level language
    are usually shorter, this is not always the case.
:::

::: {.runestone}
-   [1 = a process, 2 = a function]{#question1_3_3_opt_a}
-   Compiling is a software process, and running the interpreter is
    invoking a function, but how is a process different than a function?
-   [1 = translating an entire book, 2 = translating a line at a
    time]{#question1_3_3_opt_b}
-   Compilers take the entire source code and produce object code or the
    executable and interpreters execute the code line by line.
-   [1 = software, 2 = hardware]{#question1_3_3_opt_c}
-   Both compilers and interpreters are software.
-   [1 = object code, 2 = byte code]{#question1_3_3_opt_d}
-   Compilers can produce object code or byte code depending on the
    language. An interpreter produces neither.
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

-   [[](Algorithms.html)]{#relations-prev}
-   [[](SpecialWaystoExecutePythoninthisBook.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
