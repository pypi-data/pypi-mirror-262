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
        Problem](/runestone/default/reportabug?course=fopp&page=ChapterAssessment)
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
::: {#chapter-assessment .section}
[10.15. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
=============================================================================================================

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `travel_plans.txt`
:::

``` {#travel_plans.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="65"}
This summer I will be travelling.
I will go to...
Italy: Rome
Greece: Athens
England: London, Manchester
France: Paris, Nice, Lyon
Spain: Madrid, Barcelona, Granada
Austria: Vienna
I will probably not even want to come back!
However, I wonder how I will get by with all the different languages.
I only know English!
```
:::

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `school_prompt.txt`
:::

``` {#school_prompt.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="65"}
Writing essays for school can be difficult but
many students find that by researching their topic that they
have more to say and are better informed. Here are the university
we require many undergraduate students to take a first year writing requirement
so that they can
have a solid foundation for their writing skills. This comes
in handy for many students.
Different schools have different requirements, but everyone uses
writing at some point in their academic career, be it essays, research papers,
technical write ups, or scripts.
```
:::

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `emotion_words.txt`
:::

``` {#emotion_words.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="62"}
Sad upset blue down melancholy somber bitter troubled
Angry mad enraged irate irritable wrathful outraged infuriated
Happy cheerful content elated joyous delighted lively glad
Confused disoriented puzzled perplexed dazed befuddled
Excited eager thrilled delighted
Scared afraid fearful panicked terrified petrified startled
Nervous anxious jittery jumpy tense uneasy apprehensive
```
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_1 component="activecode" question_label="10.15.4"}
::: {#ac9_10_1_question .ac_question}
The textfile, `travel_plans.txt`{.docutils .literal .notranslate},
contains the summer travel plans for someone with some commentary. Find
the total number of characters in the file and save to the variable
`num`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_2 component="activecode" question_label="10.15.5"}
::: {#ac9_10_2_question .ac_question}
We have provided a file called `emotion_words.txt`{.docutils .literal
.notranslate} that contains lines of words that describe emotions. Find
the total number of words in the file and assign this value to the
variable `num_words`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_3 component="activecode" question_label="10.15.6"}
::: {#ac9_10_3_question .ac_question}
Assign to the variable `num_lines`{.docutils .literal .notranslate} the
number of lines in the file `school_prompt.txt`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_4 component="activecode" question_label="10.15.7"}
::: {#ac9_10_4_question .ac_question}
Assign the first 30 characters of `school_prompt.txt`{.docutils .literal
.notranslate} as a string to the variable `beginning_chars`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_5 component="activecode" question_label="10.15.8"}
::: {#ac9_10_5_question .ac_question}
**Challenge:** Using the file `school_prompt.txt`{.docutils .literal
.notranslate}, assign the third word of every line to a list called
`three`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_6 component="activecode" question_label="10.15.9"}
::: {#ac9_10_6_question .ac_question}
**Challenge:** Create a list called `emotions`{.docutils .literal
.notranslate} that contains the first word of every line in
`emotion_words.txt`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_7 component="activecode" question_label="10.15.10"}
::: {#ac9_10_7_question .ac_question}
Assign the first 33 characters from the textfile,
`travel_plans.txt`{.docutils .literal .notranslate} to the variable
`first_chars`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac9_10_8 component="activecode" question_label="10.15.11"}
::: {#ac9_10_8_question .ac_question}
**Challenge:** Using the file `school_prompt.txt`{.docutils .literal
.notranslate}, if the character 'p' is in a word, then add the word to a
list called `p_words`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_9_10_9 component="activecode" question_label="10.15.12"}
::: {#ac_9_10_9_question .ac_question}
Read in the contents of the file `SP500.txt`{.docutils .literal
.notranslate} which has monthly data for 2016 and 2017 about the S&P 500
closing prices as well as some other financial indicators, including the
"Long Term Interest Rate", which is interest rate paid on 10-year U.S.
government bonds.

Write a program that computes the average closing price (the second
column, labeled SP500) and the highest long-term interest rate. Both
should be computed only for the period from June 2016 through May 2017.
Save the results in the variables `mean_SP`{.docutils .literal
.notranslate} and `max_interest`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `SP500.txt`
:::

``` {#SP500.txt component="datafile" edit="false" data-rows="20" data-cols="65"}
Date,SP500,Dividend,Earnings,Consumer Price Index,Long Interest Rate,Real Price,Real Dividend,Real Earnings,PE10
1/1/2016,1918.6,43.55,86.5,236.92,2.09,2023.23,45.93,91.22,24.21
2/1/2016,1904.42,43.72,86.47,237.11,1.78,2006.62,46.06,91.11,24
3/1/2016,2021.95,43.88,86.44,238.13,1.89,2121.32,46.04,90.69,25.37
4/1/2016,2075.54,44.07,86.6,239.26,1.81,2167.27,46.02,90.43,25.92
5/1/2016,2065.55,44.27,86.76,240.23,1.81,2148.15,46.04,90.23,25.69
6/1/2016,2083.89,44.46,86.92,241.02,1.64,2160.13,46.09,90.1,25.84
7/1/2016,2148.9,44.65,87.64,240.63,1.5,2231.13,46.36,91,26.69
8/1/2016,2170.95,44.84,88.37,240.85,1.56,2251.95,46.51,91.66,26.95
9/1/2016,2157.69,45.03,89.09,241.43,1.63,2232.83,46.6,92.19,26.73
10/1/2016,2143.02,45.25,90.91,241.73,1.76,2214.89,46.77,93.96,26.53
11/1/2016,2164.99,45.48,92.73,241.35,2.14,2241.08,47.07,95.99,26.85
12/1/2016,2246.63,45.7,94.55,241.43,2.49,2324.83,47.29,97.84,27.87
1/1/2017,2275.12,45.93,96.46,242.84,2.43,2340.67,47.25,99.24,28.06
2/1/2017,2329.91,46.15,98.38,243.6,2.42,2389.52,47.33,100.89,28.66
3/1/2017,2366.82,46.38,100.29,243.8,2.48,2425.4,47.53,102.77,29.09
4/1/2017,2359.31,46.66,101.53,244.52,2.3,2410.56,47.67,103.74,28.9
5/1/2017,2395.35,46.94,102.78,244.73,2.3,2445.29,47.92,104.92,29.31
6/1/2017,2433.99,47.22,104.02,244.96,2.19,2482.48,48.16,106.09,29.75
7/1/2017,2454.1,47.54,105.04,244.79,2.32,2504.72,48.52,107.21,30
8/1/2017,2456.22,47.85,106.06,245.52,2.21,2499.4,48.69,107.92,29.91
9/1/2017,2492.84,48.17,107.08,246.82,2.2,2523.31,48.76,108.39,30.17
10/1/2017,2557,48.42,108.01,246.66,2.36,2589.89,49.05,109.4,30.92
11/1/2017,2593.61,48.68,108.95,246.67,2.35,2626.9,49.3,110.35,31.3
12/1/2017,2664.34,48.93,109.88,246.52,2.4,2700.13,49.59,111.36,32.09
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](../Dictionaries/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
