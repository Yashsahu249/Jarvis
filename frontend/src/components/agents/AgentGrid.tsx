"use client";

import { motion } from "framer-motion";
import { Bot, Activity, Cpu } from "lucide-react";
import { cn } from "@/lib/utils";
import { AgentCard } from "./AgentCard";

const agents = [
  { name: "CodeAgent", status: "active" as const, currentTask: "Refactoring authentication module", memoryUsage: 45 },
  { name: "BrowserAgent", status: "idle" as const, currentTask: "Awaiting instructions", memoryUsage: 12 },
  { name: "MemoryAgent", status: "active" as const, currentTask: "Indexing conversation history", memoryUsage: 68 },
  { name: "TermAgent", status: "error" as const, currentTask: "Connection timeout - retrying...", memoryUsage: 0 },
  { name: "FileAgent", status: "idle" as const, currentTask: "Monitoring file changes", memoryUsage: 8 },
  { name: "SearchAgent", status: "active" as const, currentTask: "Crawling documentation", memoryUsage: 34 },
];

export function AgentGrid() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {agents.map((agent, i) => (
        <motion.div
          key={agent.name}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.05 }}
        >
          <AgentCard
            name={agent.name}
            status={agent.status}
            currentTask={agent.currentTask}
            memoryUsage={agent.memoryUsage}
          />
        </motion.div>
      ))}
    </div>
  );
}
