"use client";

import { useRef, useEffect } from "react";
import { Send, Mic, Paperclip } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  onVoice?: () => void;
  onFileUpload?: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({
  value,
  onChange,
  onSend,
  onVoice,
  onFileUpload,
  disabled = false,
  placeholder = "Message Jarvis...",
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = `${Math.min(ta.scrollHeight, 200)}px`;
    }
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="flex items-end gap-2 rounded-[32px] bg-[#E0E5EC] p-2 shadow-extruded-sm">
      {onFileUpload && (
        <button
          onClick={onFileUpload}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl text-muted transition-all hover:text-foreground hover:shadow-inset-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          <Paperclip className="h-5 w-5" />
        </button>
      )}
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        rows={1}
        disabled={disabled}
        className="max-h-[200px] min-h-[44px] flex-1 resize-none bg-transparent px-3 py-2.5 text-foreground placeholder:text-[#A0AEC0] focus:outline-none"
      />
      {onVoice && (
        <button
          onClick={onVoice}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl text-muted transition-all hover:text-accent hover:shadow-inset-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          <Mic className="h-5 w-5" />
        </button>
      )}
      <button
        onClick={onSend}
        disabled={disabled || !value.trim()}
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-accent text-white shadow-extruded-sm transition-all hover:shadow-extruded-hover hover:shadow-accent/25 active:shadow-inset disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <Send className="h-5 w-5" />
      </button>
    </div>
  );
}
