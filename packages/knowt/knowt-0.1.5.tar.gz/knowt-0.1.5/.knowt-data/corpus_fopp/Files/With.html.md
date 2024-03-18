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
        Problem](/runestone/default/reportabug?course=fopp&page=With)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [10.1 Introduction: Working with Data
        Files](intro-WorkingwithDataFiles.html){.reference .internal}
    -   [10.2 Reading a File](ReadingaFile.html){.reference .internal}
    -   [10.3 Alternative File Reading
        Methods](AlternativeFileReadingMethods.html){.reference
        .internal}
    -   [10.4 Iterating over lines in a
        file](Iteratingoverlinesinafile.html){.reference .internal}
    -   [10.5 Finding a File in your
        Filesystem](FindingaFileonyourDisk.html){.reference .internal}
    -   [10.6 Using with for Files](With.html){.reference .internal}
    -   [10.7 Recipe for Reading and Processing a
        File](FilesRecipe.html){.reference .internal}
    -   [10.8 Writing Text Files](WritingTextFiles.html){.reference
        .internal}
    -   [10.9 CSV Format](CSVFormat.html){.reference .internal}
    -   [10.10 Reading in data from a CSV
        File](ReadingCSVFiles.html){.reference .internal}
    -   [10.11 Writing data to a CSV
        File](WritingCSVFiles.html){.reference .internal}
    -   [10.12 👩‍💻 Tips on Handling
        Files](WPTipsHandlingFiles.html){.reference .internal}
    -   [10.13 Glossary](Glossary.html){.reference .internal}
    -   [10.14 Exercises](Exercises.html){.reference .internal}
    -   [10.15 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#using-with-for-files .section}
[]{#with-page}

[10.6. ]{.section-number}Using `with`{.docutils .literal .notranslate} for Files[¶](#using-with-for-files "Permalink to this heading"){.headerlink}
===================================================================================================================================================

::: {.admonition .note}
Note

This section is a bit of an advanced topic and can be easily skipped.
But with statements are becoming very common and it doesn't hurt to know
about them in case you run into one in the wild.
:::

Now that you have seen and practiced a bit with opening and closing
files, there is another mechanism that Python provides for us that
cleans up the often forgotten close. Forgetting to close a file does not
necessarily cause a runtime error in the kinds of programs you typically
write in an introductory programing course. However if you are writing a
program that may run for days or weeks at a time that does a lot of file
reading and writing you may run into trouble.

Python has the notion of a context manager that automates the process of
doing common operations at the start of some task, as well as automating
certain operations at the end of some task. For reading and writing a
file, the normal operation is to open the file and assign it to a
variable. At the end of working with a file the common operation is to
make sure that file is closed.

The Python with statement makes using context managers easy. The general
form of a with statement is:

::: {.highlight-default .notranslate}
::: {.highlight}
    with <create some object that understands context> as <some name>:
        do some stuff with the object
        ...
:::
:::

When the program exits the with block, the context manager handles the
common stuff that normally happens at the end, in our case closing a
file. A simple example will clear up all of this abstract discussion of
contexts. Here are the contents of a file called "mydata.txt".

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `mydata.txt`
:::

``` {#mydata.txt component="datafile" edit="false" data-rows="20" data-cols="5"}
1 2 3
4 5 6
```
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_12_1 component="activecode" question_label="10.6.2"}
::: {#ac9_12_1_question .ac_question}
:::
:::
:::

The first line of the with statement opens the file and assigns it to
the variable `md`{.docutils .literal .notranslate}. Then we can iterate
over the file in any of the usual ways. When we are done we simply stop
indenting and let Python take care of closing the file and cleaning up.

This is equivalent to code that specifically closes the file at the end,
but neatly marks the set of code that can make use of the open file as
an indented block, and ensures that the programmer won't forget to
include the `.close()`{.docutils .literal .notranslate} invocation.

::: {.runestone .explainer .ac_section}
::: {#ac9_12_2 component="activecode" question_label="10.6.3"}
::: {#ac9_12_2_question .ac_question}
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

-   [[](FindingaFileonyourDisk.html)]{#relations-prev}
-   [[](FilesRecipe.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
