
import './App.css'
import {useState } from 'react'

const API_URL = '/api'

function App() {
  const [result, setResult] = useState('')
  const [input, setInput] = useState('')
  const [error, setError] = useState('')

  async function handleAnalyze() {
    setError('')
    setResult('')

    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ input: input })
    })
    const data=await response.json()

    if (!response.ok) {
      setError(
        typeof data.detail === 'string'
          ? data.detail
          : '입력값이 올바르지 않습니다.'
      )
      return
    }
    setResult(data.result)
  }


  return (
    <div className="container">
      <h1>SI unit 변환기 dfdfjkdfk</h1>
      <p>연산은 * / ^만 사용 가능합니다.</p>
      <input value={input} onChange={(event)=>setInput(event.target.value)} placeholder="예: N*m/s^2"/>
      <button onClick={handleAnalyze}>분석하기</button>
      {result && <p>분석 결과: {result}</p>}
      {error && <p>{error}</p>}
    </div>
  )
}

export default App
