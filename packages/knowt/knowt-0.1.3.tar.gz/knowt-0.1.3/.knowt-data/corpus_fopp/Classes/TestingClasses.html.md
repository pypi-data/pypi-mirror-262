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
        Problem](/runestone/default/reportabug?course=fopp&page=TestingClasses)
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
::: {#testing-classes .section}
[20.13. ]{.section-number}Testing classes[¶](#testing-classes "Permalink to this heading"){.headerlink}
=======================================================================================================

::: {.admonition .note}
Note

This page depends on the use of the test module, which is introduced in
[[the testing chapter]{.std
.std-ref}](../TestCases/intro-TestCases.html#test-cases-chap){.reference
.internal}. If you haven't covered that chapter yet, you will want to
delay reading this page until you do.
:::

To test a user-defined class, you will create test cases that check
whether instances are created properly, and you will create test cases
for each of the methods as functions, by invoking them on particular
instances and seeing whether they produce the correct return values and
side effects, especially side effects that change data stored in the
instance variables. To illustrate, we will use the Point class that was
used in the introduction to classes.

To test whether the class constructor (the `__init__`{.docutils .literal
.notranslate}) method is working correctly, create an instance and then
make tests to see whether its instance variables are set correctly. Note
that this is a side effect test: the constructor method's job is to set
instance variables, which is a side effect. Its return value doesn't
matter.

A method like `distanceFromOrigin`{.docutils .literal .notranslate} in
the `Point`{.docutils .literal .notranslate} class you saw does its work
by computing a return value, so it needs to be tested with a return
value test. A method like `move`{.docutils .literal .notranslate} in the
`Turtle`{.docutils .literal .notranslate} class does its work by
changing the contents of a mutable object (the point instance has its
instance variable changed) so it needs to be tested with a side effect
test.

Try adding some more tests in the code below, once you understand what's
there.

::: {.runestone .explainer .ac_section}
::: {#ac19_3_1 component="activecode" question_label="20.13.1"}
::: {#ac19_3_1_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [True]{#question19_3_1_opt_a}
-   Each test case checks whether the function works correctly on one
    input. It\'s a good idea to check several different inputs,
    including some extreme cases.
-   [False]{#question19_3_1_opt_b}
-   It\'s a good idea to check some extreme cases, as well as the
    typical cases.
:::

::: {.runestone}
-   [return value test]{#question19_3_2_opt_a}
-   The method may return the correct value but not properly change the
    values of instance variables. See the move method of the Point class
    above.
-   [side effect test]{#question19_3_2_opt_b}
-   The move method of the Point class above is a good example.
:::

::: {.runestone}
-   [return value test]{#question19_3_3_opt_a}
-   You want to check if maxabs returns the correct value for some
    input.
-   [side effect test]{#question19_3_3_opt_b}
-   The function has no side effects; even though it takes a list L as a
    parameter, it doesn\'t alter its contents.
:::

::: {.runestone}
-   [return value test]{#question19_3_4_opt_a}
-   The sort method always returns None, so there\'s nothing to check
    about whether it is returning the right value.
-   [side effect test]{#question19_3_4_opt_b}
-   You want to check whether it has the correct side effect, whether it
    correctly mutates the list.
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

-   [[](ThinkingAboutClasses.html)]{#relations-prev}
-   [[](Tamagotchi.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
