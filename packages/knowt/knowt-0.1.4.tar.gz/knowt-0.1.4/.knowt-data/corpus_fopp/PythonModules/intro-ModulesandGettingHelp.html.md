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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-ModulesandGettingHelp)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [4.1 Introduction to Python
        Modules](intro-PythonModules.html){.reference .internal}
    -   [4.2 Modules](intro-ModulesandGettingHelp.html){.reference
        .internal}
    -   [4.3 The random module](Therandommodule.html){.reference
        .internal}
    -   [4.4 Glossary](Glossary.html){.reference .internal}
    -   [4.5 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#modules .section}
[]{#index-0}

[4.2. ]{.section-number}Modules[¶](#modules "Permalink to this heading"){.headerlink}
=====================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#vid_modules .align-left .youtube-video component="youtube" video-height="315" question_label="4.2.1" video-width="560" video-videoid="GCLHuPBtLdQ" video-divid="vid_modules" video-start="0" video-end="-1"}
:::
:::

A **module** is a file containing Python definitions and statements
intended for use in other Python programs. There are many Python modules
that come with Python as part of the **standard library**. Providing
additional functionality through modules allows you to only use the
functionality you need when you need it, and it keeps your code cleaner.

Functions imported as part of a module live in their own **namespace**.
A namespace is simply a space within which all names are distinct from
each other. The same name can be reused in different namespaces but two
objects can't have the same name within a single namespace. One example
of a namespace is the set of street names within a single city. Many
cities have a street called "Main Street", but it's very confusing if
two streets in the same city have that name! Another example is the
folder organization of file systems. You can have a file called todo in
your work folder as well as your personal folder, but you know which is
which because of the folder it's in; each folder has its own namespace
for files. Note that human names are not part of a namespace that
enforces uniqueness; that's why governments have invented unique
identifiers to assign to people, like passport numbers.

The [Python Documentation](https://docs.python.org/3.6/){.reference
.external} site for Python version 3.6 is an extremely useful reference
for all aspects of Python. The site contains a listing of all the
standard modules that are available with Python (see [Global Module
Index](https://docs.python.org/3.6/py-modindex.html){.reference
.external}). You will also see that there is a [Standard Library
Reference](https://docs.python.org/3.6/library/index.html){.reference
.external} and a
[Tutorial](https://docs.python.org/3.6/tutorial/index.html){.reference
.external} as well as installation instructions, how-tos, and frequently
asked questions. We encourage you to become familiar with this site and
to use it often.

If you have not done so already, take a look at the Global Module Index.
Here you will see an alphabetical listing of all the modules that are
available as part of the standard library. Find the turtle module.

::: {#importing-modules .section}
[4.2.1. ]{.section-number}Importing Modules[¶](#importing-modules "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------------

In order to use Python modules, you have to **import** them into a
Python program. That happens with an import statement: the word
`import`{.docutils .literal .notranslate}, and then the *name* of the
module. The name is case-sensitive. Roughly translated to English, an
import statement says "there's some code in another file; please make
its functions and variables available in this file." More technically,
an import statement causes all the code in another file to be executed.
Any variables that are bound during that execution (including functions
that are defined) may then be referred in some way (to be discussed) in
the current file.

By convention, all `import`{.docutils .literal .notranslate} commands
are put at the very top of your file. They can be put elsewhere, but
that can lead to some confusions, so it's best to follow the convention.

Where do these other files that you can import come from? It could be a
code file that you wrote yourself, or it could be code that someone else
wrote and you copied on to your computer.

For example, if you have a file `myprog.py`{.docutils .literal
.notranslate} in directory `~/Desktop/mycode/`{.docutils .literal
.notranslate}, and myprog.py contains a line of code
`import morecode`{.docutils .literal .notranslate}, then the python
interpreter will look for a file called `morecode.py`{.docutils .literal
.notranslate}, excecute its code, and make its object bindings available
for reference in the rest of the code in myprog.py.

Note that it is `import morecode`{.docutils .literal .notranslate}, not
`import morecode.py`{.docutils .literal .notranslate}, but the other
file has to be called `morecode.py`{.docutils .literal .notranslate}.

The tests you see in your problem sets are also using a Python module
that's in the standard library, called `unittest`{.docutils .literal
.notranslate}. Right now, you can't see the code that causes those tests
to run, because we have hidden it from you, but later in the course, you
will learn how to write your own Unit Tests for code, and to do so, you
will need to write an import statement at the beginning of your
programs. Even before you learn how to write your own tests, you will
see code for Unit Tests in your problem set files.

::: {.admonition-don-t-overwrite-standard-library-modules .admonition}
Don't overwrite standard library modules!

Given the order of search for external Python modules that is described
in the list above, it is possible to overwrite a standard library. For
example, if you create a file `random.py`{.docutils .literal
.notranslate} in the same directory where `myprog.py`{.docutils .literal
.notranslate} lives, and then myprog.py invokes
`import random`{.docutils .literal .notranslate}, it will import *your*
file rather than the standard library module. That's not usually what
you want, so be careful about how you name your python files!
:::
:::

::: {#syntax-for-importing-modules-and-functionality .section}
[4.2.2. ]{.section-number}Syntax for Importing Modules and Functionality[¶](#syntax-for-importing-modules-and-functionality "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

When you see imported modules in a Python program, there are a few
variations that have slightly different consequences.

1.  The most common is `import morecode`{.docutils .literal
    .notranslate}. That imports everything in morecode.py. To invoke a
    function f1 that is defined in morecode.py, you would write
    `morecode.f1()`{.docutils .literal .notranslate}. Note that you have
    to explicitly mention morecode again, to specify that you want the
    f1 function from the morecode namespace. If you just write
    `f1()`{.docutils .literal .notranslate}, python will look for an f1
    that was defined in the current file, rather than in morecode.py.

2.  You can also give the imported module an alias (a different name,
    just for when you use it in your program). For example, after
    executing `import morecode as mc`{.docutils .literal .notranslate},
    you would invoke `f1`{.docutils .literal .notranslate} as
    `mc.f1()`{.docutils .literal .notranslate}. You have now given the
    `morecode`{.docutils .literal .notranslate} module the alias
    `mc`{.docutils .literal .notranslate}. Programmers often do this to
    make code easier to type.

3.  A third possibility for importing occurs when you only want to
    import SOME of the functionality from a module, and you want to make
    those objects be part of the current module's namespace. For
    example, you could write `from morecode import f1`{.docutils
    .literal .notranslate}. Then you could invoke f1 without referencing
    morecode again: `f1()`{.docutils .literal .notranslate}.

::: {.admonition-note-python-modules-and-limitations-with-activecode .admonition}
Note: Python modules and limitations with activecode

Throughout the chapters of this book, activecode windows allow you to
practice the Python that you are learning. We mentioned in the first
chapter that programming is normally done using some type of development
environment and that the activecode used here was strictly to help us
learn. It is not the way we write production programs.

To that end, it is necessary to mention that many of the modules
available in standard Python will **not** work in the activecode
environment. In fact, only `turtle`{.docutils .literal .notranslate},
`math`{.docutils .literal .notranslate}, `random`{.docutils .literal
.notranslate}, and a couple others have been ported at this point. If
you wish to explore any additional modules, you will need to run from
the native python interpreter on your computer.
:::

**Check your understanding**

::: {.runestone}
-   [A file containing Python definitions and statements intended for
    use in other Python programs.]{#question13_1_1_opt_a}
-   A module can be reused in different programs.
-   [A separate block of code within a program.]{#question13_1_1_opt_b}
-   While a module is separate block of code, it is separate from a
    program.
-   [One line of code in a program.]{#question13_1_1_opt_c}
-   The call to a feature within a module may be one line of code, but
    modules are usually multiple lines of code separate from the
    program.
-   [A file that contains documentation about functions in
    Python.]{#question13_1_1_opt_d}
-   Each module has its own documentation, but the module itself is more
    than just documentation.
:::

::: {.runestone}
-   [Go to the Python Documentation site.]{#question13_1_2_opt_a}
-   The site contains a listing of all the standard modules that are
    available with Python.
-   [Look at the import statements of the program you are working with
    or writing.]{#question13_1_2_opt_b}
-   The import statements only tell you what modules are currently being
    used in the program, not how to use them or what they contain.
-   [Ask the professor.]{#question13_1_2_opt_c}
-   While the professor knows a subset of the modules available in
    Python, chances are the professor will have to look up the available
    modules just like you would.
-   [Look in this textbook.]{#question13_1_2_opt_d}
-   This book only explains a portion of the modules available. For a
    full listing you should look elsewhere.
:::

::: {.runestone}
-   [True]{#question13_1_3_opt_a}
-   Only a few modules have been ported to work in activecode at this
    time.
-   [False]{#question13_1_3_opt_b}
-   Only a few modules have been ported to work in activecode at this
    time.
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

-   [[](intro-PythonModules.html)]{#relations-prev}
-   [[](Therandommodule.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
