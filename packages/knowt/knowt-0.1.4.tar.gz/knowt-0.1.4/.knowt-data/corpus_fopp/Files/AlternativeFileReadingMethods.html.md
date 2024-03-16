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
        Problem](/runestone/default/reportabug?course=fopp&page=AlternativeFileReadingMethods)
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
::: {#alternative-file-reading-methods .section}
[10.3. ]{.section-number}Alternative File Reading Methods[¶](#alternative-file-reading-methods "Permalink to this heading"){.headerlink}
========================================================================================================================================

Once you have a file "object", the thing returned by the open function,
Python provides three methods to read data from that object. The
`read()`{.docutils .literal .notranslate} method returns the entire
contents of the file as a single string (or just some characters if you
provide a number as an input parameter. The `readlines`{.docutils
.literal .notranslate} method returns the entire contents of the entire
file as a list of strings, where each item in the list is one line of
the file. The `readline`{.docutils .literal .notranslate} method reads
one line from the file and returns it as a string. The strings returned
by `readlines`{.docutils .literal .notranslate} or `readline`{.docutils
.literal .notranslate} will contain the newline character at the end.
[[Table 2]{.std .std-ref}](#filemethods2a){.reference .internal}
summarizes these methods and the following session shows them in action.

  **Method Name**                                   **Use**                                                     **Explanation**
  ------------------------------------------------- ----------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `write`{.docutils .literal .notranslate}          `filevar.write(astring)`{.docutils .literal .notranslate}   Add a string to the end of the file. `filevar`{.docutils .literal .notranslate} must refer to a file that has been opened for writing.
  `read(n)`{.docutils .literal .notranslate}        `filevar.read()`{.docutils .literal .notranslate}           Read and return a string of `n`{.docutils .literal .notranslate} characters, or the entire file as a single string if `n`{.docutils .literal .notranslate} is not provided.
  `readline(n)`{.docutils .literal .notranslate}    `filevar.readline()`{.docutils .literal .notranslate}       Read and return the next line of the file with all text up to and including the newline character. If `n`{.docutils .literal .notranslate} is provided as a parameter, then only `n`{.docutils .literal .notranslate} characters will be returned if the line is longer than `n`{.docutils .literal .notranslate}. **Note** the parameter `n`{.docutils .literal .notranslate} is not supported in the browser version of Python, and in fact is rarely used in practice, you can safely ignore it.
  `readlines(n)`{.docutils .literal .notranslate}   `filevar.readlines()`{.docutils .literal .notranslate}      Returns a list of strings, each representing a single line of the file. If `n`{.docutils .literal .notranslate} is not provided then all lines of the file are returned. If `n`{.docutils .literal .notranslate} is provided then `n`{.docutils .literal .notranslate} characters are read but `n`{.docutils .literal .notranslate} is rounded up so that an entire line is returned. **Note** Like `readline`{.docutils .literal .notranslate} `readlines`{.docutils .literal .notranslate} ignores the parameter `n`{.docutils .literal .notranslate} in the browser.

In this course, we will generally either iterate through the lines
returned by `readlines()`{.docutils .literal .notranslate} with a for
loop, or use `read()`{.docutils .literal .notranslate} to get all of the
contents as a single string.

In other programming languages, where they don't have the convenient for
loop method of going through the lines of the file one by one, they use
a different pattern which requires a different kind of loop, the
`while`{.docutils .literal .notranslate} loop. Fortunately, you don't
need to learn this other pattern, and we will put off consideration of
`while`{.docutils .literal .notranslate} loops until later in this
course. We don't need them for handling data from files.

::: {.admonition .note}
Note

A common error that novice programmers make is not realizing that all
these ways of reading the file contents, **use up the file**. After you
call readlines(), if you call it again you'll get an empty list.
:::

**Check your Understanding**

``` {#school_prompt.txt}
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

::: {.runestone .explainer .ac_section}
::: {#ac9_4_1 component="activecode" question_label="10.3.1"}
::: {#ac9_4_1_question .ac_question}
1.  Using the file `school_prompt2.txt`{.docutils .literal
    .notranslate}, find the number of characters in the file and assign
    that value to the variable `num_char`{.docutils .literal
    .notranslate}.
:::
:::
:::

``` {#travel_plans.txt}
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

::: {.runestone .explainer .ac_section}
::: {#ac9_4_2 component="activecode" question_label="10.3.2"}
::: {#ac9_4_2_question .ac_question}
2.  Find the number of lines in the file, `travel_plans2.txt`{.docutils
    .literal .notranslate}, and assign it to the variable
    `num_lines`{.docutils .literal .notranslate}.
:::
:::
:::

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
::: {#ac9_4_3 component="activecode" question_label="10.3.3"}
::: {#ac9_4_3_question .ac_question}
3.  Create a string called `first_forty`{.docutils .literal
    .notranslate} that is comprised of the first 40 characters of
    `emotion_words2.txt`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .datafile}
::: {.datafile_caption}
Data file: `travel_plans2.txt`
:::

``` {#travel_plans2.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="65"}
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
Data file: `school_prompt2.txt`
:::

``` {#school_prompt2.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="65"}
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
Data file: `emotion_words2.txt`
:::

``` {#emotion_words2.txt component="datafile" data-hidden="" edit="false" data-rows="20" data-cols="62"}
Sad upset blue down melancholy somber bitter troubled
Angry mad enraged irate irritable wrathful outraged infuriated
Happy cheerful content elated joyous delighted lively glad
Confused disoriented puzzled perplexed dazed befuddled
Excited eager thrilled delighted
Scared afraid fearful panicked terrified petrified startled
Nervous anxious jittery jumpy tense uneasy apprehensive
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

-   [[](ReadingaFile.html)]{#relations-prev}
-   [[](Iteratingoverlinesinafile.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
