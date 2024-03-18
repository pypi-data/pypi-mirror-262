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
        Problem](/runestone/default/reportabug?course=fopp&page=FindingaFileonyourDisk)
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

::: {#finding-a-file-in-your-filesystem .section}
[10.5. ]{.section-number}Finding a File in your Filesystem[¶](#finding-a-file-in-your-filesystem "Permalink to this heading"){.headerlink}
==========================================================================================================================================

In the examples we have provided, and in the simulated file system that
we've built for this online textbook, all files sit in a single
directory, and it's the same directory where the Python program is
stored. Thus, we can just write `open('myfile.txt', 'r')`{.docutils
.literal .notranslate}.

If you have installed Python on your local computer and you are trying
to get file reading and writing operations to work, there's a little
more that you may need to understand. Computer operating systems (like
Windows and the Mac OS) organize files into a hierarchy of folders, with
some folders containing other folders.

![](../_images/ExampleFileHierarchy.png){.align-center}

If your file and your Python program are in the same directory you can
simply use the filename. For example, with the file hierarchy in the
diagram, the file myPythonProgram.py could contain the code
`open('data1.txt', 'r')`{.docutils .literal .notranslate}.

If your file and your Python program are in different directories,
however, then you need to specify a **path**. You can think of the
filename as the short name for a file, and the path as the full name.
Typically, you will specify a *relative file path*, which says where to
find the file to open, relative to the directory where the code is
running from. For example, the file myPythonProgram.py could contain the
code `open('../myData/data2.txt', 'r')`{.docutils .literal
.notranslate}. The `../`{.docutils .literal .notranslate} means to go up
one level in the directory structure, to the containing folder
(allProjects); `myData/`{.docutils .literal .notranslate} says to
descend into the myData subfolder.

There is also an option to use an *absolute file path*. For example,
suppose the file structure in the figure is stored on a computer in the
user's home directory, /Users/joebob01/myFiles. Then code in any Python
program running from any file folder could open data2.txt via
`open('/Users/joebob01/myFiles/allProjects/myData/data2.txt', 'r')`{.docutils
.literal .notranslate}. You can tell an absolute file path because it
begins with a /. If you will ever move your programs and data to another
computer (e.g., to share them with someone else), it will be much more
convenient if your use relative file paths rather than absolute. That
way, if you preserve the folder structure when moving everything, you
won't need to change your code. If you use absolute paths, then the
person you are sharing with probably not have the same home directory
name, /Users/joebob01/. Note that Python pathnames follow the UNIX
conventions (Mac OS is a UNIX variant), rather than the Windows file
pathnames that use : and \\. The Python interpreter will translate to
Windows pathnames when running on a Windows machine; you should be able
to share your Python program between a Windows machine and a MAC without
having to rewrite the file open commands.

::: {.admonition .note}
Note

For security reasons, our code running in your browser doesn't read or
write files to your computer's file system. Later, when you run Python
natively on your own computer, you will be able to truly read files,
using path names as suggested above. To get you started, we have faked
it by providing a few files that you can read *as if* they were on your
hard disk. In this chapter, we simulate the existence of one textfile;
you can't open any other files from your local computer from textbook
code running in your browser.
:::

**Check Your Understanding**

::: {.runestone}
-   [open(\"YearlyProjections.csv\", \"r\")]{#question9_2_1_opt_a}
-   This would try to open a file inside of Project (but that is not
    where the file is.)
-   [open(\"../CompanyData/YearlyProjections.csv\",
    \"r\")]{#question9_2_1_opt_b}
-   This would go to the parent directory of Project and look for a
    subdirectory of that called CompanyData. But CompanyData is inside
    Project so it wouldn\'t be found.
-   [open(\"CompanyData/YearlyProjections.csv\",
    \"r\")]{#question9_2_1_opt_c}
-   Yes, this is how you can access the file!
-   [open(\"Project/CompanyData/YearlyProjections.csv\",
    \"r\")]{#question9_2_1_opt_d}
-   This would try to find a subdirectory Project of the current
    directory called Project.
-   [open(\"../YearlyProjections.csv\", \"r\")]{#question9_2_1_opt_e}
-   Remember that \'..\' will bring you up one level to the parent
    directory. This would try to open a csv file in the parent directory
    of Project (but that is not where the file is.)
:::

::: {.runestone}
-   [\"Stacy/Applications/README.txt\"]{#question9_2_2_opt_a}
-   Yes, this is a relative file path. You can tell by the lack of \"/\"
    at the beginning of the path.
-   [\"/Users/Raquel/Documents/graduation\_plans.doc\"]{#question9_2_2_opt_b}
-   This is an absolute file path. All absolute file paths start with
    \"/\".
-   [\"/private/tmp/swtag.txt\"]{#question9_2_2_opt_c}
-   This is an absolute file path. Not all absolute file paths contain
    \"User\"! Instead, check to see if the path starts with \"/\".
-   [\"ScienceData/ProjectFive/experiment\_data.csv\"]{#question9_2_2_opt_d}
-   Yes, this is a relative file path. You can tell by the lack of \"/\"
    at the beginning of the path.
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

-   [[](Iteratingoverlinesinafile.html)]{#relations-prev}
-   [[](With.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
