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
        Problem](/runestone/default/reportabug?course=fopp&page=toctree)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [20.1 Introduction: Classes and Objects - the
        Basics](intro-ClassesandObjectstheBasics.html){.reference
        .internal}
    -   [20.2 Objects Revisited](ObjectsRevisited.html){.reference
        .internal}
    -   [20.3 User Defined Classes](UserDefinedClasses.html){.reference
        .internal}
    -   [20.4 Adding Parameters to the
        Constructor](ImprovingourConstructor.html){.reference .internal}
    -   [20.5 Adding Other Methods to a
        Class](AddingOtherMethodstoourClass.html){.reference .internal}
    -   [20.6 Objects as Arguments and
        Parameters](ObjectsasArgumentsandParameters.html){.reference
        .internal}
    -   [20.7 Converting an Object to a
        String](ConvertinganObjecttoaString.html){.reference .internal}
    -   [20.8 Instances as Return
        Values](InstancesasReturnValues.html){.reference .internal}
    -   [20.9 Sorting Lists of
        Instances](sorting_instances.html){.reference .internal}
    -   [20.10 Class Variables and Instance
        Variables](ClassVariablesInstanceVariables.html){.reference
        .internal}
    -   [20.11 Public and Private Instance
        Variables](PrivateInstanceVariables.html){.reference .internal}
    -   [20.12 Thinking About Classes and
        Instances](ThinkingAboutClasses.html){.reference .internal}
    -   [20.13 Testing classes](TestingClasses.html){.reference
        .internal}
    -   [20.14 A Tamagotchi Game](Tamagotchi.html){.reference .internal}
    -   [20.15 Class Decorators](ClassDecorators.html){.reference
        .internal}
    -   [20.16 Glossary](Glossary.html){.reference .internal}
    -   [20.17 Exercises](Exercises.html){.reference .internal}
    -   [20.18 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#defining-your-own-classes .section}
[20. ]{.section-number}Defining your own Classes[¶](#defining-your-own-classes "Permalink to this heading"){.headerlink}
========================================================================================================================

::: {.toctree-wrapper .compound}
[Defining your own Classes]{.caption-text}

-   [20.1. Introduction: Classes and Objects - the
    Basics](intro-ClassesandObjectstheBasics.html){.reference .internal}
    -   [20.1.1. Object-oriented
        programming](intro-ClassesandObjectstheBasics.html#object-oriented-programming){.reference
        .internal}
-   [20.2. Objects Revisited](ObjectsRevisited.html){.reference
    .internal}
-   [20.3. User Defined Classes](UserDefinedClasses.html){.reference
    .internal}
-   [20.4. Adding Parameters to the
    Constructor](ImprovingourConstructor.html){.reference .internal}
-   [20.5. Adding Other Methods to a
    Class](AddingOtherMethodstoourClass.html){.reference .internal}
-   [20.6. Objects as Arguments and
    Parameters](ObjectsasArgumentsandParameters.html){.reference
    .internal}
-   [20.7. Converting an Object to a
    String](ConvertinganObjecttoaString.html){.reference .internal}
-   [20.8. Instances as Return
    Values](InstancesasReturnValues.html){.reference .internal}
-   [20.9. Sorting Lists of
    Instances](sorting_instances.html){.reference .internal}
    -   [20.9.1. Approach 1: Sorting Lists of Instances with
        `key`{.docutils .literal
        .notranslate}](sorting_instances.html#approach-1-sorting-lists-of-instances-with-key){.reference
        .internal}
    -   [20.9.2. Approach 2: Defining Sort Orders with Comparison
        Operators](sorting_instances.html#approach-2-defining-sort-orders-with-comparison-operators){.reference
        .internal}
-   [20.10. Class Variables and Instance
    Variables](ClassVariablesInstanceVariables.html){.reference
    .internal}
-   [20.11. Public and Private Instance
    Variables](PrivateInstanceVariables.html){.reference .internal}
-   [20.12. Thinking About Classes and
    Instances](ThinkingAboutClasses.html){.reference .internal}
-   [20.13. Testing classes](TestingClasses.html){.reference .internal}
-   [20.14. A Tamagotchi Game](Tamagotchi.html){.reference .internal}
-   [20.15. Class Decorators](ClassDecorators.html){.reference
    .internal}
-   [20.16. Glossary](Glossary.html){.reference .internal}
-   [20.17. Exercises](Exercises.html){.reference .internal}
    -   [20.17.1. Contributed
        Exercises](Exercises.html#contributed-exercises){.reference
        .internal}
-   [20.18. Chapter Assessment](ChapterAssessment.html){.reference
    .internal}
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

-   [[](../Exceptions/ChapterAssessment.html)]{#relations-prev}
-   [[](intro-ClassesandObjectstheBasics.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
