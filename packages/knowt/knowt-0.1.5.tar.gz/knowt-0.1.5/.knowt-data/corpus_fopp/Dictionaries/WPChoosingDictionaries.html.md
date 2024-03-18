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
        Problem](/runestone/default/reportabug?course=fopp&page=WPChoosingDictionaries)
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
::: {#when-to-use-a-dictionary .section}
[11.9. ]{.section-number}👩‍💻 When to use a dictionary[¶](#when-to-use-a-dictionary "Permalink to this heading"){.headerlink}
============================================================================================================================

Now that you have experience using lists and dictionaries, you will have
to decide which one is best to use in each situation. The following
guidelines will help you recognize when a dictionary will be beneficial:

-   When a piece of data consists of a set of properties of a single
    item, a dictionary is often better. You could try to keep track
    mentally that the zip code property is at index 2 in a list, but
    your code will be easier to read and you will make fewer mistakes if
    you can look up mydiction\['zipcode'\] than if you look up
    mylst\[2\].

-   When you have a collection of data pairs, and you will often have to
    look up one of the pairs based on its first value, it is better to
    use a dictionary than a list of (key, value) tuples. With a
    dictionary, you can find the value for any (key, value) tuple by
    looking up the key. With a list of tuples you would need to iterate
    through the list, examining each pair to see if it had the key that
    you want.

-   On the other hand, if you will have a collection of data pairs where
    multiple pairs share the same first data element, then you can't use
    a dictionary, because a dictionary requires all the keys to be
    distinct from each other.
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

-   [[](AccumulatingtheBestKey.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
