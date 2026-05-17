"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, Bot, Volume2, Languages } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { WaveformVisualizer } from "./WaveformVisualizer";
import { VoiceControls } from "./VoiceControls";
import { Tooltip } from "@/components/ui/Tooltip";

const MotionButton = motion.create("button");

const transcriptions = [
  { text: "What is the weather like today?", from: "user" },
  { text: "Checking the weather for your location... It's currently 72°F and sunny in San Francisco.", from: "ai" },
];

export function VoiceInterface() {
  const [isListening, setIsListening] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [language, setLanguage] = useState("en");
  const [wakeWordEnabled, setWakeWordEnabled] = useState(true);
  const [messages, setMessages] = useState(transcriptions);

  const toggleListening = () => {
    setIsListening((p) => !p);
    if (!isListening) {
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { text: "How can I assist you today?", from: "ai" },
        ]);
      }, 2000);
    }
  };

  return (
    <div className="flex flex-col items-center gap-8 py-8">
      <Card hoverable={false} className="flex w-full max-w-2xl flex-col items-center gap-8 p-10">
        <VoiceControls
          isMuted={isMuted}
          onToggleMute={() => setIsMuted(!isMuted)}
          language={language}
          onLanguageChange={setLanguage}
          wakeWordEnabled={wakeWordEnabled}
          onToggleWakeWord={() => setWakeWordEnabled(!wakeWordEnabled)}
        />

        <div className="flex flex-col items-center gap-4">
          <Tooltip content={isListening ? "Tap to stop" : "Tap to speak"}>
            <MotionButton
              whileTap={{ scale: 0.9 }}
              onClick={toggleListening}
              className={cn(
                "relative flex h-28 w-28 items-center justify-center rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-[#E0E5EC]",
                isListening
                  ? "bg-accent text-white shadow-extruded-hover"
                  : "bg-[#E0E5EC] text-accent shadow-extruded",
              )}
            >
              <Mic className="h-10 w-10" />
              {isListening && (
                <>
                  <span className="absolute inset-0 animate-ping rounded-full bg-accent/30" />
                  <span className="absolute inset-4 animate-ping rounded-full bg-accent/20" style={{ animationDelay: "0.5s" }} />
                </>
              )}
            </MotionButton>
          </Tooltip>
          <p className="text-sm text-muted">
            {isListening ? "Listening..." : "Click to start speaking"}
          </p>
        </div>

        <WaveformVisualizer isActive={isListening} className="w-full max-w-md" />

        <div className="flex w-full flex-col gap-3">
          <AnimatePresence mode="popLayout">
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className={cn(
                  "flex items-start gap-3 rounded-2xl p-4",
                  msg.from === "user"
                    ? "bg-[#E0E5EC] shadow-extruded-sm"
                    : "bg-accent/10 shadow-inset-sm",
                )}
              >
                {msg.from === "ai" ? (
                  <Bot className="mt-0.5 h-5 w-5 shrink-0 text-accent" />
                ) : (
                  <Volume2 className="mt-0.5 h-5 w-5 shrink-0 text-muted" />
                )}
                <p
                  className={cn(
                    "text-sm",
                    msg.from === "ai" ? "text-foreground" : "text-muted",
                  )}
                >
                  {msg.text}
                </p>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        <div className="flex items-center gap-2 text-xs text-muted">
          <Languages className="h-4 w-4" />
          <span>
            {language === "en"
              ? "English"
              : language === "hi"
                ? "Hindi"
                : "Hinglish"}
          </span>
        </div>
      </Card>
    </div>
  );
}
