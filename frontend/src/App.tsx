import { useState } from 'react'
import Chat from './components/Chat'
import './App.css'

function App() {
  const [key, setKey] = useState(0) // Force re-render to reset chat

  const handleNewUser = () => {
    setKey(prev => prev + 1) // This will reset the Chat component
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="header-text">
            <h1>Hospital AI Receptionist</h1>
            <p>Please describe your symptoms or concerns</p>
          </div>
          <button
            onClick={handleNewUser}
            className="new-user-header-btn"
          >
            New User
          </button>
        </div>
      </header>
      <Chat key={key} />
    </div>
  )
}

export default App