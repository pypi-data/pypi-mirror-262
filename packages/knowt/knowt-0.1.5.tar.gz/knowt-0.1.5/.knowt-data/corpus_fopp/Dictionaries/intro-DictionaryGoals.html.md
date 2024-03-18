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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-DictionaryGoals)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [11.1 Introduction:
        Dictionaries](intro-DictionaryGoals.html){.reference .internal}
    -   [11.2 Getting Started with
        Dictionaries](intro-Dictionaries.html){.reference .internal}
    -   [11.3 Dictionary
        operations](Dictionaryoperations.html){.reference .internal}
    -   [11.4 Dictionary methods](Dictionarymethods.html){.reference
        .internal}
    -   [11.5 Aliasing and copying](Aliasingandcopying.html){.reference
        .internal}
    -   [11.6 Introduction: Accumulating Multiple Results In a
        Dictionary](intro-AccumulatingMultipleResultsInaDictionary.html){.reference
        .internal}
    -   [11.7 Accumulating Results From a
        Dictionary](AccumulatingResultsFromaDictionary.html){.reference
        .internal}
    -   [11.8 Accumulating the Best
        Key](AccumulatingtheBestKey.html){.reference .internal}
    -   [11.9 👩‍💻 When to use a
        dictionary](WPChoosingDictionaries.html){.reference .internal}
    -   [11.10 Glossary](Glossary.html){.reference .internal}
    -   [11.11 Exercises](Exercises.html){.reference .internal}
    -   [11.12 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#introduction-dictionaries .section}
[]{#index-0}

[11.1. ]{.section-number}Introduction: Dictionaries[¶](#introduction-dictionaries "Permalink to this heading"){.headerlink}
===========================================================================================================================

The compound data types we have studied in detail so far --- strings and
lists --- are sequential collections. This means that the items in the
collection are ordered from left to right and they use integers as
indices to access the values they contain. This also means that looking
for a particular value requires scanning the many items in the list
until you find the desired value.

Data can sometimes be organized more usefully by associating a key with
the value we are looking for. For example, if you are asked for the page
number for the start of chapter 5 in a large textbook, you might flip
around the book looking for the chapter 5 heading. If the chapter number
appears in the header or footer of each page, you might be able to find
the page number fairly quickly but it's generally easier and faster to
go to the index page and see that chapter 5 starts on page 78.

This sort of direct look up of a value in Python is done with an object
called a Dictionary. Dictionaries are a different kind of collection.
They are Python's built-in **mapping** type. A map is an unordered,
associative collection. The association, or mapping, is from a **key**,
which can be of any immutable type (e.g., the chapter name and number in
the analogy above), to a **value** (the starting page number), which can
be any Python data object. You'll learn how to use these collections in
the following chapter.

::: {#learning-goals .section}
[11.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------

-   To introduce the idea of Key, Value pairs

-   To introduce the idea of an unordered sequence

-   To understand the use of parallel construction in lists

-   To understand the performance benefit and simplicity of a dictionary
    over parallel lists

-   To understand that dictionary iteration iterates over keys
:::

::: {#objectives .section}
[11.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------

To correctly use the following:

-   The index operator to add a key,value pair to a dictionary

-   The del operator to remove an entry

-   index operator - retrieval by key

-   search - contains in / not in

-   items

-   keys

-   values

-   get - with a default value
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

-   [[](toctree.html)]{#relations-prev}
-   [[](intro-Dictionaries.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
