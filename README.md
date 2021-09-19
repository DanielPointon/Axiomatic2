# Axiomatic2

Equation solver that generates PDFs and videos to explain maths problems to students. Includes a custom built LaTeX parser and implementation of the proof search algorithm prolog uses. See demo videos:

https://www.youtube.com/watch?v=zyGvJbNaeLA
https://www.youtube.com/watch?v=g78DdNuNKR4

Interesting bits:
* deps/algebra/functions/simplify.py
* deps/algebra/base_classes/base.py (specifically unify methods)
* deps/parser/parser.py

Uses:
* Manim
* Eel
* Python
* JavaScript


Rules are written in a list as (LHS, RHS) 
