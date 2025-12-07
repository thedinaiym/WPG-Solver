import subprocess
import os
import re
import json
import sys
import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sympy import simplify, Symbol, parse_expr, expand

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    word1: str
    word2: str

BASE_DIR = os.path.abspath("../formal_verification")

def sanitize_input(text: str) -> str:
    t = text.replace("с", "c").replace("С", "C") \
            .replace("а", "a").replace("А", "A") \
            .replace("х", "x").replace("Х", "X") \
            .replace("В", "B").replace("е", "e")
    t = t.replace("*", " * ").replace("^", " ^ ")
    return re.sub(r'\s+', ' ', t).strip()

def run_lean_atomic(lean_code: str):
    command = ["lake", "exe", "repl"]
    
    # Импорты + Код
    full_text = (
        "import Mathlib.Tactic.Abel\n"
        "import Mathlib.Algebra.Group.Basic\n"
        "set_option linter.unusedSimpArgs false\n"
        f"{lean_code}"
    )
    json_input = json.dumps({"cmd": full_text})

    print(f"🚀 [Lean] Запуск...")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            cwd=BASE_DIR,
            input=json_input, 
            text=True,        
            capture_output=True, 
            encoding='utf-8',
            timeout=180 
        )

        elapsed = time.time() - start_time
        print(f"⏱️ Время: {elapsed:.2f} сек")

        output = result.stdout.strip()
        if not output:
            print(f"⚠️ Пустой ответ! Stderr: {result.stderr}")
            return False, "System Error"

        # --- НОВЫЙ ПОСТРОЧНЫЙ ПАРСЕР ---
        # Мы не ищем JSON целиком, мы пробуем парсить каждую строку.
        # Lean часто выдает несколько JSON-ов подряд.
        
        lines = output.split('\n')
        final_success = False
        errors_found = []

        for line in lines:
            line = line.strip()
            if not line: continue
            
            try:
                data = json.loads(line)
                
                # Если видим "env", значит эта команда выполнилась успешно
                if "env" in data:
                    final_success = True
                
                # Собираем ошибки
                if "messages" in data:
                    for m in data["messages"]:
                        if m["severity"] == "error":
                            errors_found.append(m["data"])
            except:
                continue # Если строка не JSON, просто пропускаем

        if errors_found:
            print(f"❌ LEAN ERROR: {errors_found}")
            return False, f"Not Equal ({'; '.join(errors_found)})"

        if final_success:
            print("✅ УСПЕХ: Lean вернул env.")
            return True, "✅ MATHEMATICALLY PROVEN"

        return False, "Unknown Output format"

    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, f"System Error: {e}"

def prepare_lean_code(w1, w2):
    w1 = sanitize_input(w1)
    w2 = sanitize_input(w2)
    
    combined = w1 + " " + w2
    found = set(re.findall(r'[a-zA-Z]+', combined))
    # Убираем служебные слова из списка переменных
    vars = sorted(list(found - {'G', 'Type', 'CommGroup', 'example', 'by', 'simp', 'mul_comm', 'mul_assoc', 'mul_left_comm'}))
    vars_decl = " ".join(vars)
    
    # !!! МАГИЧЕСКАЯ КОМБИНАЦИЯ !!!
    # mul_comm: a*b = b*a
    # mul_assoc: (a*b)*c = a*(b*c)
    # mul_left_comm: a*(b*c) = b*(a*c)
    # Вместе они решают ВСЁ в абелевых группах.
    return f"example (G : Type) [CommGroup G] ({vars_decl} : G) : {w1} = {w2} := by simp [mul_comm, mul_assoc, mul_left_comm]"

@app.post("/solve")
async def solve(data: RequestData):
    print(f"\n📥 ЗАПРОС: {data.word1} = {data.word2}")
    
    # --- SYMPY ---
    try:
        s1 = sanitize_input(data.word1).replace("^", "**")
        s2 = sanitize_input(data.word2).replace("^", "**")
        all_vars = set(re.findall(r'[a-zA-Z]+', s1 + s2))
        local_dict = {v: Symbol(v, commutative=True) for v in all_vars}
        
        # expand() важен для раскрытия скобок
        e1 = expand(parse_expr(s1, local_dict=local_dict))
        e2 = expand(parse_expr(s2, local_dict=local_dict))
        
        diff = simplify(e1 - e2)
        print(f"🐍 SymPy Diff: {diff}")
        
        if diff == 0:
            sym_eq = True
            sym_msg = "EQUAL (Commutative)"
        else:
            sym_eq = False
            sym_msg = "NOT EQUAL"
    except Exception as e:
        print(f"⚠️ SymPy Error: {e}")
        sym_eq = False
        sym_msg = f"Error: {e}"

    # --- LEAN ---
    lean_ok, lean_msg = run_lean_atomic(prepare_lean_code(data.word1, data.word2))

    return {
        "sympy_equal": sym_eq,
        "sympy_diff": sym_msg,
        "lean_verified": lean_ok,
        "lean_log": lean_msg
    }
    