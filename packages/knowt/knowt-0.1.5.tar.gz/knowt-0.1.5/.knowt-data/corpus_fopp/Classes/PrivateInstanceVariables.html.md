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
        Problem](/runestone/default/reportabug?course=fopp&page=PrivateInstanceVariables)
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
::: {#public-and-private-instance-variables .section}
[20.11. ]{.section-number}Public and Private Instance Variables[¶](#public-and-private-instance-variables "Permalink to this heading"){.headerlink}
===================================================================================================================================================

When we define a Python class, any instance's instance variables can be
accessed within or outside of the class. For example, suppose we have a
class named `Person`{.docutils .literal .notranslate} that represents a
person and if they are a "child" (for our purposes, anyone under 18
years old is considered a child):

::: {.runestone .explainer .ac_section}
::: {#ac20_11_1 component="activecode" question_label="20.11.1"}
::: {#ac20_11_1_question .ac_question}
:::
:::
:::

Now, suppose we hand our `Person`{.docutils .literal .notranslate} class
off to another programmer (maybe you are working as part of a team or
you are writing a library for other people to use). **They should not
need to know exactly how you implemented your class; they should just be
able to call the methods you have defined** (`getGivenName`{.docutils
.literal .notranslate}, `getFamilyName`{.docutils .literal
.notranslate}, and `isChild`{.docutils .literal .notranslate}) and get
the correct results. Ideally, you should be able to change the
implementation of your `Person`{.docutils .literal .notranslate} class
without breaking any code that uses it. For example, you might decide to
change the names of the instance variables or change how instances store
and represent information (like storing given and family names
separately). As long as the methods you have defined still work, these
changes should not make the other programmer change their code. This
idea is called **abstraction**.

However, there's a problem. The other programmer can also access
`Person`{.docutils .literal .notranslate}'s instance variables from
outside of the class definition, by writing `p1.name`{.docutils .literal
.notranslate} and `p1.age`{.docutils .literal .notranslate}, if
`p1`{.docutils .literal .notranslate} is our instance. If they do, then
they are relying on the implementation details of our class. If we
change the implementation, then their code will break. For example,
suppose we change the name of the `age`{.docutils .literal .notranslate}
instance variable to `howOld`{.docutils .literal .notranslate}. Then
their code that refers to `.age`{.docutils .literal .notranslate} will
break. Further, if the other programmer's code makes changes to the
instance variables, then they might break our code. For example, if they
change `p1.age`{.docutils .literal .notranslate} to be a string instead
of an integer, then our `isChild`{.docutils .literal .notranslate}
method will break.

These problems get more severe with larger and more complex classes. For
these reasons, it is a good idea to **hide** the implementation details
of our class from other programmers.

One way to hide implementation details is to make our instance variables
**private**, which signals to other programmers that they should not
access them directly. Unlike some other programming languages, Python
does not "enforce" the idea of private instance variables, meaning that
it is technically always possible for other programmers to reference and
modify any instance variables. However, we can use naming conventions
that (1) send a signal to other programmers that they should not access
the instance variable directly and (2) make it harder for other
programmers to access the instance variable directly.

**Single underscores:** the first way to do this is to start an instance
variable name with a single underscore (`_`{.docutils .literal
.notranslate}). In the case of `Person`{.docutils .literal
.notranslate}, we would rename our instance variables to be
`_name`{.docutils .literal .notranslate} and `_age`{.docutils .literal
.notranslate}. This signals to other programmers that they should not
access the instance variables directly. However, it is still possible
for them to do so. For example, they could write `p1._age`{.docutils
.literal .notranslate} to access the `_age`{.docutils .literal
.notranslate} instance variable. This is something they should realize
is not a good idea, but it is still possible.

**Double underscores:** The second way to do this is to start any
instance variables with a double underscore (`__`{.docutils .literal
.notranslate}). In the case of `Person`{.docutils .literal
.notranslate}, we would rename our instance variables to be
`__name`{.docutils .literal .notranslate} and `__age`{.docutils .literal
.notranslate}. As is the case with a single underscore, this is a signal
to other programmers that they should not access the instance variables
directly. Further, **Python "mangles" any instance variables that start
with two underscores to make them more difficult (but not impossible) to
access**. Python mangles these names by adding the name of the class to
the beginning of the instance variable name
(`_classname__variablename`{.docutils .literal .notranslate}). For
example, `__age`{.docutils .literal .notranslate} becomes
`_Person__age`{.docutils .literal .notranslate}. Again, it is still
possible for other programmers to do something they shouldn't, by
accessing `.__Person_age`{.docutils .literal .notranslate}, but they
have to work harder to figure out what it's called, and that may deter
them.

For example, the following code throws an error when we try to access
`p1.__age`{.docutils .literal .notranslate}:

::: {.runestone .explainer .ac_section}
::: {#ac20_11_2 component="activecode" question_label="20.11.2"}
::: {#ac20_11_2_question .ac_question}
:::
:::
:::

In the code above, we have made the `__name`{.docutils .literal
.notranslate} and `__age`{.docutils .literal .notranslate} instance
variables private. We can still access them within the class definition
using `self.__name`{.docutils .literal .notranslate} and
`self.__age`{.docutils .literal .notranslate}, but we cannot access them
directly outside of the class definition. Outside of the class
definition, if we try to access `p1.__age`{.docutils .literal
.notranslate}, we get an `AttributeError`{.docutils .literal
.notranslate}. However, we can still access `p1._Person__age`{.docutils
.literal .notranslate}.

::: {.runestone}
-   [Abstraction]{#question20_11_1_opt_a}
-   Correct! The idea of hiding implementation details of a class
    represents Abstraction.
-   [Encapsulation]{#question20_11_1_opt_b}
-   Encapsulation is closely related but it refers to the bundling of
    data with the methods that operate on that data.
-   [Inheritance]{#question20_11_1_opt_c}
-   Inheritance refers to the ability of a class to inherit properties
    and methods from another class.
-   [Polymorphism]{#question20_11_1_opt_d}
-   Polymorphism refers to the ability of an object to take many forms,
    depending on the data type or class.
:::

::: {.runestone}
-   [By making them inaccessible from outside the
    class.]{#question20_11_2_opt_a}
-   While it would be ideal to make them inaccessible, Python does not
    enforce hard restrictions.
-   [By renaming them with a single underscore.]{#question20_11_2_opt_b}
-   Correct, a single underscore signals that the variable is private
    and shouldn\'t be accessed directly, though it can still be. But
    there\'s also another way.
-   [By renaming them with a double underscore.]{#question20_11_2_opt_c}
-   Correct, a double underscore further discourages direct access by
    name mangling. But there\'s also another way.
-   [Both b and c are correct.]{#question20_11_2_opt_d}
-   Correct! Python uses both single and double underscores as
    conventions to indicate that a variable is private.
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

-   [[](ClassVariablesInstanceVariables.html)]{#relations-prev}
-   [[](ThinkingAboutClasses.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
