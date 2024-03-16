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
        Problem](/runestone/default/reportabug?course=fopp&page=WritingTextFiles)
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
::: {#writing-text-files .section}
[10.8. ]{.section-number}Writing Text Files[¶](#writing-text-files "Permalink to this heading"){.headerlink}
============================================================================================================

One of the most commonly performed data processing tasks is to read data
from a file, manipulate it in some way, and then write the resulting
data out to a new data file to be used for other purposes later. To
accomplish this, the `open`{.docutils .literal .notranslate} function
discussed above can also be used to create a new file prepared for
writing. Note in [[Table 1]{.std
.std-ref}](intro-WorkingwithDataFiles.html#filemethods1a){.reference
.internal} that the only difference between opening a file for writing
and opening a file for reading is the use of the `'w'`{.docutils
.literal .notranslate} flag instead of the `'r'`{.docutils .literal
.notranslate} flag as the second parameter. When we open a file for
writing, a new, empty file with that name is created and made ready to
accept our data. If an existing file has the same name, its contents are
overwritten. As before, the function returns a reference to the new file
object.

[[Table 2]{.std
.std-ref}](AlternativeFileReadingMethods.html#filemethods2a){.reference
.internal} shows one additional method on file objects that we have not
used thus far. The `write`{.docutils .literal .notranslate} method
allows us to add data to a text file. Recall that text files contain
sequences of characters. We usually think of these character sequences
as being the lines of the file where each line ends with the newline
`\n`{.docutils .literal .notranslate} character. Be very careful to
notice that the `write`{.docutils .literal .notranslate} method takes
one parameter, a string. When invoked, the characters of the string will
be added to the end of the file. This means that it is the programmer's
job to include the newline characters as part of the string if desired.

Assume that we have been asked to provide a file consisting of all the
squared numbers from 1 to 12.

First, we will need to open the file. Afterwards, we will iterate
through the numbers 1 through 12, and square each one of them. This new
number will need to be converted to a string, and then it can be written
into the file.

The program below solves part of the problem. We first want to make sure
that we've written the correct code to calculate the square of each
number.

::: {.runestone .explainer .ac_section}
::: {#ac9_7_1 component="activecode" question_label="10.8.1"}
::: {#ac9_7_1_question .ac_question}
:::
:::
:::

When we run this program, we see the lines of output on the screen. Once
we are satisfied that it is creating the appropriate output, the next
step is to add the necessary pieces to produce an output file and write
the data lines to it. To start, we need to open a new output file by
calling the `open`{.docutils .literal .notranslate} function,
`outfile = open("squared_numbers.txt",'w')`{.docutils .literal
.notranslate}, using the `'w'`{.docutils .literal .notranslate} flag. We
can choose any file name we like. If the file does not exist, it will be
created. However, if the file does exist, it will be reinitialized as
empty and you will lose any previous contents.

Once the file has been created, we just need to call the
`write`{.docutils .literal .notranslate} method passing the string that
we wish to add to the file. In this case, the string is already being
printed so we will just change the `print`{.docutils .literal
.notranslate} into a call to the `write`{.docutils .literal
.notranslate} method. However, there is an additional step to take,
since the write method can only accept a string as input. We'll need to
convert the number to a string. Then, we just need to add one extra
character to the string. The newline character needs to be concatenated
to the end of the line. The entire line now becomes
`outfile.write(str(square)+ '\n')`{.docutils .literal .notranslate}. The
print statement automatically outputs a newline character after whatever
text it outputs, but the write method does not do that automatically. We
also need to close the file when we are done.

The complete program is shown below.

::: {.admonition .note}
Note

As with file reading, for security reasons the runestone interactive
textbook environment does not write files to the file system on your
local computer. In an activecode window, we simulate writing to a file.
The contents of the written file are shown and you can do a subsequent
read of the contents of that filename. If you try to overwrite a file
that's built in to the page, it may not let you; don't try to get too
fancy with our file system simulator!

Below, we have printed the first 10 characters to the output window.
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_7_2 component="activecode" question_label="10.8.2"}
::: {#ac9_7_2_question .ac_question}
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

-   [[](FilesRecipe.html)]{#relations-prev}
-   [[](CSVFormat.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
