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
        Problem](/runestone/default/reportabug?course=fopp&page=WritingCSVFiles)
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
::: {#writing-data-to-a-csv-file .section}
[10.11. ]{.section-number}Writing data to a CSV File[¶](#writing-data-to-a-csv-file "Permalink to this heading"){.headerlink}
=============================================================================================================================

The typical pattern for writing data to a CSV file will be to write a
header row and loop through the items in a list, outputting one row for
each.

Here is a simple example where we first make a list of the multiples of
12 and then write a file that looks like this.

::: {.highlight-default .notranslate}
::: {.highlight}
    1,12
    2,24
    3,36
    ...
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_14_1 component="activecode" question_label="10.11.1"}
::: {#ac9_14_1_question .ac_question}
:::
:::
:::

Here is a more complex example, where we a have a list of tuples, each
representing one Olympian, a subset of the rows and columns from the
file we have been reading from.

::: {.runestone .explainer .ac_section}
::: {#ac9_14_3 component="activecode" question_label="10.11.2"}
::: {#ac9_14_3_question .ac_question}
:::
:::
:::

There are a few things worth noting in the code above.

First, using .format() makes it really clear what we're doing when we
create the variable row\_string. We are making a comma separated set of
values; the {} curly braces indicated where to substitute in the actual
values. The equivalent string concatenation would be very hard to read.
An alternative, also clear way to do it would be with the .join method:
`row_string = ','.join([olympian[0], str(olympian[1]), olympian[2]])`{.docutils
.literal .notranslate}.

Second, unlike the print statement, remember that the .write() method on
a file object does not automatically insert a newline. Instead, we have
to explicitly add the character `\n`{.docutils .literal .notranslate} at
the end of each line.

Third, we have to explicitly refer to each of the elements of olympian
when building the string to write. Note that just putting
`.format(olympian)`{.docutils .literal .notranslate} wouldn't work
because the interpreter would see only one value (a tuple) when it was
expecting three values to try to substitute into the string template.
Later in the book we will see that python provides an advanced technique
for automatically unpacking the three values from the tuple, with
`.format(*olympian)`{.docutils .literal .notranslate}.

As described previously, if one or more columns contain text, and that
text could contain commas, we need to do something to distinguish a
comma in the text from a comma that is separating different values
(cells in the table). If we want to enclose each value in double quotes,
it can start to get a little tricky, because we will need to have the
double quote character inside the string output. But it is doable.
Indeed, one reason Python allows strings to be delimited with either
single quotes or double quotes is so that one can be used to delimit the
string and the other can be a character in the string. If you get to the
point where you need to quote all of the values, we recommend learning
to use python's csv module.

::: {.runestone .explainer .ac_section}
::: {#ac9_14_2 component="activecode" question_label="10.11.3"}
::: {#ac9_14_2_question .ac_question}
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

-   [[](ReadingCSVFiles.html)]{#relations-prev}
-   [[](WPTipsHandlingFiles.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
