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
        Problem](/runestone/default/reportabug?course=fopp&page=TheSliceOperator)
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
::: {#the-slice-operator .section}
[]{#index-0}

[6.6. ]{.section-number}The Slice Operator[¶](#the-slice-operator "Permalink to this heading"){.headerlink}
===========================================================================================================

A substring of a string is called a **slice**. Selecting a slice is
similar to selecting a character:

::: {.runestone .explainer .ac_section}
::: {#ac5_6_1 component="activecode" question_label="6.6.1"}
::: {#ac5_6_1_question .ac_question}
:::
:::
:::

The `slice`{.docutils .literal .notranslate} operator `[n:m]`{.docutils
.literal .notranslate} returns the part of the string starting with the
character at index n and go up to but *not including* the character at
index m. Or with normal counting from 1, this is the (n+1)st character
up to and including the mth character.

If you omit the first index (before the colon), the slice starts at the
beginning of the string. If you omit the second index, the slice goes to
the end of the string.

::: {.runestone .explainer .ac_section}
::: {#ac5_6_2 component="activecode" question_label="6.6.2"}
::: {#ac5_6_2_question .ac_question}
:::
:::
:::

What do you think `fruit[:]`{.docutils .literal .notranslate} means?

::: {#list-slices .section}
[6.6.1. ]{.section-number}List Slices[¶](#list-slices "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------

The slice operation we saw with strings also work on lists. Remember
that the first index is the starting point for the slice and the second
number is one index past the end of the slice (up to but not including
that element). Recall also that if you omit the first index (before the
colon), the slice starts at the beginning of the sequence. If you omit
the second index, the slice goes to the end of the sequence.

::: {.runestone .explainer .ac_section}
::: {#ac5_6_3 component="activecode" question_label="6.6.1.1"}
::: {#ac5_6_3_question .ac_question}
:::
:::
:::
:::

::: {#tuple-slices .section}
[6.6.2. ]{.section-number}Tuple Slices[¶](#tuple-slices "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------

We can't modify the elements of a tuple, but we can make a variable
reference a new tuple holding different information. Thankfully we can
also use the slice operation on tuples as well as strings and lists. To
construct the new tuple, we can slice parts of the old tuple and join up
the bits to make the new tuple. So `julia`{.docutils .literal
.notranslate} has a new recent film, and we might want to change her
tuple. We can easily slice off the parts we want and concatenate them
with the new tuple.

::: {.runestone .explainer .ac_section}
::: {#ac5_6_4 component="activecode" question_label="6.6.2.1"}
::: {#ac5_6_4_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [python]{#question5_6_1_opt_a}
-   That would be s\[0:6\].
-   [rocks]{#question5_6_1_opt_b}
-   That would be s\[7:\].
-   [hon r]{#question5_6_1_opt_c}
-   Yes, start with the character at index 3 and go up to but not
    include the character at index 8.
-   [Error, you cannot have two numbers inside the \[
    \].]{#question5_6_1_opt_d}
-   This is called slicing, not indexing. It requires a start and an
    end.
:::

::: {.runestone}
-   [\[ \[ \], 3.14, False\]]{#question5_6_2_opt_a}
-   Yes, the slice starts at index 4 and goes up to and including the
    last item.
-   [\[ \[ \], 3.14\]]{#question5_6_2_opt_b}
-   By leaving out the upper bound on the slice, we go up to and
    including the last item.
-   [\[ \[56, 57, \"dog\"\], \[ \], 3.14, False\]]{#question5_6_2_opt_c}
-   Index values start at 0.
:::

::: {.runestone}
-   [2]{#question5_6_3_opt_a}
-   The list begins with the second item of L and includes everything up
    to but not including the last item.
-   [3]{#question5_6_3_opt_b}
-   Yes, there are 3 items in this list.
-   [4]{#question5_6_3_opt_c}
-   The list begins with the second item of L and includes everything up
    to but not including the last item.
-   [5]{#question5_6_3_opt_d}
-   The list begins with the second item of L and includes everything up
    to but not including the last item.
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_6_5 component="activecode" question_label="6.6.2.5"}
::: {#ac5_6_5_question .ac_question}
Create a new list using the 9th through 12th elements (four items in
all) of `new_lst`{.docutils .literal .notranslate} and assign it to the
variable `sub_lst`{.docutils .literal .notranslate}.
:::
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

-   [[](Length.html)]{#relations-prev}
-   [[](ConcatenationandRepetition.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
