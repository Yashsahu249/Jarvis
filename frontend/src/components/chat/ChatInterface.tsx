"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Loader2 } from "lucide-react";
import { MessageBubble } from "./MessageBubble";
import { ChatInput } from "./ChatInput";
import { ConversationList } from "./ConversationList";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: number;
}

const initialMessages: Message[] = [
  {
    id: "0",
    role: "assistant",
    content: "Hello! I'm Jarvis. How can I help you today? I can write code, analyze data, browse the web, and much more.",
    timestamp: Date.now(),
  },
];

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [inputText, setInputText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!inputText.trim() || isStreaming) return;
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: inputText.trim(),
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText("");
    simulateResponse();
  };

  const simulateResponse = () => {
    setIsStreaming(true);
    const assistantMsg: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, assistantMsg]);

    const response =
      "I've processed your request. Here's what I found:\n\n```python\ndef hello():\n    print('Hello from Jarvis!')\n```\n\nLet me know if you need anything else!";
    let idx = 0;
    const interval = setInterval(() => {
      if (idx < response.length) {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last.role === "assistant") {
            updated[updated.length - 1] = {
              ...last,
              content: last.content + response[idx],
            };
          }
          return updated;
        });
        idx++;
      } else {
        clearInterval(interval);
        setIsStreaming(false);
      }
    }, 15);
  };

  return (
    <div className="flex h-[calc(100vh-2rem)] gap-4">
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 320, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="overflow-hidden rounded-[32px] bg-[#E0E5EC] p-4 shadow-extruded"
          >
            <ConversationList
              activeId={null}
              onSelect={() => {}}
              onDelete={() => {}}
              onNew={() => {
                setMessages(initialMessages);
              }}
            />
          </motion.div>
        )}
      </AnimatePresence>
      <div className="flex flex-1 flex-col rounded-[32px] bg-[#E0E5EC] shadow-extruded">
        <div className="flex items-center gap-3 border-b border-[#D1D5DB]/40 px-6 py-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="rounded-2xl p-2 text-muted transition-all hover:bg-white/30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            <div className="flex flex-col gap-1">
              <span className="block h-0.5 w-5 rounded-full bg-current" />
              <span className="block h-0.5 w-5 rounded-full bg-current" />
              <span className="block h-0.5 w-5 rounded-full bg-current" />
            </div>
          </button>
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-accent" />
            <span className="font-medium text-foreground">Jarvis Chat</span>
          </div>
          {isStreaming && (
            <div className="flex items-center gap-2 text-sm text-muted">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          )}
        </div>
        <div className="flex-1 overflow-y-auto scrollbar-thin px-6 py-4">
          <div className="flex flex-col gap-4">
            {messages.map((msg) => (
              <MessageBubble
                key={msg.id}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <div className="border-t border-[#D1D5DB]/40 px-6 py-4">
          <ChatInput
            value={inputText}
            onChange={setInputText}
            onSend={handleSend}
            onVoice={() => {}}
            onFileUpload={() => {}}
            disabled={isStreaming}
          />
        </div>
      </div>
    </div>
  );
}
