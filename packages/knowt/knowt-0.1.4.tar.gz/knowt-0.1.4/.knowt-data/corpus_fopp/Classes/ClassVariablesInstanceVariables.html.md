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
        Problem](/runestone/default/reportabug?course=fopp&page=ClassVariablesInstanceVariables)
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
::: {#class-variables-and-instance-variables .section}
[]{#class-and-instance-vars}

[20.10. ]{.section-number}Class Variables and Instance Variables[¶](#class-variables-and-instance-variables "Permalink to this heading"){.headerlink}
=====================================================================================================================================================

You have already seen that each instance of a class has its own
namespace with its own instance variables. Two instances of the Point
class each have their own instance variable x. Setting x in one instance
doesn't affect the other instance.

A class can also have class variables. A class variable is set as part
of the class definition.

For example, consider the following version of the Point class. Here we
have added a graph method that generates a string representing a little
text-based graph with the Point plotted on the graph. It's not a very
pretty graph, in part because the y-axis is stretched like a rubber
band, but you can get the idea from this.

Note that there is an assignment to the variable printed\_rep on line 4.
It is not inside any method. That makes it a class variable. It is
accessed in the same way as instance variables. For example, on line 16,
there is a reference to self.printed\_rep. If you change line 4, you
have it print a different character at the x,y coordinates of the Point
in the graph.

::: {.runestone .explainer .ac_section}
::: {#classvars_1 component="activecode" question_label="20.10.1"}
::: {#classvars_1_question .ac_question}
:::
:::
:::

To be able to reason about class variables and instance variables, it is
helpful to know the rules that the python interpreter uses. That way,
you can mentally simulate what the interpreter does.

When the interpreter sees an expression of the form \<obj\>.\<varname\>, it:

:   1.  Checks if the object has an instance variable set. If so, it
        uses that value.

    2.  If it doesn't find an instance variable, it checks whether the
        class has a class variable. If so it uses that value.

    3.  If it doesn't find an instance or a class variable, it creates a
        runtime error (actually, it does one other check first, which
        you will learn about in the next chapter).

When the interpreter sees an assignment statement of the form \<obj\>.\<varname\> = \<expr\>, it:

:   1.  Evaluates the expression on the right-hand side to yield some
        python object;

    2.  Sets the instance variable \<varname\> of \<obj\> to be bound to
        that python object. Note that an assignment statement of this
        form never sets the class variable; it only sets the instance
        variable.

In order to set the class variable, you use an assignment statement of
the form \<varname\> = \<expr\> at the top-level in a class definition,
like on line 4 in the code above to set the class variable printed\_rep.

In case you are curious, method definitions also create class variables. Thus, in the code above, graph becomes a class variable that is bound to a function/method object. p1.graph() is evaluated by:

:   -   looking up p1 and finding that it's an instance of Point

    -   looking for an instance variable called graph in p1, but not
        finding one

    -   looking for a class variable called graph in p1's class, the
        Point class; it finds a function/method object

    -   Because of the () after the word graph, it invokes the
        function/method object, with the parameter self bound to the
        object p1 points to.

Try running it in codelens and see if you can follow how it all works.
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

-   [[](sorting_instances.html)]{#relations-prev}
-   [[](PrivateInstanceVariables.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
