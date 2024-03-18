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
        Problem](/runestone/default/reportabug?course=fopp&page=Testingfunctions)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [18.1 Introduction: Test Cases](intro-TestCases.html){.reference
        .internal}
    -   [18.2 Checking Assumptions About Data
        Types](TestingTypes.html){.reference .internal}
    -   [18.3 Checking Other
        Assumptions](CheckingOtherAssumptions.html){.reference
        .internal}
    -   [18.4 Testing Conditionals](TestingConditionals.html){.reference
        .internal}
    -   [18.5 Testing Loops](TestingLoops.html){.reference .internal}
    -   [18.6 Writing Test Cases for
        Functions](Testingfunctions.html){.reference .internal}
    -   [18.7 Testing Optional
        Parameters](TestingOptionalParameters.html){.reference
        .internal}
    -   [18.8 👩‍💻 Test Driven
        Development](WPProgramDevelopment.html){.reference .internal}
    -   [18.9 Glossary](Glossary.html){.reference .internal}
    -   [18.10 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [18.11 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#writing-test-cases-for-functions .section}
[18.6. ]{.section-number}Writing Test Cases for Functions[¶](#writing-test-cases-for-functions "Permalink to this heading"){.headerlink}
========================================================================================================================================

It is a good idea to write one or more test cases for each function that
you define.

A function defines an operation that can be performed. If the function
takes one or more parameters, it is supposed to work properly on a
variety of possible inputs. Each test case will check whether the
function works properly on **one set of possible inputs**.

A useful function will do some combination of three things, given its
input parameters:

-   Return a value. For these, you will write **return value tests**.

-   Modify the contents of some mutable object, like a list or
    dictionary. For these you will write **side effect tests**.

-   Print something or write something to a file. Tests of whether a
    function generates the right printed output are beyond the scope of
    this testing framework; you won't write these tests.

::: {#return-value-tests .section}
[18.6.1. ]{.section-number}Return Value Tests[¶](#return-value-tests "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------

Testing whether a function returns the correct value is the easiest test
case to define. You simply check whether the result of invoking the
function on a particular input produces the particular output that you
expect. If `f`{.docutils .literal .notranslate} is your function, and
you think that it should transform inputs `x`{.docutils .literal
.notranslate} and `y`{.docutils .literal .notranslate} into output
`z`{.docutils .literal .notranslate}, then you could write a test as
`assert f(x, y) == z`{.docutils .literal .notranslate}. Or, to give a
more concrete example, if you have a function `square`{.docutils
.literal .notranslate}, you could have a test case
`assert square(3) ==  9`{.docutils .literal .notranslate}. Call this a
**return value test**.

Because each test checks whether a function works properly on specific
inputs, the test cases will never be complete: in principle, a function
might work properly on all the inputs that are tested in the test cases,
but still not work properly on some other inputs. That's where the art
of defining test cases comes in: you try to find specific inputs that
are representative of all the important kinds of inputs that might ever
be passed to the function.

The first test case that you define for a function should be an "easy"
case, one that is prototypical of the kinds of inputs the function is
supposed to handle. Additional test cases should handle "extreme" or
unusual inputs, sometimes called **edge cases**. For example, if you are
defining the "square" function, the first, easy case, might be an input
like 3. Additional extreme or unusual inputs around which you create
test cases might be a negative number, 0, and a floating point number.

One way to think about how to generate edge cases is to think in terms
of **equivalence classes** of the different kinds of inputs the function
might get. For example, the input to the `square`{.docutils .literal
.notranslate} function could be either positive or negative. We then
choose an input from each of these classes. **It is important to have at
least one test for each equivalence class of inputs.**

Semantic errors are often caused by improperly handling the boundaries
between equivalence classes. The boundary for this problem is zero. **It
is important to have a test at each boundary.**

Another way to think about edge cases is to imagine things that could go
wrong in the implementation. For example, in the square function we
might mistakenly use addition instead of multiplication. Thus, we
shouldn't rely on a test that uses 2 as input, but we might be fooled
into thinking it was working when it produced an output of 4, when it
was really doubling rather than squaring.

Try adding one or two more test cases for the square function in the
code below, based on the suggestions for edge cases.

::: {.runestone .explainer .ac_section}
::: {#ac19_2_1 component="activecode" question_label="18.6.1.1"}
::: {#ac19_2_1_question .ac_question}
:::
:::
:::
:::

::: {#side-effect-tests .section}
[18.6.2. ]{.section-number}Side Effect Tests[¶](#side-effect-tests "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------

To test whether a function makes correct changes to a mutable object,
you will need more than one line of code. You will first set the mutable
object to some value, then run the function, then check whether the
object has the expected value. Call this a **side effect test** because
you are checking to see whether the function invocation has had the
correct side effect on the mutable object.

An example follows, testing the `update_counts`{.docutils .literal
.notranslate} function (which is deliberately implemented
incorrectly...). This function takes a string called `letters`{.docutils
.literal .notranslate} and updates the counts in `counts_d`{.docutils
.literal .notranslate} that are associated with each character in the
string. To do a side effect test, we first create a dictionary with
initial counts for some letters. Then we invoke the function. Then we
test that the dictionary has the correct counts for some letters (those
correct counts are computed manually when we write the test. We have to
know what the correct answer should be in order to write a test). You
can think of it like writing a small exam for your code -- we would not
give you an exam without knowing the answers ourselves.

::: {.runestone .explainer .ac_section}
::: {#ac19_2_2 component="activecode" question_label="18.6.2.1"}
::: {#ac19_2_2_question .ac_question}
:::
:::
:::

::: {.runestone}
-   [True]{#question19_2_1_opt_a}
-   No matter how many tests you write, there may be some input that you
    didn\'t test, and the function could do the wrong thing on that
    input.
-   [False]{#question19_2_1_opt_b}
-   The tests should cover as many edge cases as you can think of, but
    there\'s always a possibility that the function does badly on some
    input that you didn\'t include as a test case.
:::

::: {.runestone}
-   [assert blanked(\'under\', \'du\', \'u\_d\_\_\') ==
    True]{#question19_1_3_opt_a}
-   blanked only takes two inputs; this provides three inputs to the
    blanked function
-   [assert blanked(\'under\', \'u\_d\_\_\') ==
    \'du\']{#question19_1_3_opt_b}
-   The second argument to the blanked function should be the letters
    that have been guessed, not the blanked version of the word
-   [assert blanked(\'under\', \'du\') ==
    \'u\_d\_\_\']{#question19_1_3_opt_c}
-   This checks whether the value returned from the blanked function is
    \'u\_d\_\_\'.
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

-   [[](TestingLoops.html)]{#relations-prev}
-   [[](TestingOptionalParameters.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
