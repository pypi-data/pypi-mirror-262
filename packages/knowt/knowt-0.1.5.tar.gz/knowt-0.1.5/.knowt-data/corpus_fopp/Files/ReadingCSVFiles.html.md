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
        Problem](/runestone/default/reportabug?course=fopp&page=ReadingCSVFiles)
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
::: {#reading-in-data-from-a-csv-file .section}
[10.10. ]{.section-number}Reading in data from a CSV File[¶](#reading-in-data-from-a-csv-file "Permalink to this heading"){.headerlink}
=======================================================================================================================================

We are able to read in CSV files the same way we have with other text
files. Because of the standardized structure of the data, there is a
common pattern for processing it. To practice this, we will be using
data about olympic events.

Typically, CSV files will have a header as the first line, which
contains column names. Then, each following row in the file will contain
data that corresponds to the appropriate columns.

All file methods that we have mentioned - `read`{.docutils .literal
.notranslate}, `readline`{.docutils .literal .notranslate}, and
`readlines`{.docutils .literal .notranslate}, and simply iterating over
the file object itself - will work on CSV files. In our examples, we
will iterate over the lines. Because the values on each line are
separated with commas, we can use the `.split()`{.docutils .literal
.notranslate} method to parse each line into a collection of separate
value.

::: {.runestone .explainer .ac_section}
::: {#ac9_13_1 component="activecode" question_label="10.10.1"}
::: {#ac9_13_1_question .ac_question}
:::
:::
:::

In the above code, we open the file, olympics.txt, which contains data
on some olympians. The contents are similar to our previous olympics
file, but include an extra column with information about medals they
won.

We split the first row to get the field names. We split other rows to
get values. Note that we specify to split on commas by passing that as a
parameter. Also note that we first pass the row through the .strip()
method to get rid of the trailing n.

Once we have parsed the lines into their separate values, we can use
those values in the program. For example, in the code above, we select
only those rows where the olympian won a medal, and we print out only
three of the fields, in a different format.

Note that the trick of splitting the text for each row based on the
presence of commas only works because commas are not used in any of the
field values. Suppose that some of our events were more specific, and
used commas. For example, "Swimming, 100M Freestyle". How will a program
processing a .csv file know when a comma is separating columns, and when
it is just part of the text string giving a value within a column?

The CSV format is actually a little more general than we have described
and has a couple of solutions for that problem. One alternative format
uses a different column separator, such as \| or a tab (\\t). Sometimes,
when a tab is used, the format is called tsv, for tab-separated values).
If you get a file using a different separator, you can just call the
`.split('|')`{.docutils .literal .notranslate} or
`.split('\t')`{.docutils .literal .notranslate}.

The other advanced CSV format uses commas to separate but encloses all
values in double quotes.

For example, the data file might look like:

``` {#sample.txt}
"Name","Sex","Age","Team","Event","Medal"
"A Dijiang","M","24","China","Basketball","NA"
"Edgar Lindenau Aabye","M","34","Denmark/Sweden","Tug-Of-War","Gold"
"Christine Jacoba Aaftink","F","21","Netherlands","Speed Skating, 1500M","NA"
```

If you are reading a .csv file that has enclosed all values in double
quotes, it's actually a pretty tricky programming problem to split the
text for one row into a list of values. You won't want to try to do it
directly. Instead, you should use python's built-in csv module. However,
there's a bit of a learning curve for that, and we find that students
gain a better understanding of reading CSV format by first learning to
read the simple, unquoted format and split lines on commas.
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

-   [[](CSVFormat.html)]{#relations-prev}
-   [[](WritingCSVFiles.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
