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
::: {#chapter-assessment .section}
[20.18. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
=============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac_ch13_01 component="activecode" question_label="20.18.1"}
::: {#ac_ch13_01_question .ac_question}
Define a class called `Bike`{.docutils .literal .notranslate} that
accepts a string and a float as input, and assigns those inputs
respectively to two instance variables, `color`{.docutils .literal
.notranslate} and `price`{.docutils .literal .notranslate}. Assign to
the variable `testOne`{.docutils .literal .notranslate} an instance of
`Bike`{.docutils .literal .notranslate} whose color is **blue** and
whose price is **89.99**. Assign to the variable `testTwo`{.docutils
.literal .notranslate} an instance of Bike whose color is **purple** and
whose price is **25.0**.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_ch13_021 component="activecode" question_label="20.18.2"}
::: {#ac_ch13_021_question .ac_question}
Create a class called `AppleBasket`{.docutils .literal .notranslate}
whose constructor accepts two inputs: a string representing a color, and
a number representing a quantity of apples. The constructor should
initialize two instance variables: `apple_color`{.docutils .literal
.notranslate} and `apple_quantity`{.docutils .literal .notranslate}.
Write a class method called `increase`{.docutils .literal .notranslate}
that increases the quantity by `1`{.docutils .literal .notranslate} each
time it is invoked. You should also write a `__str__`{.docutils .literal
.notranslate} method for this class that returns a string of the format:
`"A basket of [quantity goes here] [color goes here] apples."`{.docutils
.literal .notranslate} e.g. `"A basket of 4 red apples."`{.docutils
.literal .notranslate} or `"A basket of 50 blue apples."`{.docutils
.literal .notranslate} (Writing some test code that creates instances
and assigns values to variables may help you solve this problem!)
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_ch13_03 component="activecode" question_label="20.18.3"}
::: {#ac_ch13_03_question .ac_question}
Define a class called `BankAccount`{.docutils .literal .notranslate}
that accepts the name you want associated with your bank account in a
string, and an integer that represents the amount of money in the
account. The constructor should initialize two instance variables from
those inputs: `name`{.docutils .literal .notranslate} and
`amt`{.docutils .literal .notranslate}. Add a string method so that when
you print an instance of `BankAccount`{.docutils .literal .notranslate},
you see
`"Your account, [name goes here], has [start_amt goes here] dollars."`{.docutils
.literal .notranslate} Create an instance of this class with
`"Bob"`{.docutils .literal .notranslate} as the name and `100`{.docutils
.literal .notranslate} as the amount. Save this to the variable
`t1`{.docutils .literal .notranslate}.
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
-   [[](../BuildingPrograms/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
