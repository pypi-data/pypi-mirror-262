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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-WorkingwithDataFiles)
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
::: {#introduction-working-with-data-files .section}
[10.1. ]{.section-number}Introduction: Working with Data Files[¶](#introduction-working-with-data-files "Permalink to this heading"){.headerlink}
=================================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#filesintrovideo .align-left .youtube-video component="youtube" video-height="315" question_label="10.1.1" video-width="560" video-videoid="zASE-UA2YKg" video-divid="filesintrovideo" video-start="0" video-end="-1"}
:::
:::

So far, the data we have used in this book have all been either coded
right into the program, or have been entered by the user. In real life
data reside in files. For example the images we worked with in the image
processing unit ultimately live in files on your hard drive. Web pages,
and word processing documents, and music are other examples of data that
live in files. In this short chapter we will introduce the Python
concepts necessary to use data from files in our programs.

For our purposes, we will assume that our data files are text
files--that is, files filled with characters. The Python programs that
you write are stored as text files. We can create these files in any of
a number of ways. For example, we could use a text editor to type in and
save the data. We could also download the data from a website and then
save it in a file. Regardless of how the file is created, Python will
allow us to manipulate the contents.

In Python, we must **open** files before we can use them and **close**
them when we are done with them. As you might expect, once a file is
opened it becomes a Python object just like all other data. [[Table
1]{.std .std-ref}](#filemethods1a){.reference .internal} shows the
functions and methods that can be used to open and close files.

  **Method Name**                            **Use**                                                   **Explanation**
  ------------------------------------------ --------------------------------------------------------- ---------------------------------------------------------------------------------------------------------
  `open`{.docutils .literal .notranslate}    `open(filename,'r')`{.docutils .literal .notranslate}     Open a file called filename and use it for reading. This will return a reference to a file object.
  `open`{.docutils .literal .notranslate}    `open(filename,'w')`{.docutils .literal .notranslate}     Open a file called filename and use it for writing. This will also return a reference to a file object.
  `close`{.docutils .literal .notranslate}   `filevariable.close()`{.docutils .literal .notranslate}   File use is complete.

::: {#learning-goals .section}
[10.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------

-   To understand the structure of file systems

-   To understand opening files with different modes

-   To introduce files as another kind of sequence that one can iterate
    over

-   To introduce the read/transform/write pattern

-   To introduce parallel assignment to two or three variables
:::

::: {#objectives .section}
[10.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------

-   Demonstrate that you can read a single value from each line in a
    file

-   Convert the line to the appropriate value

-   Read a line and convert it into multiple values using split and
    assignment to multiple variables
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

-   [[](toctree.html)]{#relations-prev}
-   [[](ReadingaFile.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
