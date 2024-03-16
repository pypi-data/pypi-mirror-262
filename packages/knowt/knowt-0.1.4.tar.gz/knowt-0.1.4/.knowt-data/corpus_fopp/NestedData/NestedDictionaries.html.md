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
        Problem](/runestone/default/reportabug?course=fopp&page=NestedDictionaries)
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
::: {#nested-dictionaries .section}
[17.2. ]{.section-number}Nested Dictionaries[¶](#nested-dictionaries "Permalink to this heading"){.headerlink}
==============================================================================================================

Just as lists can contain items of any type, the value associated with a
key in a dictionary can also be an object of any type. In particular, it
is often useful to have a list or a dictionary as a value in a
dictionary. And of course, those lists or dictionaries can also contain
lists and dictionaries. There can be many layers of nesting.

Only the values in dictionaries can be objects of arbitrary type. The
keys in dictionaries must be one of the immutable data types (numbers,
strings, tuples).

**Check Your Understanding**

::: {.runestone}
-   [d\[5\] = {1: 2, 3: 4}]{#question17_2_1_opt_a}
-   5 is a valid key; {1:2, 3:4} is a dictionary with two keys, and is a
    valid value to associate with key 5.
-   [d\[{1:2, 3:4}\] = 5]{#question17_2_1_opt_b}
-   Dictionary keys must be of immutable types. A dictionary can\'t be
    used as a key in a dictionary.
-   [d\[\'key1\'\]\[\'d\'\] = d\[\'key2\'\]]{#question17_2_1_opt_c}
-   d\[\'key2\'\] is {\'b\': 3, \'c\': \"yes\"}, a python object. It can
    be bound to the key \'d\' in a dictionary {\'a\': 5, \'c\': 90, 5:
    50}
-   [d\[key2\] = 3]{#question17_2_1_opt_d}
-   key2 is an unbound variable here. d\[\'key2\'\] would be OK.
:::

::: {.runestone .explainer .ac_section}
::: {#ac17_2_1 component="activecode" question_label="17.2.2"}
::: {#ac17_2_1_question .ac_question}
**1.** Extract the value associated with the key color and assign it to
the variable `color`{.docutils .literal .notranslate}. Do not hard code
this.
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

-   [[](ListswithComplexItems.html)]{#relations-prev}
-   [[](jsonlib.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
