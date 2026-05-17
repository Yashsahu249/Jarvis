"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  MessageSquare,
  Mic,
  Globe,
  Bot,
  FolderGit2,
  Database,
  Terminal,
  ChevronLeft,
  ChevronRight,
  Cpu,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAppStore, type ActiveModule } from "@/stores/app-store";

const navItems: { label: string; module: ActiveModule; icon: React.ReactNode }[] = [
  { label: "Dashboard", module: "dashboard", icon: <LayoutDashboard size={20} /> },
  { label: "Chat", module: "chat", icon: <MessageSquare size={20} /> },
  { label: "Voice", module: "voice", icon: <Mic size={20} /> },
  { label: "Browser", module: "browser", icon: <Globe size={20} /> },
  { label: "Agents", module: "agents", icon: <Bot size={20} /> },
  { label: "Repos", module: "repos", icon: <FolderGit2 size={20} /> },
  { label: "Memory", module: "memory", icon: <Database size={20} /> },
  { label: "Terminal", module: "terminal", icon: <Terminal size={20} /> },
];

export default function Sidebar() {
  const { sidebarOpen, activeModule, setActiveModule, toggleSidebar, systemStatus } =
    useAppStore();

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarOpen ? 240 : 72 }}
      transition={{ duration: 0.3, ease: "easeInOut" }}
      className={cn(
        "relative flex flex-col h-screen bg-[#E0E5EC] overflow-hidden",
        "border-r border-white/20 shrink-0"
      )}
    >
      <div
        className={cn(
          "flex items-center h-16 px-4",
          sidebarOpen ? "justify-between" : "justify-center"
        )}
      >
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-3"
          >
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-accent to-accent-secondary flex items-center justify-center shadow-extruded-sm">
              <Cpu size={16} className="text-white" />
            </div>
            <h1 className="font-heading text-lg font-bold text-foreground tracking-tight">
              Jarvis <span className="text-accent">OS</span>
            </h1>
          </motion.div>
        )}
        {!sidebarOpen && (
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-accent to-accent-secondary flex items-center justify-center shadow-extruded-sm">
            <Cpu size={16} className="text-white" />
          </div>
        )}
        {sidebarOpen && (
          <button
            onClick={toggleSidebar}
            className="neu-button p-1.5 rounded-xl text-muted hover:text-foreground"
            aria-label="Collapse sidebar"
          >
            <ChevronLeft size={16} />
          </button>
        )}
      </div>

      <nav className="flex-1 px-2 py-4 space-y-1.5 scrollbar-thin overflow-y-auto">
        {navItems.map((item) => {
          const isActive = activeModule === item.module;
          return (
            <button
              key={item.module}
              onClick={() => setActiveModule(item.module)}
              className={cn(
                "relative flex items-center gap-3 w-full p-3 rounded-2xl transition-all duration-200",
                isActive
                  ? "shadow-inset-sm text-accent"
                  : "shadow-extruded-sm text-muted hover:text-foreground hover:shadow-extruded-hover",
                !sidebarOpen && "justify-center p-3"
              )}
              title={!sidebarOpen ? item.label : undefined}
            >
              <span className="shrink-0">{item.icon}</span>
              {sidebarOpen && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-sm font-medium"
                >
                  {item.label}
                </motion.span>
              )}
              {isActive && sidebarOpen && (
                <motion.div
                  layoutId="activeNav"
                  className="absolute inset-0 rounded-2xl shadow-inset-sm pointer-events-none"
                  transition={{ type: "spring", stiffness: 380, damping: 30 }}
                />
              )}
            </button>
          );
        })}
      </nav>

      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="px-3 py-3 border-t border-white/20"
          >
            <div className="neu-card-inset p-3 space-y-2">
              <div className="flex items-center justify-between text-xs text-muted">
                <span>System</span>
                <span
                  className={cn(
                    "w-2 h-2 rounded-full",
                    systemStatus.online ? "bg-green-500" : "bg-red-500"
                  )}
                />
              </div>
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted">CPU</span>
                  <span className="font-medium text-foreground">
                    {systemStatus.cpu}%
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-[#D0D5DC] overflow-hidden">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-r from-accent to-accent-secondary"
                    initial={{ width: 0 }}
                    animate={{ width: `${systemStatus.cpu}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted">Memory</span>
                  <span className="font-medium text-foreground">
                    {systemStatus.memory}%
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-[#D0D5DC] overflow-hidden">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-r from-accent-secondary to-emerald-400"
                    initial={{ width: 0 }}
                    animate={{ width: `${systemStatus.memory}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </div>
              <div className="text-xs text-muted pt-1">
                Uptime: {systemStatus.uptime}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {!sidebarOpen && (
        <div className="px-2 py-3 border-t border-white/20 flex justify-center">
          <button
            onClick={toggleSidebar}
            className="neu-button p-2 rounded-xl text-muted hover:text-foreground"
            aria-label="Expand sidebar"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      )}
    </motion.aside>
  );
}
