import { useEffect, useRef } from 'react'
import { useCoach } from '../hooks/useCoach'
import MessageBubble from '../components/coach/MessageBubble'
import TypingIndicator from '../components/coach/TypingIndicator'
import ChatInput from '../components/coach/ChatInput'
import BottomNav from '../components/layout/BottomNav'
import type { CoachMessage } from '../types'

const WELCOME_MESSAGE: CoachMessage = {
  role: 'assistant',
  content:
    '¡Hola! Soy tu coach personal de Habit Power. ' +
    'Puedo ayudarte a entender tu progreso, motivarte ' +
    'y darte recomendaciones para mejorar tus hábitos. ' +
    '¿En qué te puedo ayudar hoy?',
  created_at: new Date().toISOString(),
}

const SUGGESTIONS = [
  '¿Cómo voy con mis hábitos?',
  '¿Qué hábito debería priorizar?',
  'Necesito motivación hoy',
]

export default function CoachPage() {
  const { messages, isLoading, isSending, error, sendMessage, clearError } = useCoach()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending])

  const displayMessages = messages.length === 0 && !isLoading
    ? [WELCOME_MESSAGE]
    : messages

  const canRetry =
    error !== null && messages.length > 0 && messages[messages.length - 1].role === 'user'

  const handleRetry = () => {
    const lastUserMsg = messages[messages.length - 1]
    if (lastUserMsg) {
      clearError()
      sendMessage(lastUserMsg.content)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100 flex-shrink-0">
        <div className="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center text-lg">
          🤖
        </div>
        <div>
          <h1 className="text-base font-semibold text-gray-800">Coach IA</h1>
          <p className="text-xs text-gray-400">Tu entrenador personal</p>
        </div>
      </header>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 pt-4" style={{ paddingBottom: '8px' }}>
        {isLoading ? (
          <div className="flex flex-col gap-4 animate-pulse">
            {[false, true, false].map((isRight, i) => (
              <div key={i} className={`flex ${isRight ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`h-10 rounded-2xl ${isRight ? 'bg-blue-100' : 'bg-gray-100'}`}
                  style={{ width: `${[55, 65, 45][i]}%` }}
                />
              </div>
            ))}
          </div>
        ) : (
          <>
            {displayMessages.map((msg, i) => (
              <MessageBubble key={i} message={msg} />
            ))}

            {/* Quick suggestions */}
            {messages.length <= 1 && !isSending && (
              <div className="flex flex-wrap gap-2 mb-4">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => sendMessage(s)}
                    disabled={isSending}
                    className="text-sm bg-blue-50 text-blue-600 rounded-full px-3 py-1 border border-blue-200 hover:bg-blue-100 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}

            {isSending && <TypingIndicator />}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Error banner */}
      {error && (
        <div className="mx-4 mb-2 flex items-center justify-between gap-2 rounded-xl bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-600">
          <span>⚠️ {error}</span>
          {canRetry && (
            <button
              onClick={handleRetry}
              className="font-medium underline whitespace-nowrap"
            >
              Reintentar
            </button>
          )}
        </div>
      )}

      {/* Input */}
      <ChatInput onSend={sendMessage} isDisabled={isSending || isLoading} />

      {/* Bottom navigation */}
      <BottomNav />
    </div>
  )
}
