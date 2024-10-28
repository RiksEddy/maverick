import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [apiResponse, setApiResponse] = useState<string>('')

  const callBackend = async () => {
    try {
      const response = await fetch('http://localhost:8000/')
      const data = await response.json()
      setApiResponse(data.message || JSON.stringify(data))
    } catch (error) {
      console.error('Error calling backend:', error)
      setApiResponse('Error connecting to backend')
    }
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <button onClick={callBackend} className="mt-4">
          Call Backend
        </button>
        {apiResponse && (
          <p className="mt-2">Response from backend: {apiResponse}</p>
        )}
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="text-3xl font-bold underline">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
