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
        Problem](/runestone/default/reportabug?course=fopp&page=AddingOtherMethodstoourClass)
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
::: {#adding-other-methods-to-a-class .section}
[20.5. ]{.section-number}Adding Other Methods to a Class[¶](#adding-other-methods-to-a-class "Permalink to this heading"){.headerlink}
======================================================================================================================================

The key advantage of using a class like `Point`{.docutils .literal
.notranslate} rather than something like a simple tuple
`(7, 6)`{.docutils .literal .notranslate} now becomes apparent. We can
add methods to the `Point`{.docutils .literal .notranslate} class that
are sensible operations for points. Had we chosen to use a tuple to
represent the point, we would not have this capability. Creating a class
like `Point`{.docutils .literal .notranslate} brings an exceptional
amount of "organizational power" to our programs, and to our thinking.
We can group together the sensible operations, and the kinds of data
they apply to, and each instance of the class can have its own state.

A **method** behaves like a function but it is invoked on a specific
instance. For example, with a list bound to variable L,
`L.append(7)`{.docutils .literal .notranslate} calls the function
append, with the list itself as the first parameter and 7 as the second
parameter. Methods are accessed using dot notation. This is why
`L.append(7)`{.docutils .literal .notranslate} has 2 parameters even
though you may think it only has one: the list stored in the variable
`L`{.docutils .literal .notranslate} is the first parameter value and 7
is the second.

Let's add two simple methods to allow a point to give us information
about its state. The `getX`{.docutils .literal .notranslate} method,
when invoked, will return the value of the x coordinate.

The implementation of this method is straight forward since we already
know how to write functions that return values. One thing to notice is
that even though the `getX`{.docutils .literal .notranslate} method does
not need any other parameter information to do its work, there is still
one formal parameter, `self`{.docutils .literal .notranslate}. As we
stated earlier, all methods defined in a class that operate on objects
of that class will have `self`{.docutils .literal .notranslate} as their
first parameter. Again, this serves as a reference to the object itself
which in turn gives access to the state data inside the object.

::: {.runestone .explainer .ac_section}
::: {#chp13_classes4 component="activecode" question_label="20.5.1"}
::: {#chp13_classes4_question .ac_question}
:::
:::
:::

Note that the `getX`{.docutils .literal .notranslate} method simply
returns the value of the instance variable x from the object self. In
other words, the implementation of the method is to go to the state of
the object itself and get the value of `x`{.docutils .literal
.notranslate}. Likewise, the `getY`{.docutils .literal .notranslate}
method looks almost the same.

Let's add another method, `distanceFromOrigin`{.docutils .literal
.notranslate}, to see better how methods work. This method will again
not need any additional information to do its work, beyond the data
stored in the instance variables. It will perform a more complex task.

::: {.runestone .explainer .ac_section}
::: {#chp13_classes5 component="activecode" question_label="20.5.2"}
::: {#chp13_classes5_question .ac_question}
:::
:::
:::

Notice that the call of `distanceFromOrigin`{.docutils .literal
.notranslate} does not *explicitly* supply an argument to match the
`self`{.docutils .literal .notranslate} parameter. This is true of all
method calls. The definition will always seem to have one additional
parameter as compared to the invocation.

**Check Your Understanding**

1.  Create a class called `Animal`{.docutils .literal .notranslate} that
    accepts two numbers as inputs and assigns them respectively to two
    instance variables: `arms`{.docutils .literal .notranslate} and
    `legs`{.docutils .literal .notranslate}. Create an instance method
    called `limbs`{.docutils .literal .notranslate} that, when called,
    returns the total number of limbs the animal has. To the variable
    name `spider`{.docutils .literal .notranslate}, assign an instance
    of `Animal`{.docutils .literal .notranslate} that has 4 arms and 4
    legs. Call the limbs method on the `spider`{.docutils .literal
    .notranslate} instance and save the result to the variable name
    `spidlimbs`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac_chp13_classes_01 component="activecode" question_label="20.5.3"}
::: {#ac_chp13_classes_01_question .ac_question}
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

-   [[](ImprovingourConstructor.html)]{#relations-prev}
-   [[](ObjectsasArgumentsandParameters.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
