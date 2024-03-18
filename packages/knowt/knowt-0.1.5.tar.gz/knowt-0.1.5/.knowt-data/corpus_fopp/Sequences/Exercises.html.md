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
        Problem](/runestone/default/reportabug?course=fopp&page=Exercises)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [6.1 Introduction: Sequences](intro-Sequences.html){.reference
        .internal}
    -   [6.2 Strings, Lists, and
        Tuples](StringsandLists.html){.reference .internal}
    -   [6.3 Index Operator: Working with the Characters of a
        String](IndexOperatorWorkingwiththeCharactersofaString.html){.reference
        .internal}
    -   [6.4 Disambiguating \[\]: creation vs
        indexing](DisabmiguatingSquareBrackets.html){.reference
        .internal}
    -   [6.5 Length](Length.html){.reference .internal}
    -   [6.6 The Slice Operator](TheSliceOperator.html){.reference
        .internal}
    -   [6.7 Concatenation and
        Repetition](ConcatenationandRepetition.html){.reference
        .internal}
    -   [6.8 Count and Index](CountandIndex.html){.reference .internal}
    -   [6.9 Splitting and Joining
        Strings](SplitandJoin.html){.reference .internal}
    -   [6.10 Exercises](Exercises.html){.reference .internal}
    -   [6.11 Chapter Assessment](week2a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#exercises .section}
[6.10. ]{.section-number}Exercises[¶](#exercises "Permalink to this heading"){.headerlink}
==========================================================================================

1.  ::: {.runestone .parsons-container}
    ::: {#pp5_11_1 .parsons component="parsons"}
    ::: {.parsons_question .parsons-text}
    Write a program that will print out the length of each item in the
    list as well as the first and last characters of the item.
    :::

    ``` {.parsonsblocks question_label="6.10.1" style="visibility: hidden;"}
            weather = ["sunny", "cloudy", "partially sunny",
               "rainy", "storming", "windy", "foggy",
               "snowy", "hailing"]
    ---
    for condition in weather:
    ---
        print("The word is", len(condition), "characters")
    ---
        first_char = condition[0]
        last_char = condition[-1]
    ---
        print("The first character is: " + first_char)
        print("The last character is: " + last_char)
            
    ```
    :::
    :::

2.  ::: {.runestone .parsons-container}
    ::: {#pp5_11_2 .parsons component="parsons"}
    ::: {.parsons_question .parsons-text}
    Write code to determine how many t's are in the following sentences.
    :::

    ``` {.parsonsblocks question_label="6.10.2" style="visibility: hidden;"}
            phrases = ["My, what a lovely day today is!",
    "Have you mastered cooking yet? A tasty treat could be in your future.",
    "Have you ever seen the leaves change color?"]
    ---
    for sentence in phrases:
    ---
        print(sentence.count("t"))
            
    ```
    :::
    :::

::: {#contributed-exercises .section}
[6.10.1. ]{.section-number}Contributed Exercises[¶](#contributed-exercises "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------
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

-   [[](SplitandJoin.html)]{#relations-prev}
-   [[](week2a1.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
