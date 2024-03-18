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
        Problem](/runestone/default/reportabug?course=fopp&page=NestedIteration)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [17.1 Introduction: Nested Data and Nested
        Iteration](ListswithComplexItems.html){.reference .internal}
    -   [17.2 Nested Dictionaries](NestedDictionaries.html){.reference
        .internal}
    -   [17.3 Processing JSON results](jsonlib.html){.reference
        .internal}
    -   [17.4 Nested Iteration](NestedIteration.html){.reference
        .internal}
    -   [17.5 👩‍💻 Structuring Nested
        Data](WPStructuringNestedData.html){.reference .internal}
    -   [17.6 Deep and Shallow
        Copies](DeepandShallowCopies.html){.reference .internal}
    -   [17.7 👩‍💻 Extracting from Nested
        Data](WPExtractFromNestedData.html){.reference .internal}
    -   [17.8 Exercises](Exercises.html){.reference .internal}
    -   [17.9 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#nested-iteration .section}
[17.4. ]{.section-number}Nested Iteration[¶](#nested-iteration "Permalink to this heading"){.headerlink}
========================================================================================================

When you have nested data structures, especially lists and/or
dictionaries, you will frequently need nested for loops to traverse
them.

::: {.runestone .explainer .ac_section}
::: {#ac17_4_1 component="activecode" question_label="17.4.1"}
::: {#ac17_4_1_question .ac_question}
:::
:::
:::

Line 3 executes once for each top-level list, three times in all. With
each sub-list, line 5 executes once for each item in the sub-list. Try
stepping through it in Codelens to make sure you understand what the
nested iteration does.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="17.4.2"}
::: {#clens17_4_1_question .ac_question}
:::

::: {#clens17_4_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 17.4.2 (clens17\_4\_1)]{.runestone_caption_text}
:::
:::

**Check Your Understanding**

::: {.runestone .parsons-container}
::: {#pp17_4_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Now try rearranging these code fragments to make a function that counts
all the *leaf* items in a nested list like nested1 above, the items at
the lowest level of nesting (8 of them in nested1).
:::

``` {.parsonsblocks question_label="17.4.3" style="visibility: hidden;"}
        def count_leaves(n):
---
    count = 0
---
    for L in n:
---
        for x in L:
---
            count = count + 1
---
    return count
        
```
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac17_4_2 component="activecode" question_label="17.4.4"}
::: {#ac17_4_2_question .ac_question}
**2.** Below, we have provided a list of lists that contain information
about people. Write code to create a new list that contains every
person's last name, and save that list as `last_names`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac17_4_3 component="activecode" question_label="17.4.5"}
::: {#ac17_4_3_question .ac_question}
**3.** Below, we have provided a list of lists named `L`{.docutils
.literal .notranslate}. Use nested iteration to save every string
containing "b" into a new list named `b_strings`{.docutils .literal
.notranslate}.
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

-   [[](jsonlib.html)]{#relations-prev}
-   [[](WPStructuringNestedData.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
