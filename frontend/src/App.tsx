import { useState } from 'react'
import axios from 'axios'
import './App.css' // Можно оставить дефолтный или почистить

// Типы ответов от сервера
interface SolutionResult {
  sympy_result: boolean;
  sympy_normalized: string;
  lean_verified: boolean;
  lean_output: string;
}

function App() {
  const [word1, setWord1] = useState("a * b")
  const [word2, setWord2] = useState("b * a")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SolutionResult | null>(null)

  const handleSolve = async () => {
    setLoading(true);
    setResult(null);
    try {
      // Запрос к нашему Python Backend
      const response = await axios.post('http://127.0.0.1:8000/solve', {
        word1: word1,
        word2: word2
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error connecting to backend", error);
      alert("Ошибка соединения с сервером");
    }
    setLoading(false);
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1>🧬 WPG Solver: Hybrid Framework</h1>
      <p>Commutative (Abelian) Group Verification</p>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <div style={{ flex: 1 }}>
          <label>Word 1:</label>
          <input 
            type="text" 
            value={word1} 
            onChange={e => setWord1(e.target.value)}
            style={{ width: "100%", padding: "8px", fontSize: "1.2rem" }}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label>Word 2:</label>
          <input 
            type="text" 
            value={word2} 
            onChange={e => setWord2(e.target.value)}
            style={{ width: "100%", padding: "8px", fontSize: "1.2rem" }}
          />
        </div>
      </div>

      <button 
        onClick={handleSolve} 
        disabled={loading}
        style={{ 
          padding: "10px 20px", 
          fontSize: "1.2rem", 
          backgroundColor: loading ? "#ccc" : "#007bff", 
          color: "white", 
          border: "none", 
          cursor: "pointer" 
        }}
      >
        {loading ? "Verifying with Lean..." : "Verify Identity"}
      </button>

      {result && (
        <div style={{ marginTop: "2rem", border: "1px solid #ddd", padding: "1rem", borderRadius: "8px" }}>
          
          {/* Блок Python */}
          <div style={{ marginBottom: "1rem" }}>
            <h3>🐍 Symbolic Computation (SymPy)</h3>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              Status: 
              <span style={{ 
                fontWeight: "bold", 
                color: result.sympy_result ? "green" : "red" 
              }}>
                {result.sympy_result ? "EQUAL" : "NOT EQUAL"}
              </span>
            </div>
            <small>{result.sympy_normalized}</small>
          </div>
          
          <hr />

          {/* Блок Lean */}
          <div>
            <h3>⚖️ Formal Verification (Lean 4)</h3>
            {result.lean_verified ? (
              <div style={{ backgroundColor: "#e6fffa", padding: "10px", borderLeft: "5px solid green" }}>
                <strong style={{color: "green"}}>✅ MATHEMATICALLY PROVEN</strong>
                <pre style={{ whiteSpace: "pre-wrap", marginTop: "5px", color: "#333" }}>
                  {result.lean_output}
                </pre>
              </div>
            ) : (
              <div style={{ backgroundColor: "#fff5f5", padding: "10px", borderLeft: "5px solid red" }}>
                <strong style={{color: "red"}}>❌ PROOF FAILED</strong>
                <pre>{result.lean_output}</pre>
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  )
}

export default App