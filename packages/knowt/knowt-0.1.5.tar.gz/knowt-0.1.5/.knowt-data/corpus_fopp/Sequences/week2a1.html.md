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
        Problem](/runestone/default/reportabug?course=fopp&page=week2a1)
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
::: {#chapter-assessment .section}
[6.11. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

**Check your understanding**

::: {.runestone}
-   [zpzpzpzpzp]{#assess_question2_1_1_1_opt_a}
-   The order of concatenation matters.
-   [zzzzzppppp]{#assess_question2_1_1_1_opt_b}
-   Think about the order that the program is executed in, what occurs
    first?
-   [pzpzpzpzpz]{#assess_question2_1_1_1_opt_c}
-   Yes, because let\_two was put before let, c has \"pz\" and then that
    is repeated five times.
-   [pppppzzzzz]{#assess_question2_1_1_1_opt_d}
-   Think about the order that the program is executed in, what occurs
    first?
-   [None of the above, an error will
    occur.]{#assess_question2_1_1_1_opt_e}
-   This is correct syntax and no errors will occur.
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac_2_1_1_2 component="activecode" question_label="6.11.2"}
::: {#assess_ac_2_1_1_2_question .ac_question}
Write a program that extracts the last three items in the list
`sports`{.docutils .literal .notranslate} and assigns it to the variable
`last`{.docutils .literal .notranslate}. Make sure to write your code so
that it works no matter how many items are in the list.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac_2_1_1_3 component="activecode" question_label="6.11.3"}
::: {#assess_ac_2_1_1_3_question .ac_question}
Write code that combines the following variables so that the sentence
"You are doing a great job, keep it up!" is assigned to the variable
`message`{.docutils .literal .notranslate}. Do not edit the values
assigned to `by`{.docutils .literal .notranslate}, `az`{.docutils
.literal .notranslate}, `io`{.docutils .literal .notranslate}, or
`qy`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone}
-   [\[\'travel\', \'lights\',
    \'moon\'\]]{#assess_question2_1_1_4_opt_a}
-   When we take a slice of something, it includes the item at the first
    index and excludes the item at the second index.
-   [\[\'world\', \'travel\',
    \'lights\'\]]{#assess_question2_1_1_4_opt_b}
-   When we take a slice of something, it includes the item at the first
    index and excludes the item at the second index. Additionally,
    Python is a zero-index based language.
-   [\[\'travel\', \'lights\'\]]{#assess_question2_1_1_4_opt_c}
-   Yes, python is a zero-index based language and slices are inclusive
    of the first index and exclusive of the second.
-   [\[\'world\', \'travel\'\]]{#assess_question2_1_1_4_opt_d}
-   Python is a zero-index based language.
:::

::: {.runestone}
-   [string]{#assess_question2_1_1_5_opt_a}
-   Not quite, is it slicing or accessing an element?
-   [integer]{#assess_question2_1_1_5_opt_b}
-   What is happening in the assignment statement for m?
-   [float]{#assess_question2_1_1_5_opt_c}
-   What is happening in the assignment statement for m?
-   [list]{#assess_question2_1_1_5_opt_d}
-   Yes, a slice returns a list no matter how large the slice.
:::

::: {.runestone}
-   [string]{#assess_question2_1_1_6_opt_a}
-   Yes, the quotes around the number mean that this is a string.
-   [integer]{#assess_question2_1_1_6_opt_b}
-   Not quite, look again at what is being extracted.
-   [float]{#assess_question2_1_1_6_opt_c}
-   Not quite, look again at what is being extracted.
-   [list]{#assess_question2_1_1_6_opt_d}
-   Not quite, is it slicing or accessing an element?
:::

::: {.runestone}
-   [string]{#assess_question2_1_1_7_opt_a}
-   Not quite; .split() returns a list, each of whose elements is a
    string.
-   [integer]{#assess_question2_1_1_7_opt_b}
-   Not quite, look again at what types are present and what the result
    of .split() is.
-   [float]{#assess_question2_1_1_7_opt_c}
-   Not quite, look again at what types are present and what the result
    of .split() is.
-   [list]{#assess_question2_1_1_7_opt_d}
-   Yes, the .split() method returns a list.
:::

::: {.runestone}
-   [string]{#assess_question2_1_1_8_opt_a}
-   Yes, the string is split into a list, then joined back into a
    string, then split again, and finally joined back into a string.
-   [integer]{#assess_question2_1_1_8_opt_b}
-   Not quite, look again at what types are present and what the result
    of .split() is.
-   [float]{#assess_question2_1_1_8_opt_c}
-   Not quite, look again at what types are present and what the result
    of .split() is.
-   [list]{#assess_question2_1_1_8_opt_d}
-   Not quite, think about what .split() and .join() return.
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac2_1_1_9 component="activecode" question_label="6.11.9"}
::: {#assess_ac2_1_1_9_question .ac_question}
Write code to determine how many 9's are in the list `nums`{.docutils
.literal .notranslate} and assign that value to the variable
`how_many`{.docutils .literal .notranslate}. Do not use a for loop to do
this.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac2_1_1_10 component="activecode" question_label="6.11.10"}
::: {#assess_ac2_1_1_10_question .ac_question}
Write code that uses slicing to get rid of the the second 8 so that here
are only two 8's in the list bound to the variable nums.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#access_ac_2_1_1_11 component="activecode" question_label="6.11.11"}
::: {#access_ac_2_1_1_11_question .ac_question}
Assign the last element of `lst`{.docutils .literal .notranslate} to the
variable `end_elem`{.docutils .literal .notranslate}. Do this so that it
works no matter how long lst is.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#access_ac_2_1_1_12 component="activecode" question_label="6.11.12"}
::: {#access_ac_2_1_1_12_question .ac_question}
Assign the number of elements in `lst`{.docutils .literal .notranslate}
to the variable `num_lst`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac_2_1_1_13 component="activecode" question_label="6.11.13"}
::: {#assess_ac_2_1_1_13_question .ac_question}
Create a variable called `wrds`{.docutils .literal .notranslate} and
assign to it a list whose elements are the words in the string
`sent`{.docutils .literal .notranslate}. Do not worry about punctuation.
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](../Iteration/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
