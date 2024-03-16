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
        Problem](/runestone/default/reportabug?course=fopp&page=UserDefinedClasses)
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
::: {#user-defined-classes .section}
[]{#chap-constructor}[]{#index-0}

[20.3. ]{.section-number}User Defined Classes[¶](#user-defined-classes "Permalink to this heading"){.headerlink}
================================================================================================================

We've already seen classes like `str`{.docutils .literal .notranslate},
`int`{.docutils .literal .notranslate}, `float`{.docutils .literal
.notranslate} and `list`{.docutils .literal .notranslate}. These were
defined by Python and made available for us to use. However, in many
cases when we are solving problems we need to create data objects that
are related to the problem we are trying to solve. We need to create our
own classes.

As an example, consider the concept of a mathematical point. In two
dimensions, a point is two numbers (coordinates) that are treated
collectively as a single object. Points are often written in parentheses
with a comma separating the coordinates. For example, `(0, 0)`{.docutils
.literal .notranslate} represents the origin, and `(x, y)`{.docutils
.literal .notranslate} represents the point `x`{.docutils .literal
.notranslate} units to the right and `y`{.docutils .literal
.notranslate} units up from the origin. This `(x,y)`{.docutils .literal
.notranslate} is the state of the point.

Thinking about our diagram above, we could draw a `point`{.docutils
.literal .notranslate} object as shown here.

![A point has an x and a y](../_images/objectpic2.png)

Some of the typical operations that one associates with points might be
to ask the point for its x coordinate, `getX`{.docutils .literal
.notranslate}, or to ask for its y coordinate, `getY`{.docutils .literal
.notranslate}. You would want these types of functions available to
prevent accidental changes to these instance variables since doing so
would allow you to view the values without accessing them directly. You
may also wish to calculate the distance of a point from the origin, or
the distance of a point from another point, or find the midpoint between
two points, or answer the question as to whether a point falls within a
given rectangle or circle. We'll shortly see how we can organize these
together with the data.

![A point also has methods](../_images/objectpic3.png)

Now that we understand what a `point`{.docutils .literal .notranslate}
object might look like, we can define a new **class**. We'll want our
points to each have an `x`{.docutils .literal .notranslate} and a
`y`{.docutils .literal .notranslate} attribute, so our first class
definition looks like this.

::: {.highlight-python .notranslate}
::: {.highlight}
    1class Point:
    2    """ Point class for representing and manipulating x,y coordinates. """
    3
    4    def __init__(self):
    5        """ Create a new point at the origin """
    6        self.x = 0
    7        self.y = 0
:::
:::

Class definitions can appear anywhere in a program, but they are usually
near the beginning (after the `import`{.docutils .literal .notranslate}
statements). The syntax rules for a class definition are the same as for
other compound statements. There is a header which begins with the
keyword, `class`{.docutils .literal .notranslate}, followed by the name
of the class, and ending with a colon.

If the first line after the class header is a string, it becomes the
docstring of the class, and will be recognized by various tools. (This
is also the way docstrings work in functions.)

Every class should have a method with the special name
`__init__`{.docutils .literal .notranslate}. This **initializer
method**, often referred to as the **constructor**, is automatically
called whenever a new instance of `Point`{.docutils .literal
.notranslate} is created. It gives the programmer the opportunity to set
up the attributes required within the new instance by giving them their
initial state values. The `self`{.docutils .literal .notranslate}
parameter (you could choose any other name, but nobody ever does!) is
automatically set to reference the newly created object that needs to be
initialized.

So let's use our new Point class now. This next part should look a
little familiar, if you remember some of the syntax for how we created
instances of the Turtle class, in the [[chapter on Turtle graphics]{.std
.std-ref}](../PythonTurtle/intro-HelloLittleTurtles.html#turtles-chap){.reference
.internal}.

::: {.runestone .explainer .ac_section}
::: {#chp13_classes1 component="activecode" question_label="20.3.1"}
::: {#chp13_classes1_question .ac_question}
:::
:::
:::

During the initialization of the objects, we created two attributes
called x and y for each object, and gave them both the value 0. You will
note that when you run the program, nothing happens. It turns out that
this is not quite the case. In fact, two `Points`{.docutils .literal
.notranslate} have been created, each having an x and y coordinate with
value 0. However, because we have not asked the program to do anything
with the points, we don't see any other result.

![Simple object has state and methods](../_images/objectpic4.png)

The following program adds a few print statements. You can see that the
output suggests that each one is a `Point object`{.docutils .literal
.notranslate}. However, notice that the `is`{.docutils .literal
.notranslate} operator returns `False`{.docutils .literal .notranslate}
meaning that they are different objects (we will have more to say about
this in a later section).

::: {.runestone .explainer .ac_section}
::: {#chp13_classes2 component="activecode" question_label="20.3.2"}
::: {#chp13_classes2_question .ac_question}
:::
:::
:::

A function like `Point`{.docutils .literal .notranslate} that creates a
new object instance is called a **constructor**. Every class
automatically uses the name of the class as the name of the constructor
function. The definition of the constructor function is done when you
write the `__init__`{.docutils .literal .notranslate} function (method)
inside the class definition.

It may be helpful to think of a class as a factory for making objects.
The class itself isn't an instance of a point, but it contains the
machinery to make point instances. Every time you call the constructor,
you're asking the factory to make you a new object. As the object comes
off the production line, its initialization method is executed to get
the object properly set up with it's factory default settings.

The combined process of "make me a new object" and "get its settings
initialized to the factory default settings" is called
**instantiation**.

To get a clearer understanding of what happens when instantiating a new
instance, examine the previous code using CodeLens.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="20.3.3"}
::: {#chp13_classes2a_question .ac_question}
:::

::: {#chp13_classes2a .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 20.3.3 (chp13\_classes2a)]{.runestone_caption_text}
:::
:::

At Step 2 in the CodeLens execution, you can see that `Point`{.docutils
.literal .notranslate} has been bound to an object representing the
`Point`{.docutils .literal .notranslate} class, but there are not yet
any instances. The execution of line 9, `p = Point()`{.docutils .literal
.notranslate}, occurs at steps 3-5. First, at step 3, you can see that a
blank instance of the class has been created, and is passed as the first
(and only parameter) to the `__init__`{.docutils .literal .notranslate}
method. That method's code is executed, with the variable
`self`{.docutils .literal .notranslate} bound to that instance. At steps
4 and 5, two instance variables are filled in: `x`{.docutils .literal
.notranslate} and `y`{.docutils .literal .notranslate} are both set to
`0`{.docutils .literal .notranslate}. Nothing is returned from the
`__init__`{.docutils .literal .notranslate} method, but the point object
itself is returned from the call to `Point()`{.docutils .literal
.notranslate}. Thus, at step 7, `p`{.docutils .literal .notranslate} is
bound to the new point that was created and initialized.

Skipping ahead, by the time we get to Step 14, `p`{.docutils .literal
.notranslate} and `q`{.docutils .literal .notranslate} are each bound to
different `Point`{.docutils .literal .notranslate} instances. Even
though both have `x`{.docutils .literal .notranslate} and `y`{.docutils
.literal .notranslate} instance variables set to `0`{.docutils .literal
.notranslate}, they are *different objects*. Thus `p is q`{.docutils
.literal .notranslate} evaluates to `False`{.docutils .literal
.notranslate}.
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

-   [[](ObjectsRevisited.html)]{#relations-prev}
-   [[](ImprovingourConstructor.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
