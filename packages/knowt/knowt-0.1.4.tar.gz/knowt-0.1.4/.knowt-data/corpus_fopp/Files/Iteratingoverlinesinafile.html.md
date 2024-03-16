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
        Problem](/runestone/default/reportabug?course=fopp&page=Iteratingoverlinesinafile)
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

::: {#iterating-over-lines-in-a-file .section}
[10.4. ]{.section-number}Iterating over lines in a file[¶](#iterating-over-lines-in-a-file "Permalink to this heading"){.headerlink}
====================================================================================================================================

We will now use this file as input in a program that will do some data
processing. In the program, we will examine each line of the file and
print it with some additional text. Because `readlines()`{.docutils
.literal .notranslate} returns a list of lines of text, we can use the
*for* loop to iterate through each line of the file.

A **line** of a file is defined to be a sequence of characters up to and
including a special character called the **newline** character. If you
evaluate a string that contains a newline character you will see the
character represented as `\n`{.docutils .literal .notranslate}. If you
print a string that contains a newline you will not see the
`\n`{.docutils .literal .notranslate}, you will just see its effects (a
carriage return).

As the *for* loop iterates through each line of the file the loop
variable will contain the current line of the file as a string of
characters. The general pattern for processing each line of a text file
is as follows:

::: {.highlight-default .notranslate}
::: {.highlight}
    for line in myFile.readlines():
        statement1
        statement2
        ...
:::
:::

To process all of our olympics data, we will use a *for* loop to iterate
over the lines of the file. Using the `split`{.docutils .literal
.notranslate} method, we can break each line into a list containing all
the fields of interest about the athlete. We can then take the values
corresponding to name, team and event to construct a simple sentence.

::: {.runestone .explainer .ac_section}
::: {#ac9_5_1 component="activecode" question_label="10.4.1"}
::: {#ac9_5_1_question .ac_question}
:::
:::
:::

To make the code a little simpler, and to allow for more efficient
processing, Python provides a built-in way to iterate through the
contents of a file one line at a time, without first reading them all
into a list. Some students find this confusing initially, so we don't
recommend doing it this way, until you get a little more comfortable
with Python. But this idiom is preferred by Python programmers, so you
should be prepared to read it. And when you start dealing with big
files, you may notice the efficiency gains of using it.

::: {.runestone .explainer .ac_section}
::: {#ac9_5_2 component="activecode" question_label="10.4.2"}
::: {#ac9_5_2_question .ac_question}
:::
:::
:::

``` {#olympics.txt hidden=""}
Name,Sex,Age,Team,Event,Medal
A Dijiang,M,24,China,Basketball,NA
A Lamusi,M,23,China,Judo,NA
Gunnar Nielsen Aaby,M,24,Denmark,Football,NA
Edgar Lindenau Aabye,M,34,Denmark/Sweden,Tug-Of-War,Gold
Christine Jacoba Aaftink,F,21,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,25,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,25,Netherlands,Speed Skating,NA
Christine Jacoba Aaftink,F,27,Netherlands,Speed Skating,NA
Per Knut Aaland,M,31,United States,Cross Country Skiing,NA
Per Knut Aaland,M,33,United States,Cross Country Skiing,NA
John Aalberg,M,31,United States,Cross Country Skiing,NA
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
Timo Antero Aaltonen,M,31,Finland,Athletics,NA
Win Valdemar Aaltonen,M,54,Finland,Art Competitions,NA
```

**Check your Understanding**

``` {#emotion_words.txt}
Sad upset blue down melancholy somber bitter troubled
Angry mad enraged irate irritable wrathful outraged infuriated
Happy cheerful content elated joyous delighted lively glad
Confused disoriented puzzled perplexed dazed befuddled
Excited eager thrilled delighted
Scared afraid fearful panicked terrified petrified startled
Nervous anxious jittery jumpy tense uneasy apprehensive
```

::: {.runestone .explainer .ac_section}
::: {#ac9_5_3 component="activecode" question_label="10.4.3"}
::: {#ac9_5_3_question .ac_question}
1.  Write code to find out how many lines are in the file
    `emotion_words.txt`{.docutils .literal .notranslate} as shown above.
    Save this value to the variable `num_lines`{.docutils .literal
    .notranslate}. Do not use the len method.
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

-   [[](AlternativeFileReadingMethods.html)]{#relations-prev}
-   [[](FindingaFileonyourDisk.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
