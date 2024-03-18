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
        Problem](/runestone/default/reportabug?course=fopp&page=ClassDecorators)
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
::: {#class-decorators .section}
[20.15. ]{.section-number}Class Decorators[¶](#class-decorators "Permalink to this heading"){.headerlink}
=========================================================================================================

Recall that Python has a [["decorator" syntax"]{.std
.std-ref}](../AdvancedFunctions/FunctionWrappingAndDecorators.html#decorators){.reference
.internal} that allows us to modify the behavior of functions. We can
use this same syntax to modify the behavior of classes. There are two
ways we can use decorators with classes: (1) by decorating individual
class methods or (2) by decorating the class itself.

**Decorating class methods** is analogous to the function decorators
we've already seen. For example, suppose we have the
`addLogging`{.docutils .literal .notranslate} function from
[[earlier]{.std
.std-ref}](../AdvancedFunctions/FunctionWrappingAndDecorators.html#decorators){.reference
.internal}:

::: {.highlight-default .notranslate}
::: {.highlight}
    def addLogging(func): # The argument, func is a function

        def wrapper(x): # x is the argument that we're going to pass to func
            print(f"About to call the function with argument {x}")
            result = func(x) # actually call our function and store the result
            print(f"Done with the function with argument {x}. Result: {result}")
            return result # return whatever our function returned

        return wrapper # return our new function
:::
:::

We first need to modify this function slightly to add `self`{.docutils
.literal .notranslate} as the first argument, since it will be a method
of a class. Then, we can use the function to decorate any class method
that accepts one argument:

::: {.runestone .explainer .ac_section}
::: {#ac20_15_1 component="activecode" question_label="20.15.1"}
::: {#ac20_15_1_question .ac_question}
:::
:::
:::

Beyond decorating class methods, we can also **decorate the class
itself**. Just like functions in Python, classes are "first class",
meaning they can be referenced like any other object, passed as
arguments, returned, and wrapped. We decorate classes in almost the same
way that we decorate functions, except that our decorator accepts a
*class* as an argument, rather than a function. We could then modify the
class, or return a new class. For example, suppose we want to create a
decorator (named `addBeep`{.docutils .literal .notranslate}) that adds
an extra method (named `beep`{.docutils .literal .notranslate}) to any
class. We could do that as follows:

::: {.runestone .explainer .ac_section}
::: {#ac20_15_2 component="activecode" question_label="20.15.2"}
::: {#ac20_15_2_question .ac_question}
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

-   [[](Tamagotchi.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
