import { useEffect, useState } from 'react'

function App() {
  const [api, setApi] = useState('checking…')

  useEffect(() => {
    fetch('/api/health')
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.statusText))))
      .then((d: { status: string }) => setApi(d.status))
      .catch(() => setApi('unreachable'))
  }, [])

  return (
    <main>
      <h1>NOT-IN-SPEC</h1>
      <p>API: {api}</p>
    </main>
  )
}

export default App
