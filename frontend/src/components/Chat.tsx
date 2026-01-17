import { useState, useRef, useEffect } from 'react'
import './Chat.css'

interface Message {
  id: string
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

const Chat = () => {
  // Generate user avatar seed once per session for consistency
  const [userAvatarSeed] = useState(() => {
    const seeds = ['person-1', 'person-2', 'person-3', 'person-4', 'person-5']
    return seeds[Math.floor(Math.random() * seeds.length)]
  })

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m the hospital AI receptionist. Please describe your symptoms or concerns, and I\'ll help route you to the appropriate department.',
      sender: 'ai',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [lastMessageTime, setLastMessageTime] = useState<number>(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])


  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    // Debounce: prevent sending messages too quickly (300ms minimum)
    const now = Date.now()
    if (now - lastMessageTime < 300) return
    setLastMessageTime(now)

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    // Cancel previous request if it's still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()

    try {
      // Normalize API base and ensure we call the /api/chat endpoint exactly once
      const rawApiEnv = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const apiBase = rawApiEnv.replace(/\/$/, '') // drop trailing slash
      const apiRoot = apiBase.endsWith('/api') ? apiBase : `${apiBase}/api`
      const apiEndpoint = `${apiRoot}/chat`

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text,
          session_id: sessionId
        }),
        signal: abortControllerRef.current.signal
      })

      if (!response.ok) {
        // Try to read response body for debugging (limit length)
        let errText = ''
        try {
          errText = await response.text()
          if (errText.length > 500) errText = errText.slice(0, 500) + '...'
        } catch (e) {
          errText = ''
        }
        throw new Error(`Failed to send message (status ${response.status})${errText ? `: ${errText}` : ''}`)
      }

      const text = await response.text()
      let data: any = { response: text }
      try {
        data = JSON.parse(text)
      } catch (e) {
        // response was not JSON, keep raw text for debugging
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || String(data),
        sender: 'ai',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error: any) {
      // Don't show error for aborted requests
      if (error.name === 'AbortError') return
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I\'m having trouble connecting. Please try again.',
        sender: 'ai',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}
          >
            <div className="message-container">
              <div className="avatar">
                {message.sender === 'user' ? (
                  <img
                    src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${userAvatarSeed}`}
                    alt="User"
                    className="avatar-image"
                  />
                ) : (
                  <img
                    src="https://api.dicebear.com/7.x/bottts/svg?seed=ai-assistant"
                    alt="AI Assistant"
                    className="avatar-image"
                  />
                )}
              </div>
              <div className="message-content-wrapper">
                <div className="message-content">
                  {message.text}
                </div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-container">
              <div className="avatar">
                <img
                  src="https://api.dicebear.com/7.x/bottts/svg?seed=ai-assistant"
                  alt="AI Assistant"
                  className="avatar-image"
                />
              </div>
              <div className="message-content-wrapper">
                <div className="message-content typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!inputMessage.trim() || isLoading}
          className="send-button"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default Chat