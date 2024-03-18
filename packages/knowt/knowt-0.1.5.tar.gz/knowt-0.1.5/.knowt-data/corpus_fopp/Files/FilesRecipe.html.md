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
        Problem](/runestone/default/reportabug?course=fopp&page=FilesRecipe)
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
::: {#recipe-for-reading-and-processing-a-file .section}
[10.7. ]{.section-number}Recipe for Reading and Processing a File[¶](#recipe-for-reading-and-processing-a-file "Permalink to this heading"){.headerlink}
========================================================================================================================================================

Here's a foolproof recipe for processing the contents of a text file. If
you've fully digested the previous sections, you'll understand that
there are other options as well. Some of those options are preferable
for some situations, and some are preferred by python programmers for
efficiency reasons. In this course, though, you can always succeed by
following this recipe.

\#1. Open the file using `with`{.docutils .literal .notranslate} and
`open`{.docutils .literal .notranslate}.

\#2. Use `.readlines()`{.docutils .literal .notranslate} to get a list
of the lines of text in the file.

\#3. Use a `for`{.docutils .literal .notranslate} loop to iterate
through the strings in the list, each being one line from the file. On
each iteration, process that line of text

\#4. When you are done extracting data from the file, continue writing
your code outside of the indentation. Using `with`{.docutils .literal
.notranslate} will automatically close the file once the program exits
the with block.

::: {.highlight-default .notranslate}
::: {.highlight}
    fname = "yourfile.txt"
    with open(fname, 'r') as fileref:         # step 1
        lines = fileref.readlines()           # step 2
        for lin in lines:                     # step 3
            #some code that references the variable lin
    #some other code not relying on fileref   # step 4
:::
:::

However, this will not be good to use when you are working with large
data. Imagine working with a datafile that has 1000 rows of data. It
would take a long time to read in all the data and then if you had to
iterate over it, even more time would be necessary. This would be a case
where programmers prefer another option for efficiency reasons.

This option involves iterating over the file itself while still
iterating over each line in the file:

::: {.highlight-default .notranslate}
::: {.highlight}
    with open(fname, 'r') as fileref:
     for lin in fileref:
         ## some code that uses line as the current line of the file
         ## some more code
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

-   [[](With.html)]{#relations-prev}
-   [[](WritingTextFiles.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
