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
        Problem](/runestone/default/reportabug?course=fopp&page=ReadingaFile)
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
::: {#reading-a-file .section}
[10.2. ]{.section-number}Reading a File[¶](#reading-a-file "Permalink to this heading"){.headerlink}
====================================================================================================

As an example, suppose we have a text file called
`olympics.txt`{.docutils .literal .notranslate} that contains the data
representing about olympians across different years. The contents of the
file are shown at the bottom of the page.

To open this file, we would call the `open`{.docutils .literal
.notranslate} function. The variable, `fileref`{.docutils .literal
.notranslate}, now holds a reference to the file object returned by
`open`{.docutils .literal .notranslate}. When we are finished with the
file, we can close it by using the `close`{.docutils .literal
.notranslate} method. After the file is closed any further attempts to
use `fileref`{.docutils .literal .notranslate} will result in an error.

::: {.runestone .explainer .ac_section}
::: {#ac9_2_1 component="activecode" question_label="10.2.1"}
::: {#ac9_2_1_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

A common mistake is to get confused about whether you are providing a
variable name or a string literal as an input to the open function. In
the code above, "olympics.txt" is a string literal that should
correspond to the name of a file on your computer. If you put something
without quotes, like `open(x, "r")`{.docutils .literal .notranslate}, it
will be treated as a variable name. In this example, x should be a
variable that's already been bound to a string value like
"olympics.txt".
:::

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `olympics.txt`
:::

``` {#olympics.txt component="datafile" edit="false" data-rows="20" data-cols="65"}
Name,Sex,Age,Team,Event,Medal
A Dijiang,M,24,China,Basketball,NA
A Lamusi,M,23,China,Judo,NA
Gunnar Nielsen Aaby,M,24,Denmark,Football,NA
Edgar Lindenau Aabye,M,34,Denmark/Sweden,Tug-Of-War,Gold
Christine Jacoba Aaftink,F,21,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,21,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,25,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,25,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,27,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,27,Netherlands,Speed Skating,NA
Per Knut Aaland,M,31,United States,Cross Country Skiing,NA
Per Knut Aaland,M,31,United States,Cross Country Skiing,NA
Per Knut Aaland,M,31,United States,Cross Country Skiing,NA
Per Knut Aaland,M,31,United States,Cross Country Skiing,NA
Per Knut Aaland,M,33,United States,Cross Country Skiing,NA
Per Knut Aaland,M,33,United States,Cross Country Skiing,NA
Per Knut Aaland,M,33,United States,Cross Country Skiing,NA
Per Knut Aaland,M,33,United States,Cross Country Skiing,NA
John Aalberg,M,31,United States,Cross Country Skiing,NA
John Aalberg,M,31,United States,Cross Country Skiing,NA
John Aalberg,M,31,United States,Cross Country Skiing,NA
John Aalberg,M,31,United States,Cross Country Skiing,NA
John Aalberg,M,33,United States,Cross Country Skiing,NA
John Aalberg,M,33,United States,Cross Country Skiing,NA
John Aalberg,M,33,United States,Cross Country Skiing,NA
John Aalberg,M,33,United States,Cross Country Skiing,NA
"Cornelia ""Cor"" Aalten (-Strannood)",F,18,Netherlands,Athletics,NA
"Cornelia ""Cor"" Aalten (-Strannood)",F,18,Netherlands,Athletics,NA
Antti Sami Aalto,M,26,Finland,Ice Hockey,NA
"Einar Ferdinand ""Einari"" Aalto",M,26,Finland,Swimming,NA
Jorma Ilmari Aalto,M,22,Finland,Cross Country Skiing,NA
Jyri Tapani Aalto,M,31,Finland,Badminton,NA
Minna Maarit Aalto,F,30,Finland,Sailing,NA
Minna Maarit Aalto,F,34,Finland,Sailing,NA
Pirjo Hannele Aalto (Mattila-),F,32,Finland,Biathlon,NA
Arvo Ossian Aaltonen,M,22,Finland,Swimming,NA
Arvo Ossian Aaltonen,M,22,Finland,Swimming,NA
Arvo Ossian Aaltonen,M,30,Finland,Swimming,Bronze
Arvo Ossian Aaltonen,M,30,Finland,Swimming,Bronze
Arvo Ossian Aaltonen,M,34,Finland,Swimming,NA
Juhamatti Tapio Aaltonen,M,28,Finland,Ice Hockey,Bronze
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,Bronze
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,Gold
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,Gold
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,28,Finland,Gymnastics,Gold
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,Bronze
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Paavo Johannes Aaltonen,M,32,Finland,Gymnastics,NA
Timo Antero Aaltonen,M,31,Finland,Athletics,NA
Win Valdemar Aaltonen,M,54,Finland,Art Competitions,NA
```
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

-   [[](intro-WorkingwithDataFiles.html)]{#relations-prev}
-   [[](AlternativeFileReadingMethods.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
