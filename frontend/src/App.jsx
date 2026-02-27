import { useState, useCallback, useEffect } from 'react'
import './index.css'

import Header from './components/Header'
import ConnectionPanel from './components/ConnectionPanel'
import QueryEditor from './components/QueryEditor'
import SafetyPanel from './components/SafetyPanel'
import SimulationPanel from './components/SimulationPanel'
import ResultsTable from './components/ResultsTable'
import QueryLogs from './components/QueryLogs'

const API = 'http://localhost:5001'

function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem('sober-theme') || 'dark')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('sober-theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark')

  // connection
  const [dbType, setDbType] = useState('sqlite')
  const [dbName, setDbName] = useState('')
  const [connected, setConnected] = useState(false)
  const [schema, setSchema] = useState(null)

  // query + results
  const [query, setQuery] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [simulation, setSimulation] = useState(null)
  const [simulating, setSimulating] = useState(false)
  const [execution, setExecution] = useState(null)
  const [executing, setExecuting] = useState(false)
  const [logs, setLogs] = useState([])
  const [error, setError] = useState(null)

  const connectDB = useCallback(async () => {
    setError(null)
    try {
      const res = await fetch(`${API}/connect-db`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ db_type: dbType, database: dbName, host: '', port: 5432, user: '', password: '' })
      })
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setConnected(true)
      setSchema(data.schema)
    } catch (e) {
      setError(e.message)
      setConnected(false)
    }
  }, [dbType, dbName])

  const simulateQuery = useCallback(async () => {
    setSimulating(true)
    try {
      const res = await fetch(`${API}/simulate-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      if (res.status >= 400 && data.error) throw new Error(data.error)
      setSimulation(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setSimulating(false)
    }
  }, [query])

  const analyzeQuery = useCallback(async () => {
    setAnalyzing(true)
    setError(null)
    setAnalysis(null)
    setSimulation(null)
    setExecution(null)
    try {
      const res = await fetch(`${API}/analyze-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      if (res.status >= 400 && data.error) throw new Error(data.error)
      setAnalysis(data)
      if (data.safe) simulateQuery()
    } catch (e) {
      setError(e.message)
    } finally {
      setAnalyzing(false)
    }
  }, [query, simulateQuery])

  const executeQuery = useCallback(async () => {
    setExecuting(true)
    setError(null)
    try {
      const res = await fetch(`${API}/execute-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      if (res.status >= 400 && data.error) throw new Error(data.error)
      setExecution(data)
      fetchLogs()
    } catch (e) {
      setError(e.message)
    } finally {
      setExecuting(false)
    }
  }, [query])

  const fetchLogs = useCallback(async () => {
    try {
      const res = await fetch(`${API}/logs`)
      const data = await res.json()
      setLogs(data.logs || [])
    } catch (e) { /* silent */ }
  }, [])

  return (
    <div className="max-w-[860px] mx-auto px-6 py-8 pb-12 font-sans">
      <Header theme={theme} onToggleTheme={toggleTheme} />

      <ConnectionPanel
        dbType={dbType}
        dbName={dbName}
        connected={connected}
        schema={schema}
        onDbTypeChange={setDbType}
        onDbNameChange={setDbName}
        onConnect={connectDB}
      />

      <QueryEditor
        query={query}
        connected={connected}
        safe={analysis?.safe}
        analyzing={analyzing}
        executing={executing}
        onChange={setQuery}
        onAnalyze={analyzeQuery}
        onExecute={executeQuery}
        onFetchLogs={fetchLogs}
      />

      {error && (
        <div className="flex items-start gap-1.5 px-3 py-2 bg-red-bg border border-red-border rounded-[5px] mb-5 text-[0.78rem] text-red">
          ⛔ {error}
        </div>
      )}

      {(analysis || simulating) && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-5">
          <SafetyPanel analysis={analysis} />
          <SimulationPanel simulation={simulation} simulating={simulating} />
        </div>
      )}

      <ResultsTable execution={execution} />
      <QueryLogs logs={logs} />

      {!analysis && !execution && logs.length === 0 && (
        <div className="text-center py-10 text-text-muted text-[0.82rem] mt-10">
          <div className="text-3xl mb-1.5 opacity-50">🛡️</div>
          {connected ? 'Write a SQL query and click Analyze to begin' : 'Connect to a database to get started'}
        </div>
      )}
    </div>
  )
}

export default App
