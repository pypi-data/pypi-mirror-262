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
        Problem](/runestone/default/reportabug?course=fopp&page=WPAccumulatorPatternStrategies)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [9.1 Introduction: Transforming
        Sequences](intro-SequenceMutation.html){.reference .internal}
    -   [9.2 Mutability](Mutability.html){.reference .internal}
    -   [9.3 List Element Deletion](ListDeletion.html){.reference
        .internal}
    -   [9.4 Objects and
        References](ObjectsandReferences.html){.reference .internal}
    -   [9.5 Aliasing](Aliasing.html){.reference .internal}
    -   [9.6 Cloning Lists](CloningLists.html){.reference .internal}
    -   [9.7 Mutating Methods](MutatingMethods.html){.reference
        .internal}
    -   [9.8 Append versus
        Concatenate](AppendversusConcatenate.html){.reference .internal}
    -   [9.9 Non-mutating Methods on
        Strings](NonmutatingMethodsonStrings.html){.reference .internal}
    -   [9.10 String Format Method](StringFormatting.html){.reference
        .internal}
    -   [9.11 f-Strings](FStrings.html){.reference .internal}
    -   [9.12 The Accumulator Pattern with
        Lists](TheAccumulatorPatternwithLists.html){.reference
        .internal}
    -   [9.13 The Accumulator Pattern with
        Strings](TheAccumulatorPatternwithStrings.html){.reference
        .internal}
    -   [9.14 👩‍💻 Accumulator Pattern
        Strategies](WPAccumulatorPatternStrategies.html){.reference
        .internal}
    -   [9.15 👩‍💻 Don't Mutate A List That You Are Iterating
        Through](WPDontMutateAListYouIterateThrough.html){.reference
        .internal}
    -   [9.16 Summary](Glossary.html){.reference .internal}
    -   [9.17 Exercises](Exercises.html){.reference .internal}
    -   [9.18 Chapter Assessment - List
        Methods](week4a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#accumulator-pattern-strategies .section}
[9.14. ]{.section-number}👩‍💻 Accumulator Pattern Strategies[¶](#accumulator-pattern-strategies "Permalink to this heading"){.headerlink}
========================================================================================================================================

::: {#when-to-use-it .section}
[9.14.1. ]{.section-number}When to Use it[¶](#when-to-use-it "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------

When children first encounter word problems in their math classes, they
find it difficult to translate those words into arithmetic expressions
involving addition, subtraction, multiplication, and division. Teachers
offer heuristics. If the problem says "how many...altogether", that's an
addition problem. If it says "how many are left", that's going to be a
subtraction problem.

Learning to use the accumulator pattern can be similarly confusing. The
first step is to recognizing something in the problem statement that
suggests an accumulation pattern. Here are a few. You might want to try
adding some more of your own.

Phrase
:::
:::
:::

Accumulation Pattern

how many

count accumulation

how frequently

total

sum accumulation

a list of

list accumulation

concatenate

string accumulation

join together

For example, if the problem is to compute the total distance traveled in
a series of small trips, you would want to accumulate a sum. If the
problem is to make a list of the cubes of all the numbers from 1-25, you
want a list accumulation, starting with an empty list and appending one
more cube each time. If the problem is to make a comma separated list of
all the people invited to a party, you should think of concatenating
them; you could start with an empty string and concatenate one more
person on each iteration through a list of name.

::: {#before-writing-it .section}
[9.14.2. ]{.section-number}Before Writing it[¶](#before-writing-it "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------

Before writing any code, we recommend that you first answer the
following questions:

-   What sequence will you iterate through as you accumulate a result?
    It could be a range of numbers, the letters in a string, or some
    existing list that you have just as a list of names.

-   What type of value will you accumulate? If your final result will be
    a number, your accumulator will start out with a number and always
    have a number even as it is updated each time. Similarly, if your
    final result will be a list, start with a list. If your final result
    will be a string, you'll probably want to start with a string; one
    other option is to accumulate a list of strings and then use the
    .join() method at the end to concatenate them all together.

We recommend writing your answers to these questions in a comment. As
you encounter bugs and have to look things up, it will help remind you
of what you were trying to implement. Sometimes, just writing the
comment can help you to realize a potential problem and avoid it before
you ever write any code.
:::

::: {#choosing-good-accumulator-and-iterator-variable-names .section}
[9.14.3. ]{.section-number}Choosing Good Accumulator and Iterator Variable Names[¶](#choosing-good-accumulator-and-iterator-variable-names "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The final piece of advice regarding accumulation strategies is to be
intentional when choosing variable names for the accumulator and
iterator variables. A good name can help remind you of what the value is
assigned to the variable as well as what you should have by the end of
your code. While it might be tempting at first to use a short variable
name, such as `a`{.docutils .literal .notranslate} or `x`{.docutils
.literal .notranslate}, if you run into any bugs or look at your code
later, you may have trouble understanding what you intended to do and
what your code is actually doing.

For the accumulator variable, one thing that can help is to make the
variable name end with "so\_far". The prefix can be something that helps
remind you of what you're supposed to end up with. For example:
count\_so\_far, total\_so\_far, or cubes\_so\_far.

As mentioned previously in a previous Way of the Programmer segment,
[[👩‍💻 Naming Variables in For Loops]{.std
.std-ref}](../Iteration/WPNamingVariablesinForLoops.html#naming-variables-in-for-loops){.reference
.internal}, the iterator variable should be a singular noun. It should
describe what one item in the original sequence, not what one item in
the final result will be. For example, when accumulating the cubes of
the numbers from 1-25, don't write for cube in range(25):. Instead,
write for num in range(25):. If you name the iterator variable cube you
run the risk of getting confused that it has already been cubed, when
that's an operation that you still have to write in your code.

**Check Your Understanding**

::: {.runestone}
-   [Yes; \"save\... to a list\"]{#question8_11_1_opt_a}
-   Correct!
-   [Yes; \"add \'ed\' to the end of the word\"]{#question8_11_1_opt_b}
-   Not quite - these words don\'t necessarily mean that we want to
    accumulate the new strings into a new variable.
-   [No]{#question8_11_1_opt_c}
-   In this case, an accumulation pattern would be good to use!
:::

::: {.runestone}
-   [Yes; \"to sum up\"]{#question8_11_2_opt_a}
-   Correct!
-   [Yes; \"numbers in the list\"]{#question8_11_2_opt_b}
-   Not quite - these words don\'t necessarily mean that we want to do
    sum accumulation.
-   [No]{#question8_11_2_opt_c}
-   In this case, an accumulation pattern would be good to use!
:::

::: {.runestone}
-   [Yes; \"print out each\"]{#question8_11_3_opt_a}
-   Incorrect, this prompt does not need to use the accumulation
    pattern.
-   [Yes; \"on a separate line\"]{#question8_11_3_opt_b}
-   Incorrect, this prompt does not need to use the accumulation
    pattern.
-   [No]{#question8_11_3_opt_c}
-   Correct!
:::

::: {.runestone}
-   [Yes; \"vowels in the sentence\"]{#question8_11_4_opt_a}
-   Not quite - these words don\'t necessarily mean that we want to do
    sum accumulation.
-   [Yes; \"code that will count\"]{#question8_11_4_opt_b}
-   Correct!
-   [No]{#question8_11_4_opt_c}
-   In this case, an accumulation pattern would be good to use!
:::

::: {.runestone}
-   [string]{#question8_11_5_opt_a}
-   Incorrect, that is not the best type for the accumulator variable.
-   [list]{#question8_11_5_opt_b}
-   Incorrect, that is not the best type for the accumulator variable.
-   [integer]{#question8_11_5_opt_c}
-   Yes, because we want to keep track of a number.
-   [none, there is no accumulator variable.]{#question8_11_5_opt_d}
-   Incorrect, we will need an accumulator variable.
:::

::: {.runestone}
-   [num\_vowels]{#question8_11_6_opt_a}
-   No, that is the accumulator variable.
-   [s]{#question8_11_6_opt_b}
-   Yes, that is the sequence you will iterate through!
-   [the prompt does not say]{#question8_11_6_opt_c}
-   It is stated in the prompt.
:::

::: {.runestone}
-   [string]{#question8_11_7_opt_a}
-   Incorrect, that is not the best type for the accumulator variable.
-   [list]{#question8_11_7_opt_b}
-   Yes, because we want a new list at the end of the code.
-   [integer]{#question8_11_7_opt_c}
-   Incorrect, that is not the best type for the accumulator variable.
-   [none, there is no accumulator variable.]{#question8_11_7_opt_d}
-   Incorrect, we will need an accumulator variable.
:::

::: {.runestone}
-   [wrds]{#question8_11_8_opt_a}
-   Yes, that is the sequence you will iterate through!
-   [past\_wrds]{#question8_11_8_opt_b}
-   No, that is the accumulator variable.
-   [the prompt does not say]{#question8_11_8_opt_c}
-   It is stated in the prompt.
:::

::: {.runestone}
-   [string]{#question8_11_9_opt_a}
-   Incorrect, that is not the best type for the accumulator variable.
-   [list]{#question8_11_9_opt_b}
-   Incorrect, that is not the best type for the accumulator variable.
-   [integer]{#question8_11_9_opt_c}
-   Yes, because we want to keep track of a number.
-   [none, there is no accumulator variable.]{#question8_11_9_opt_d}
-   Incorrect, we will need an accumulator variable.
:::

::: {.runestone}
-   [seat\_counts]{#question8_11_10_opt_a}
-   Yes, that is the sequence you will iterate through!
-   [total\_seat\_counts]{#question8_11_10_opt_b}
-   No, that is the accumulator variable.
-   [the prompt does not say]{#question8_11_10_opt_c}
-   It is stated in the prompt.
:::

::: {.runestone}
-   [string]{#question8_11_11_opt_a}
-   Incorrect, there should not be an accumulator variable.
-   [list]{#question8_11_11_opt_b}
-   Incorrect, there should not be an accumulator variable.
-   [integer]{#question8_11_11_opt_c}
-   Incorrect, there should not be an accumulator variable.
-   [none, there is no accumulator variable.]{#question8_11_11_opt_d}
-   Correct, because this prompt does not suggest an accumulator pattern
:::

::: {.runestone}
-   [my\_str]{#question8_11_12_opt_a}
-   Yes, that is the sequence you will iterate through!
-   [my\_str.split()]{#question8_11_12_opt_b}
-   Close, but read the prompt again - did it say to iterate through
    words?
-   [the prompt does not say]{#question8_11_12_opt_c}
-   It is stated in the prompt.
:::

::: {.runestone}
-   [Accumulator Variable: wrds\_so\_far ; Iterator Variable:
    wrd]{#question8_11_13_opt_a}
-   Yes, this is the most clear combination of accumulator and iterator
    variables.
-   [Accumulator Variable: wrds\_so\_far ; Iterator Variable:
    x]{#question8_11_13_opt_b}
-   The iterator variable is not the clearest here, something else may
    be better.
-   [Accumulator Variable: changed\_wrds ; Iterator Variable:
    ed]{#question8_11_13_opt_c}
-   The iterator variable is not the clearest here
:::

::: {.runestone}
-   [Accumulator Variable: count\_so\_far ; Iterator Variable:
    l]{#question8_11_14_opt_a}
-   Though the accumulator variable is good, the iterator variable is
    not very clear.
-   [Accumulator Variable: total\_so\_far ; Iterator Variable:
    letter]{#question8_11_14_opt_b}
-   Yes! Both the accumulator and iterator variable are clear.
-   [Accumulator Variable: n\_v ; Iterator Variable:
    letter]{#question8_11_14_opt_c}
-   Though the iterator variable is good, the accumulator variable is
    not very clear.
:::

::: {.runestone}
-   [Accumulator Variable: total\_so\_far ; Iterator Variable:
    seat]{#question8_11_15_opt_a}
-   Though the accumulator variable is good, the iterator variable is
    not clear enough.
-   [Accumulator Variable: total\_seats\_so\_far ; Iterator Variable:
    seat\_count]{#question8_11_15_opt_b}
-   Yes, this is the most clear combination.
-   [Accumulator Variable: count ; Iterator Variable:
    n]{#question8_11_15_opt_c}
-   Neither the accumulator nor iterator variable are clear enough. The
    accumulator variable is better, but could be more clear.
:::

::: {.runestone}
-   [Accumulator Variable: character\_so\_far ; Iterator Variable:
    char]{#question8_11_16_opt_a}
-   Incorrect, there is no accumulator variable neccessary
-   [Accumulator Variable: no variable needed ; Iterator Variable:
    c]{#question8_11_16_opt_b}
-   Though no accumulator variable is needed, the iterator variable is
    not clear enough
-   [Accumulator Variable: no variable needed ; Iterator Variable:
    char]{#question8_11_16_opt_c}
-   Yes, there is no accumulator variable needed and the iterator
    variable is clear (char is a common short form of character)
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

-   [[](TheAccumulatorPatternwithStrings.html)]{#relations-prev}
-   [[](WPDontMutateAListYouIterateThrough.html)]{#relations-next}

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
