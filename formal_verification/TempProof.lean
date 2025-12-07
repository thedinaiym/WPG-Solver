
import Mathlib.Tactic.Abel
import Mathlib.Algebra.Group.Basic

example {G : Type*} [CommGroup G] (a b : G) : 
  a * b = b * a := by
  abel
