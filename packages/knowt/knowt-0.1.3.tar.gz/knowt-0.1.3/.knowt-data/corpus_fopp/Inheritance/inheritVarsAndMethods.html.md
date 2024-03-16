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
        Problem](/runestone/default/reportabug?course=fopp&page=inheritVarsAndMethods)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [22.1 Introduction: Class Inheritance](intro.html){.reference
        .internal}
    -   [22.2 Inheriting Variables and
        Methods](inheritVarsAndMethods.html){.reference .internal}
    -   [22.3 Overriding Methods](OverrideMethods.html){.reference
        .internal}
    -   [22.4 Invoking the Parent Class's
        Method](InvokingSuperMethods.html){.reference .internal}
    -   [22.5 Multiple inheritance](MultipleInheritance.html){.reference
        .internal}
    -   [22.6 Tamagotchi Revisited](TamagotchiRevisited.html){.reference
        .internal}
    -   [22.7 Exercises](Exercises.html){.reference .internal}
    -   [22.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [22.9 Project - Wheel of Python](chapterProject.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#inheriting-variables-and-methods .section}
[22.2. ]{.section-number}Inheriting Variables and Methods[¶](#inheriting-variables-and-methods "Permalink to this heading"){.headerlink}
========================================================================================================================================

::: {#mechanics-of-defining-a-subclass .section}
[]{#index-0}

[22.2.1. ]{.section-number}Mechanics of Defining a Subclass[¶](#mechanics-of-defining-a-subclass "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------------------

We said that inheritance provides us a more elegant way of, for example,
creating `Dog`{.docutils .literal .notranslate} and `Cat`{.docutils
.literal .notranslate} types, rather than making a very complex
`Pet`{.docutils .literal .notranslate} class. In the abstract, this is
pretty intuitive: all pets have certain things, but dogs are different
from cats, which are different from birds. Going a step further, a
Collie dog is different from a Labrador dog, for example. Inheritance
provides us with an easy and elegant way to represent these differences.

Basically, it works by defining a new class, and using a special syntax
to show what the new sub-class *inherits from* a super-class. So if you
wanted to define a `Dog`{.docutils .literal .notranslate} class as a
special kind of `Pet`{.docutils .literal .notranslate}, you would say
that the `Dog`{.docutils .literal .notranslate} type inherits from the
`Pet`{.docutils .literal .notranslate} type. In the definition of the
inherited class, you only need to specify the methods and instance
variables that are different from the parent class (the **parent
class**, or the **superclass**, is what we may call the class that is
*inherited from*. In the example we're discussing, `Pet`{.docutils
.literal .notranslate} would be the superclass of `Dog`{.docutils
.literal .notranslate} or `Cat`{.docutils .literal .notranslate}).

Here is an example. Say we want to define a class `Cat`{.docutils
.literal .notranslate} that inherits from `Pet`{.docutils .literal
.notranslate}. Assume we have the `Pet`{.docutils .literal .notranslate}
class that we defined earlier.

We want the `Cat`{.docutils .literal .notranslate} type to be exactly
the same as `Pet`{.docutils .literal .notranslate}, *except* we want the
sound cats to start out knowing "meow" instead of "mrrp", and we want
the `Cat`{.docutils .literal .notranslate} class to have its own special
method called `chasing_rats`{.docutils .literal .notranslate}, which
only `Cat`{.docutils .literal .notranslate} s have.

For reference, here's the original Tamagotchi code

::: {.runestone .explainer .ac_section}
::: {#inheritance_cat_example component="activecode" question_label="22.2.1.1"}
::: {#inheritance_cat_example_question .ac_question}
:::
:::
:::

All we need is the few extra lines at the bottom of the ActiveCode
window! The elegance of inheritance allows us to specify just the
differences in the new, inherited class. In that extra code, we make
sure the `Cat`{.docutils .literal .notranslate} class inherits from the
`Pet`{.docutils .literal .notranslate} class. We do that by putting the
word Pet in parentheses, `class Cat(Pet):`{.docutils .literal
.notranslate}. In the definition of the class `Cat`{.docutils .literal
.notranslate}, we only need to define the things that are different from
the ones in the `Pet`{.docutils .literal .notranslate} class.

In this case, the only difference is that the class variable
`sounds`{.docutils .literal .notranslate} starts out with the string
`"Meow"`{.docutils .literal .notranslate} instead of the string
`"mrrp"`{.docutils .literal .notranslate}, and there is a new method
`chasing_rats`{.docutils .literal .notranslate}.

We can still use all the `Pet`{.docutils .literal .notranslate} methods
in the `Cat`{.docutils .literal .notranslate} class, this way. You can
call the `__str__`{.docutils .literal .notranslate} method on an
instance of `Cat`{.docutils .literal .notranslate} to `print`{.docutils
.literal .notranslate} an instance of `Cat`{.docutils .literal
.notranslate}, the same way you could call it on an instance of
`Pet`{.docutils .literal .notranslate}, and the same is true for the
`hi`{.docutils .literal .notranslate} method -- it's the same for
instances of `Cat`{.docutils .literal .notranslate} and `Pet`{.docutils
.literal .notranslate}. But the `chasing_rats`{.docutils .literal
.notranslate} method is special: it's only usable on `Cat`{.docutils
.literal .notranslate} instances, because `Cat`{.docutils .literal
.notranslate} is a subclass of `Pet`{.docutils .literal .notranslate}
which has that additional method.

In the original Tamagotchi game in the last chapter, you saw code that
created instances of the `Pet`{.docutils .literal .notranslate} class.
Now let's write a little bit of code that uses instances of the
`Pet`{.docutils .literal .notranslate} class AND instances of the
`Cat`{.docutils .literal .notranslate} class.

::: {.runestone .explainer .ac_section}
::: {#tamagotchi_2 component="activecode" question_label="22.2.1.2"}
::: {#tamagotchi_2_question .ac_question}
:::
:::
:::

And you can continue the inheritance tree. We inherited `Cat`{.docutils
.literal .notranslate} from `Pet`{.docutils .literal .notranslate}. Now
say we want a subclass of `Cat`{.docutils .literal .notranslate} called
`Cheshire`{.docutils .literal .notranslate}. A Cheshire cat should
inherit everything from `Cat`{.docutils .literal .notranslate}, which
means it inherits everything that `Cat`{.docutils .literal .notranslate}
inherits from `Pet`{.docutils .literal .notranslate}, too. But the
`Cheshire`{.docutils .literal .notranslate} class has its own special
method, `smile`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#inheritance_cheshire_example component="activecode" question_label="22.2.1.3"}
::: {#inheritance_cheshire_example_question .ac_question}
:::
:::
:::
:::

::: {#how-the-interpreter-looks-up-attributes .section}
[22.2.2. ]{.section-number}How the interpreter looks up attributes[¶](#how-the-interpreter-looks-up-attributes "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------------------

So what is happening in the Python interpreter when you write programs
with classes, subclasses, and instances of both parent classes and
subclasses?

**This is how the interpreter looks up attributes:**

1.  First, it checks for an instance variable or an instance method by
    the name it's looking for.

2.  If an instance variable or method by that name is not found, it
    checks for a class variable. (See the [[previous chapter]{.std
    .std-ref}](../Classes/ClassVariablesInstanceVariables.html#class-and-instance-vars){.reference
    .internal} for an explanation of the difference between **instance
    variables** and **class variables**.)

3.  If no class variable is found, it looks for a class variable in the
    parent class.

4.  If no class variable is found, the interpreter looks for a class
    variable in THAT class's parent (the "grandparent" class).

5.  This process goes on until the last ancestor is reached, at which
    point Python will signal an error.

Let's look at this with respect to some code.

Say you write the lines:

::: {.highlight-python .notranslate}
::: {.highlight}
    new_cat = Cheshire("Pumpkin")
    print(new_cat.name)
:::
:::

In the second line, after the instance is created, Python looks for the
instance variable `name`{.docutils .literal .notranslate} in the
`new_cat`{.docutils .literal .notranslate} instance. In this case, it
exists. The name on this instance of `Cheshire`{.docutils .literal
.notranslate} is `Pumpkin`{.docutils .literal .notranslate}. There you
go!

When the following lines of code are written and executed:

::: {.highlight-python .notranslate}
::: {.highlight}
    cat1 = Cat("Sepia")
    cat1.hi()
:::
:::

The Python interpreter looks for `hi`{.docutils .literal .notranslate}
in the instance of `Cat`{.docutils .literal .notranslate}. It does not
find it, because there's no statement of the form
`cat1.hi = ...`{.docutils .literal .notranslate}. (Be careful here -- if
you *had* set an instance variable on Cat called `hi`{.docutils .literal
.notranslate} it would be a bad idea, because you would not be able to
use the **method** that it inherited anymore. We'll see more about this
later.)

Then it looks for hi as a class variable (or method) in the class Cat,
and still doesn't find it.

Next, it looks for a class variable `hi`{.docutils .literal
.notranslate} on the parent class of `Cat`{.docutils .literal
.notranslate}, `Pet`{.docutils .literal .notranslate}. It finds that --
there's a **method** called `hi`{.docutils .literal .notranslate} on the
class `Pet`{.docutils .literal .notranslate}. Because of the
`()`{.docutils .literal .notranslate} after `hi`{.docutils .literal
.notranslate}, the method is invoked. All is well.

However, for the following, it won't go so well

::: {.highlight-python .notranslate}
::: {.highlight}
    p1 = Pet("Teddy")
    p1.chasing_rats()
:::
:::

The Python interpreter looks for an instance variable or method called
`chasing_rats`{.docutils .literal .notranslate} on the `Pet`{.docutils
.literal .notranslate} class. It doesn't exist. `Pet`{.docutils .literal
.notranslate} has no parent classes, so Python signals an error.

**Check your understanding**

::: {.runestone}
-   [1]{#question_inheritance_1_opt_a}
-   Neither Cheshire nor Cat defines an \_\_init\_\_ constructor method,
    so the grandaprent class, Pet, will have it\'s \_\_init\_\_ method
    called. Check how many instance variables it sets.
-   [2]{#question_inheritance_1_opt_b}
-   Neither Cheshire nor Cat defines an \_\_init\_\_ constructor method,
    so the grandaprent class, Pet, will have it\'s \_\_init\_\_ method
    called. Check how many instance variables it sets.
-   [3]{#question_inheritance_1_opt_c}
-   Neither Cheshire nor Cat defines an \_\_init\_\_ constructor method,
    so the grandaprent class, Pet, will have it\'s \_\_init\_\_ method
    called. Check how many instance variables it sets.
-   [4]{#question_inheritance_1_opt_d}
-   Neither Cheshire nor Cat defines an \_\_init\_\_ constructor method,
    so the grandaprent class, Pet, will have it\'s \_\_init\_\_ method
    called. That constructor method sets the instance variables name,
    hunger, boredom, and sounds.
:::

::: {.runestone}
-   [I am a purrrfect creature.]{#question_inheritance_2_opt_a}
-   another\_cat is an instance of Siamese, so its song() method is
    invoked.
-   [Error]{#question_inheritance_2_opt_b}
-   another\_cat is an instance of Siamese, so its song() method is
    invoked.
-   [Pumpkin]{#question_inheritance_2_opt_c}
-   This would print if the statement was print new\_cat.name.
-   [Nothing. There's no print
    statement.]{#question_inheritance_2_opt_d}
-   There is a print statement in the method definition.
:::

::: {.runestone}
-   [We are Siamese if you please. We are Siamese if you don't
    please.]{#question_inheritance_3_opt_a}
-   You cannot invoke methods defined in the Siamese class on an
    instance of the Cheshire class. Both are subclasses of Cat, but
    Cheshire is not a subclass of Siamese, so it doesn\'t inherit its
    methods.
-   [Error]{#question_inheritance_3_opt_b}
-   You cannot invoke methods defined in the Siamese class on an
    instance of the Cheshire class. Both are subclasses of Cat, but
    Cheshire is not a subclass of Siamese, so it doesn\'t inherit its
    methods.
-   [Cat1]{#question_inheritance_3_opt_c}
-   This would print if the statement was print new\_cat.name.
-   [Nothing. There's no print
    statement.]{#question_inheritance_3_opt_d}
-   There is a print statement in the method definition for Siamese.
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

-   [[](intro.html)]{#relations-prev}
-   [[](OverrideMethods.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
