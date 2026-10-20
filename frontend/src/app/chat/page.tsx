'use client';

import React from 'react';
import { ChatWindow } from '@/components/ChatWindow';

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      <ChatWindow />
    </div>
  );
}
