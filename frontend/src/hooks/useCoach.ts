import { useState, useEffect } from 'react'
import { sendCoachMessage, getCoachHistory } from '../api/coach'
import type { CoachMessage } from '../types'

interface UseCoachReturn {
  messages: CoachMessage[]
  isLoading: boolean
  isSending: boolean
  error: string | null
  sendMessage: (text: string) => Promise<void>
  conversationId: string | null
  clearError: () => void
}

export function useCoach(): UseCoachReturn {
  const [messages, setMessages] = useState<CoachMessage[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [conversationId, setConversationId] = useState<string | null>(null)

  useEffect(() => {
    getCoachHistory()
      .then((history) => {
        setMessages(history.messages)
        setConversationId(history.conversation_id)
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Error cargando historial.')
      })
      .finally(() => setIsLoading(false))
  }, [])

  const sendMessage = async (text: string) => {
    const userMsg: CoachMessage = {
      role: 'user',
      content: text,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsSending(true)
    setError(null)

    try {
      const result = await sendCoachMessage(text)
      const assistantMsg: CoachMessage = {
        role: 'assistant',
        content: result.reply,
        created_at: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, assistantMsg])
      setConversationId(result.conversation_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setIsSending(false)
    }
  }

  const clearError = () => setError(null)

  return { messages, isLoading, isSending, error, sendMessage, conversationId, clearError }
}
