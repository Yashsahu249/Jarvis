"use client";

import { Mic, MicOff, Globe, Ear } from "lucide-react";
import { cn } from "@/lib/utils";

interface VoiceControlsProps {
  isMuted: boolean;
  onToggleMute: () => void;
  language: string;
  onLanguageChange: (lang: string) => void;
  wakeWordEnabled: boolean;
  onToggleWakeWord: () => void;
  className?: string;
}

const languages = [
  { value: "en", label: "English" },
  { value: "hi", label: "Hindi" },
  { value: "hinglish", label: "Hinglish" },
];

export function VoiceControls({
  isMuted,
  onToggleMute,
  language,
  onLanguageChange,
  wakeWordEnabled,
  onToggleWakeWord,
  className,
}: VoiceControlsProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <button
        onClick={onToggleMute}
        className={cn(
          "flex h-10 w-10 items-center justify-center rounded-2xl transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
          isMuted
            ? "bg-[#FC8181]/20 text-[#FC8181] shadow-inset-sm"
            : "bg-[#E0E5EC] text-muted shadow-extruded-sm hover:shadow-extruded-hover active:shadow-inset-sm",
        )}
      >
        {isMuted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
      </button>
      <div className="relative">
        <Globe className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
        <select
          value={language}
          onChange={(e) => onLanguageChange(e.target.value)}
          className="appearance-none rounded-2xl bg-[#E0E5EC] py-2.5 pl-10 pr-8 text-sm text-foreground shadow-inset-sm focus:shadow-inset-deep focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-[#E0E5EC]"
        >
          {languages.map((l) => (
            <option key={l.value} value={l.value}>
              {l.label}
            </option>
          ))}
        </select>
      </div>
      <button
        onClick={onToggleWakeWord}
        className={cn(
          "flex h-10 items-center gap-2 rounded-2xl px-4 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
          wakeWordEnabled
            ? "bg-accent text-white shadow-extruded-sm"
            : "bg-[#E0E5EC] text-muted shadow-inset-sm",
        )}
      >
        <Ear className="h-4 w-4" />
        <span>Wake Word</span>
      </button>
    </div>
  );
}
