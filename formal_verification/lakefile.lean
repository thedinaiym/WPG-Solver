import Lake
open Lake DSL

package "wpg_project" where
  -- Настройки пакета

lean_lib «WpgProject» where
  roots := #[`WpgProject]

@[default_target]
lean_exe "wpg_main" where
  root := `Main

-- 1. Математика
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

-- 2. REPL (Инструмент для демона)
require repl from git
  "https://github.com/leanprover-community/repl.git" @ "master"
