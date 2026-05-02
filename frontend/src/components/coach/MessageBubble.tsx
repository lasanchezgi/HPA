import type { CoachMessage } from '../../types'

interface MessageBubbleProps {
  message: CoachMessage
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const time = new Date(message.created_at).toLocaleTimeString('es-CO', {
    hour: '2-digit',
    minute: '2-digit',
  })

  if (isUser) {
    return (
      <div className="flex justify-end mb-3">
        <div className="flex flex-col items-end max-w-[75%]">
          <div className="bg-blue-500 text-white rounded-2xl rounded-br-sm px-4 py-2 text-sm whitespace-pre-wrap break-words">
            {message.content}
          </div>
          <span className="text-xs text-gray-400 mt-1">{time}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-end gap-2 mb-3">
      <div className="w-7 h-7 rounded-full bg-blue-100 flex items-center justify-center text-sm flex-shrink-0">
        🤖
      </div>
      <div className="flex flex-col items-start max-w-[75%]">
        <div className="bg-gray-100 text-gray-800 rounded-2xl rounded-bl-sm px-4 py-2 text-sm whitespace-pre-wrap break-words">
          {message.content}
        </div>
        <span className="text-xs text-gray-400 mt-1">{time}</span>
      </div>
    </div>
  )
}
