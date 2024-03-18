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
        Problem](/runestone/default/reportabug?course=fopp&page=week4a1)
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
::: {#chapter-assessment-list-methods .section}
[9.18. ]{.section-number}Chapter Assessment - List Methods[¶](#chapter-assessment-list-methods "Permalink to this heading"){.headerlink}
========================================================================================================================================

**Check your understanding**

::: {.runestone}
Which of these is a correct reference diagram following the execution of
the following code?

::: {.highlight-python .notranslate}
::: {.highlight}
    lst = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    lst.remove('pluto')
    first_three = lst[:3]
:::
:::

1.  

![First Potential Solution](../_images/week3a1_1.png)

2.  

![Second Potential Solution](../_images/week3a1_2.png)

I.

Yes, when we are using the remove method, we are just editing the
existing list, not making a new copy.

II\.

When we use the remove method, we just edit the existing list. We do not
make a new copy that does not include the removed object.

Neither is the correct reference diagram.

One of the diagrams is correct - look again at what is happening to lst.
:::

::: {.runestone}
-   [.pop()]{#assess_question4_1_1_2_opt_a}
-   pop removes and returns items (default is to remove and return the
    last item in the list)
-   [.insert()]{#assess_question4_1_1_2_opt_b}
-   insert will add an item at whatever position is specified.
-   [.count()]{#assess_question4_1_1_2_opt_c}
-   count returns the number of times something occurs in a list
-   [.index()]{#assess_question4_1_1_2_opt_d}
-   Yes, index will return the position of the first occurance of an
    item.
:::

::: {.runestone}
-   [.insert()]{#assess_question4_1_1_3_opt_a}
-   While you can use insert, it is not the best method to use because
    you need to specify that you want to stick the new item at the end.
-   [.pop()]{#assess_question4_1_1_3_opt_b}
-   pop removes an item from a list
-   [.append()]{#assess_question4_1_1_3_opt_c}
-   Yes, though you can use insert to do the same thing, you don\'t need
    to provide the position.
-   [.remove()]{#assess_question4_1_1_3_opt_d}
-   remove gets rid of the first occurance of any item that it is told.
    It does not add an item.
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac4_1_1_4 component="activecode" question_label="9.18.4"}
::: {#assess_ac4_1_1_4_question .ac_question}
Write code to add 'horseback riding' to the third position (i.e., right
before volleyball) in the list `sports`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac4_1_1_5 component="activecode" question_label="9.18.5"}
::: {#assess_ac4_1_1_5_question .ac_question}
Write code to take 'London' out of the list `trav_dest`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac4_1_1_6 component="activecode" question_label="9.18.6"}
::: {#assess_ac4_1_1_6_question .ac_question}
Write code to add 'Guadalajara' to the end of the list
`trav_dest`{.docutils .literal .notranslate} using a list method.
:::
:::
:::

::: {#chapter-assessment-aliases-and-references .section}
[9.18.1. ]{.section-number}Chapter Assessment - Aliases and References[¶](#chapter-assessment-aliases-and-references "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------------------------

**Check your understanding**

::: {.runestone}
::: {#assess_question3_3_1_1 component="fillintheblank" question_label="9.18.1.1" style="visibility: hidden;"}
What will be the value of `a`{.docutils .literal .notranslate} after the
following code has executed?

::: {.highlight-python .notranslate}
::: {.highlight}
    a = ["holiday", "celebrate!"]
    quiet = a
    quiet.append("company")
:::
:::

The value of `a`{.docutils .literal .notranslate} will be
:::
:::

::: {.runestone}
-   [yes]{#assess_question3_3_1_2_opt_a}
-   Yes, b and z reference the same list and changes are made using both
    aliases.
-   [no]{#assess_question3_3_1_2_opt_b}
-   Can you figure out what the value of b is only by looking at the
    lines that mention b?
:::

::: {.runestone}
-   [yes]{#assess_question3_3_1_4_opt_a}
-   Since a string is immutable, aliasing won\'t be as confusing. Beware
    of using something like item = item + new\_item with mutable objects
    though because it creates a new object. However, when we use += then
    that doesn\'t happen.
-   [no]{#assess_question3_3_1_4_opt_b}
-   Since a string is immutable, aliasing won\'t be as confusing. Beware
    of using something like item = item + new\_item with mutable objects
    though because it creates a new object. However, when we use += then
    that doesn\'t happen.
:::

::: {.runestone}
Which of these is a correct reference diagram following the execution of
the following code?

::: {.highlight-python .notranslate}
::: {.highlight}
    x = ["dogs", "cats", "birds", "reptiles"]
    y = x
    x += ['fish', 'horses']
    y = y + ['sheep']
:::
:::

1.  

![First Potential Solution](../_images/week3a3_1.png)

2.  

![Second Potential Solution](../_images/week3a3_2.png)

3.  

![Third Potential Solution](../_images/week3a3_3.png)

4.  

![Fourth Potential Solution](../_images/week3a3_4.png)

I.

When an object is concatenated with another using +=, it extends the
original object. If this is done in the longer form (item = item +
object) then it makes a copy.

II\.

When an object is concatenated with another using +=, it extends the
original object. If this is done in the longer form (item = item +
object) then it makes a copy.

III\.

When an object is concatenated with another using +=, it extends the
original object. If this is done in the longer form (item = item +
object) then it makes a copy.

IV\.

Yes, the behavior of obj = obj + object\_two is different than obj +=
object\_two when obj is a list. The first version makes a new object
entirely and reassigns to obj. The second version changes the original
object so that the contents of object\_two are added to the end of the
first.
:::
:::

::: {#chapter-assessment-split-and-join .section}
[9.18.2. ]{.section-number}Chapter Assessment - Split and Join[¶](#chapter-assessment-split-and-join "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------------------------------------------------

::: {.runestone}
Which of these is a correct reference diagram following the execution of
the following code?

::: {.highlight-python .notranslate}
::: {.highlight}
    sent = "The mall has excellent sales right now."
    wrds = sent.split()
    wrds[1] = 'store'
    new_sent = " ".join(wrds)
:::
:::

1.  

![First Potential Solution](../_images/week3a2_1.png)

2.  

![Second Potential Solution](../_images/week3a2_2.png)

3.  

![Third Potential Solution](../_images/week3a2_3.png)

4.  

![Fourth Potential Solution](../_images/week3a2_4.png)

I.

Yes, when we make our own diagrams we want to keep the old information
because sometimes other variables depend on them. It can get cluttered
though if there is a lot of information.

II\.

Not quite, we want to keep track of old information because sometimes
other variables depend on them.

III\.

Look again at what is happening when join is executed.

IV\.

What happens to the spaces in a string when it is split by whitespace?
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac_4_1_3_2 component="activecode" question_label="9.18.2.2"}
::: {#assess_ac_4_1_3_2_question .ac_question}
Write code to find the position of the string "Tony" in the list
`awards`{.docutils .literal .notranslate} and save that information in
the variable `pos`{.docutils .literal .notranslate}.
:::
:::
:::
:::

::: {#chapter-assessment-for-loop-mechanics .section}
[9.18.3. ]{.section-number}Chapter Assessment - For Loop Mechanics[¶](#chapter-assessment-for-loop-mechanics "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------------------------------

**Check your understanding**

::: {.runestone}
-   [byzo]{#assess_question5_1_1_1_opt_a}
-   This is the variable with our string, but it does not accumulate
    anything.
-   [x]{#assess_question5_1_1_1_opt_b}
-   This is the iterator variable. It changes each time but does not
    accumulate.
-   [z]{#assess_question5_1_1_1_opt_c}
-   This is a variable inside the for loop. It changes each time but
    does not accumulate or retain the old expressions that were assigned
    to it.
-   [c]{#assess_question5_1_1_1_opt_d}
-   Yes, this is the accumulator variable. By the end of the program, it
    will have a full count of how many items are in byzo.
:::

::: {.runestone}
-   [cawdra]{#assess_question5_1_1_2_opt_a}
-   Yes, this is the sequence that we iterate over.
-   [elem]{#assess_question5_1_1_2_opt_b}
-   This is the iterator variable. It changes each time but is not the
    whole sequence itself.
-   [t]{#assess_question5_1_1_2_opt_c}
-   This is the accumulator variable. By the end of the program, it will
    have a full count of how many items are in cawdra.
:::

::: {.runestone}
-   [item]{#assess_question5_1_1_3_opt_a}
-   Yes, this is the iterator variable. It changes each time but is not
    the whole sequence itself.
-   [lst]{#assess_question5_1_1_3_opt_b}
-   This is the sequence that we iterate over.
-   [num]{#assess_question5_1_1_3_opt_c}
-   This is the accumulator variable. By the end of the program, it will
    have the total value of the integers that are in lst.
:::

::: {.runestone}
::: {#assess_question5_1_1_4 component="fillintheblank" question_label="9.18.3.4" style="visibility: hidden;"}
What is the iterator (loop) variable in the following?

::: {.highlight-python .notranslate}
::: {.highlight}
    rest = ["sleep", 'dormir', 'dormire', "slaap", 'sen', 'yuxu', 'yanam']
    let = ''
    for phrase in rest:
        let += phrase[0]
:::
:::

The iterator variable is
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_week5_01 component="activecode" question_label="9.18.3.5"}
::: {#assess_week5_01_question .ac_question}
Currently there is a string called `str1`{.docutils .literal
.notranslate}. Write code to create a list called `chars`{.docutils
.literal .notranslate} which should contain the characters from
`str1`{.docutils .literal .notranslate}. Each character in
`str1`{.docutils .literal .notranslate} should be its own element in the
list `chars`{.docutils .literal .notranslate}.
:::
:::
:::
:::

::: {#chapter-assessment-accumulator-pattern .section}
[9.18.4. ]{.section-number}Chapter Assessment - Accumulator Pattern[¶](#chapter-assessment-accumulator-pattern "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------------------

**Check your understanding**

::: {.runestone}
Given that we want to accumulate the total sum of a list of numbers,
which of the following accumulator patterns would be appropriate?

1.  

::: {.highlight-python .notranslate}
::: {.highlight}
    nums = [4, 5, 2, 93, 3, 5]
    s = 0
    for n in nums:
        s = s + 1
:::
:::

2.  

::: {.highlight-python .notranslate}
::: {.highlight}
    nums = [4, 5, 2, 93, 3, 5]
    s = 0
    for n in nums:
        s = n + n
:::
:::

3.  

::: {.highlight-python .notranslate}
::: {.highlight}
    nums = [4, 5, 2, 93, 3, 5]
    s = 0
    for n in nums:
        s = s + n
:::
:::

I.

This pattern will only count how many items are in the list, not provide
the total accumulated value.

II\.

This would reset the value of s each time the for loop iterated, and so
by the end s would be assigned the value of the last item in the list
plus the last item in the list.

III\.

Yes, this will solve the problem.

none of the above would be appropriate for the problem.

One of the patterns above is a correct way to solve the problem.
:::

::: {.runestone}
Given that we want to accumulate the total number of strings in the
list, which of the following accumulator patterns would be appropriate?

1.  

::: {.highlight-python .notranslate}
::: {.highlight}
    lst = ['plan', 'answer', 5, 9.29, 'order, items', [4]]
    s = 0
    for n in lst:
        s = s + n
:::
:::

2.  

::: {.highlight-python .notranslate}
::: {.highlight}
    lst = ['plan', 'answer', 5, 9.29, 'order, items', [4]]
    for item in lst:
        s = 0
        if type(item) == type("string"):
            s = s + 1
:::
:::

3.  

::: {.highlight-python .notranslate}
::: {.highlight}
    lst = ['plan', 'answer', 5, 9.29, 'order, items', [4]]
    s = ""
    for n in lst:
        s = s + n
:::
:::

4.  

::: {.highlight-python .notranslate}
::: {.highlight}
    lst = ['plan', 'answer', 5, 9.29, 'order, items', [4]]
    s = 0
    for item in lst:
        if type(item) == type("string"):
            s = s + 1
:::
:::

1\.

How does this solution know that the element of lst is a string and that
s should be updated?

2\.

What happens to s each time the for loop iterates?

3\.

Reread the prompt again, what do we want to accumulate?

4\.

Yes, this will solve the problem.

none of the above would be appropriate for the problem.

One of the patterns above is a correct way to solve the problem.
:::

::: {.runestone}
-   [sum]{#assess_question5_2_1_3_opt_a}
-   No, though sum might be clear, it is also the name of a commonly
    used function in Python, and so there can be issues if sum is used
    as an accumulator variable.
-   [x]{#assess_question5_2_1_3_opt_b}
-   No, x is not a clear enough name to be used for an accumulator
    variable.
-   [total]{#assess_question5_2_1_3_opt_c}
-   Yes, total is a good name for accumulating numbers.
-   [accum]{#assess_question5_2_1_3_opt_d}
-   Yes, accum is a good name. It\'s both short and easy to remember.
-   [none of the above]{#assess_question5_2_1_3_opt_e}
-   At least one of the answers above is a good name for an accumulator
    variable.
:::

::: {.runestone}
-   [item]{#assess_question5_2_1_4_opt_a}
-   Yes, item can be a good name to use as an iterator variable.
-   [y]{#assess_question5_2_1_4_opt_b}
-   No, y is not likely to be a clear name for the iterator variable.
-   [elem]{#assess_question5_2_1_4_opt_c}
-   Yes, elem can be a good name to use as an iterator variable,
    especially when iterating over lists.
-   [char]{#assess_question5_2_1_4_opt_d}
-   Yes, char can be a good name to use when iterating over a string,
    because the iterator variable would be assigned a character each
    time.
-   [none of the above]{#assess_question5_2_1_4_opt_e}
-   At least one of the answers above is a good name for an iterator
    variable.
:::

::: {.runestone}
-   [num\_lst]{#assess_question5_2_1_5_opt_a}
-   Yes, num\_lst is good for a sequence variable if the value is
    actually a list of numbers.
-   [p]{#assess_question5_2_1_5_opt_b}
-   No, p is not likely to be a clear name for the iterator variable.
-   [sentence]{#assess_question5_2_1_5_opt_c}
-   Yes, this is good to use if the for loop is iterating through a
    string.
-   [names]{#assess_question5_2_1_5_opt_d}
-   Yes, names is good, assuming that the for loop is iterating through
    actual names and not something unrelated to names.
-   [none of the above]{#assess_question5_2_1_5_opt_e}
-   At least one of the answers above is a good name for a sequence
    variable
:::

::: {.runestone}
-   [accumulator variable: x \| iterator variable: s \| sequence
    variable: lst]{#assess_question5_2_1_6_opt_a}
-   Though lst is an acceptable name, x and s are not informative names
    for accumulator and iterator variables.
-   [accumulator variable: total \| iterator variable: s \| sequence
    variable: lst]{#assess_question5_2_1_6_opt_b}
-   Though total is great and lst is an acceptable name, s is a little
    bit cryptic as a variable name referring to a sentence.
-   [accumulator variable: x \| iterator variable: sentences \| sequence
    variable: sentence\_lst]{#assess_question5_2_1_6_opt_c}
-   Though sentence\_lst is a good name, the iterator variable should be
    singular rather than plural, and x is not an informative name for
    the accumulator variable.
-   [accumulator variable: total \| iterator variable: sentence
    \|sequence variable: sentence\_lst]{#assess_question5_2_1_6_opt_d}
-   Yes, this combination of variable names is the clearest.
-   [none of the above]{#assess_question5_2_1_6_opt_e}
-   One of the options above has good names for the scenario.
:::

::: {.runestone .explainer .ac_section}
::: {#access_ac_5_2_1_1 component="activecode" question_label="9.18.4.7"}
::: {#access_ac_5_2_1_1_question .ac_question}
For each character in the string saved in `ael`{.docutils .literal
.notranslate}, append that character to a list that should be saved in a
variable `app`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#access_ac_5_2_1_2 component="activecode" question_label="9.18.4.8"}
::: {#access_ac_5_2_1_2_question .ac_question}
For each string in `wrds`{.docutils .literal .notranslate}, add 'ed' to
the end of the word (to make the word past tense). Save these past tense
words to a list called `past_wrds`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps_02_06 component="activecode" question_label="9.18.4.9"}
::: {#assess_ps_02_06_question .ac_question}
Write code to create a **list of word lengths** for the words in
`original_str`{.docutils .literal .notranslate} using the accumulation
pattern and assign the answer to a variable `num_words_list`{.docutils
.literal .notranslate}. (You should use the `len`{.docutils .literal
.notranslate} function).
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_pc_02_10 component="activecode" question_label="9.18.4.10"}
::: {#assess_pc_02_10_question .ac_question}
Create an empty string and assign it to the variable `lett`{.docutils
.literal .notranslate}. Then using range, write code such that when your
code is run, `lett`{.docutils .literal .notranslate} has 7 b's
(`"bbbbbbb"`{.docutils .literal .notranslate}).
:::
:::
:::
:::

::: {#chapter-assessment-problem-solving .section}
[9.18.5. ]{.section-number}Chapter Assessment - Problem Solving[¶](#chapter-assessment-problem-solving "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------------------------

::: {.runestone .explainer .ac_section}
::: {#asign_c01_01 component="activecode" question_label="9.18.5.1"}
::: {#asign_c01_01_question .ac_question}
Below are a set of scores that students have received in the past
semester. Write code to determine how many are 90 or above and assign
that result to the value `a_scores`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#asign_c01_02 component="activecode" question_label="9.18.5.2"}
::: {#asign_c01_02_question .ac_question}
Write code that uses the string stored in `org`{.docutils .literal
.notranslate} and creates an acronym which is assigned to the variable
`acro`{.docutils .literal .notranslate}. Only the first letter of each
word should be used, each letter in the acronym should be a capital
letter, and there should be nothing to separate the letters of the
acronym. Words that should not be included in the acronym are stored in
the list `stopwords`{.docutils .literal .notranslate}. For example, if
`org`{.docutils .literal .notranslate} was assigned the string "hello to
world" then the resulting acronym should be "HW".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#asign_c01_03 component="activecode" question_label="9.18.5.3"}
::: {#asign_c01_03_question .ac_question}
Write code that uses the string stored in `sent`{.docutils .literal
.notranslate} and creates an acronym which is assigned to the variable
`acro`{.docutils .literal .notranslate}. The first two letters of each
word should be used, each letter in the acronym should be a capital
letter, and each element of the acronym should be separated by a ". "
(dot and space). Words that should not be included in the acronym are
stored in the list `stopwords`{.docutils .literal .notranslate}. For
example, if `sent`{.docutils .literal .notranslate} was assigned the
string "height and ewok wonder" then the resulting acronym should be
"HE. EW. WO".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#asign_c01_04 component="activecode" question_label="9.18.5.4"}
::: {#asign_c01_04_question .ac_question}
A palindrome is a phrase that, if reversed, would read the exact same.
Write code that checks if `p_phrase`{.docutils .literal .notranslate} is
a palindrome by reversing it and then checking if the reversed version
is equal to the original. Assign the reversed version of
`p_phrase`{.docutils .literal .notranslate} to the variable
`r_phrase`{.docutils .literal .notranslate} so that we can check your
work.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#asign_c01_05 component="activecode" question_label="9.18.5.5"}
::: {#asign_c01_05_question .ac_question}
Provided is a list of data about a store's inventory where each item in
the list represents the name of an item, how much is in stock, and how
much it costs. Print out each item in the list with the same formatting,
using the .format method (not string concatenation). For example, the
first print statment should read
`The store has 12 shoes, each for 29.99 USD.`{.docutils .literal
.notranslate}
:::
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
-   [[](../Files/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
