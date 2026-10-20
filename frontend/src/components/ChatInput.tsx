'use client';

import React, { useRef, KeyboardEvent, FormEvent } from 'react';

export interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSend, disabled = false, placeholder = 'Escribe un mensaje...' }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const textarea = textareaRef.current;
    if (!textarea || !textarea.value.trim() || disabled) return;

    const message = textarea.value.trim();
    textarea.value = '';
    textarea.style.height = 'auto';
    onSend(message);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const textarea = e.currentTarget;
      if (textarea.value.trim() && !disabled) {
        const message = textarea.value.trim();
        textarea.value = '';
        textarea.style.height = 'auto';
        onSend(message);
      }
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-2 p-4 border-t border-gray-200 bg-white">
      <textarea
        ref={textareaRef}
        onKeyDown={handleKeyDown}
        onChange={handleInput}
        disabled={disabled}
        placeholder={placeholder}
        className={`
          flex-1 min-h-[44px] max-h-[120px] px-4 py-3
          border border-gray-300 rounded-2xl rounded-br-md
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
          disabled:bg-gray-100 disabled:cursor-not-allowed
          resize-none text-sm
        `}
        rows={1}
        aria-label="Mensaje para el asistente"
      />
      <button
        type="submit"
        disabled={disabled}
        className={`
          flex-shrink-0 w-10 h-10 rounded-xl
          transition-colors
          ${!disabled
            ? 'bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }
        `}
        aria-label="Enviar mensaje"
        aria-disabled={disabled}
      >
        <svg
          className="w-5 h-5 mx-auto my-auto"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          />
        </svg>
      </button>
    </form>
  );
}