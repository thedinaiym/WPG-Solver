import Lake
open Lake DSL

package "wpg_project" where
  -- Настройки пакета

lean_lib «WpgProject» where
  -- Мы указываем, что библиотека лежит в папке WpgProject
  roots := #[`WpgProject]

@[default_target]
lean_exe "wpg_main" where
  -- Точка входа в программу (файл Main.lean)
  root := `Main

-- Библиотека математики
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
