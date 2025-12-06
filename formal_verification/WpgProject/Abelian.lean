import Mathlib.Algebra.Group.Basic
import Mathlib.Tactic.Ring

-- Объявляем пространство имен (чтобы не путаться)
namespace Wpg.Abelian

-- ТЕОРЕМА: В коммутативной группе (a * b)^2 = a^2 * b^2
-- Python пришлет нам утверждение, а Lean его проверит.
theorem square_mul_comm {G : Type*} [CommGroup G] (a b : G) :
  (a * b)^2 = a^2 * b^2 := by
  -- Это магия Lean. Тактика 'group' умеет решать такие равенства.
  group

end Wpg.Abelian
