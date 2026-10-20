'use client';

import React from 'react';

export interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  isLoading?: boolean;
}

export function ChatMessage({ role, content, isLoading = false }: ChatMessageProps) {
  return (
    <div
      className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
      role="log"
      aria-label={`Mensaje del ${role === 'user' ? 'usuario' : 'asistente'}`}
    >
      <div
        className={`
          max-w-[75%] px-4 py-3 rounded-2xl
          ${role === 'user'
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-gray-100 text-gray-900 rounded-bl-md'
          }
          ${isLoading ? 'animate-pulse' : ''}
        `}
      >
        {isLoading ? (
          <div className="flex items-center gap-2 text-gray-500">
            <span className="loading-dots">●</span>
            <span className="loading-dots" style={{ animationDelay: '0.2s' }}>●</span>
            <span className="loading-dots" style={{ animationDelay: '0.4s' }}>●</span>
            <style jsx>{`
              .loading-dots {
                animation: bounce 1.4s infinite ease-in-out both;
              }
              @keyframes bounce {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
              }
            `}</style>
          </div>
        ) : (
          <p className="whitespace-pre-wrap">{content}</p>
        )}
      </div>
    </div>
  );
}