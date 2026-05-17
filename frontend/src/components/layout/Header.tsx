"use client";

import { motion } from "framer-motion";
import { Menu, Monitor, Moon, Sun } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAppStore } from "@/stores/app-store";

const moduleLabels: Record<string, string> = {
  dashboard: "Dashboard",
  chat: "Chat",
  voice: "Voice Commands",
  browser: "Web Browser",
  agents: "AI Agents",
  repos: "Repositories",
  memory: "Memory Bank",
  terminal: "Terminal",
};

export default function Header() {
  const { activeModule, toggleSidebar, themeMode, setThemeMode, systemStatus } =
    useAppStore();

  const toggleTheme = () => {
    const modes: Array<"light" | "dark" | "system"> = ["light", "dark", "system"];
    const currentIndex = modes.indexOf(themeMode);
    setThemeMode(modes[(currentIndex + 1) % modes.length]);
  };

  const getThemeIcon = () => {
    switch (themeMode) {
      case "dark":
        return <Moon size={16} />;
      case "system":
        return <Monitor size={16} />;
      default:
        return <Sun size={16} />;
    }
  };

  return (
    <header className="sticky top-0 z-30 w-full h-16 bg-[#E0E5EC]/80 backdrop-blur-xl border-b border-white/20">
      <div className="flex items-center justify-between h-full px-4 lg:px-6">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="neu-button p-2.5 rounded-xl text-muted hover:text-foreground lg:hidden"
            aria-label="Toggle sidebar"
          >
            <Menu size={18} />
          </button>

          <motion.div
            key={activeModule}
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className="flex items-center gap-2"
          >
            <span className="text-muted text-sm">/</span>
            <h2 className="font-heading text-sm font-semibold text-foreground">
              {moduleLabels[activeModule] ?? activeModule}
            </h2>
          </motion.div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#E0E5EC] shadow-inset-sm text-xs text-muted">
            <span
              className={cn(
                "w-2 h-2 rounded-full",
                systemStatus.online ? "bg-green-500" : "bg-red-500"
              )}
            />
            <span>{systemStatus.online ? "Online" : "Offline"}</span>
            <span className="text-[#B0B8C4]">|</span>
            <span>CPU {systemStatus.cpu}%</span>
          </div>

          <button
            onClick={toggleTheme}
            className="neu-button p-2.5 rounded-xl text-muted hover:text-foreground"
            aria-label={`Theme: ${themeMode}`}
          >
            {getThemeIcon()}
          </button>
        </div>
      </div>
    </header>
  );
}
