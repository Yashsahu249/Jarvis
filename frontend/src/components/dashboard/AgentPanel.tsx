"use client";

import { Bot, Activity, Cpu } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/utils";

const agents = [
  {
    name: "CodeAgent",
    status: "active",
    task: "Refactoring auth module",
    memory: 45,
  },
  {
    name: "BrowserAgent",
    status: "idle",
    task: "Awaiting instructions",
    memory: 12,
  },
  {
    name: "MemoryAgent",
    status: "active",
    task: "Indexing conversations",
    memory: 68,
  },
  {
    name: "TermAgent",
    status: "error",
    task: "Connection timeout",
    memory: 0,
  },
];

export function AgentPanel() {
  return (
    <Card className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">Active Agents</h3>
        <Badge>{agents.length} total</Badge>
      </div>
      <div className="flex flex-col gap-2">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className="flex items-center gap-3 rounded-2xl bg-[#E0E5EC] p-3 transition-colors hover:bg-white/30"
          >
            <div
              className={cn(
                "flex h-9 w-9 items-center justify-center rounded-xl",
                "bg-[#E0E5EC] shadow-inset-sm",
                agent.status === "active" && "text-[#38B2AC]",
                agent.status === "idle" && "text-muted",
                agent.status === "error" && "text-[#FC8181]",
              )}
            >
              <Bot className="h-4 w-4" />
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-foreground">
                  {agent.name}
                </span>
                <span
                  className={cn(
                    "h-2 w-2 rounded-full",
                    agent.status === "active" && "bg-[#38B2AC]",
                    agent.status === "idle" && "bg-muted",
                    agent.status === "error" && "bg-[#FC8181]",
                  )}
                />
              </div>
              <p className="truncate text-xs text-muted">{agent.task}</p>
            </div>
            <span className="text-xs text-muted">{agent.memory}%</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
