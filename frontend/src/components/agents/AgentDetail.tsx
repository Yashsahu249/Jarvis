"use client";

import { motion } from "framer-motion";
import { Bot, Clock, MessageSquare, GitBranch, ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Button } from "@/components/ui/Button";
import { Tabs } from "@/components/ui/Tabs";
import { useState } from "react";

const detailTabs = [
  { id: "tasks", label: "Tasks" },
  { id: "memory", label: "Memory" },
  { id: "comm", label: "Communication" },
];

const taskHistory = [
  { id: "1", task: "Refactored user authentication middleware", status: "completed", time: "5m ago" },
  { id: "2", task: "Generated API documentation", status: "completed", time: "15m ago" },
  { id: "3", task: "Fixed database connection pooling", status: "in-progress", time: "2m ago" },
  { id: "4", task: "Code review for PR #42", status: "pending", time: "-" },
];

export function AgentDetail() {
  const [activeTab, setActiveTab] = useState("tasks");

  return (
    <Card hoverable={false} className="flex flex-col gap-6 p-8">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => {}}>
          <ArrowLeft className="h-4 w-4" /> Back
        </Button>
        <div className="flex items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-[32px] bg-[#E0E5EC] text-accent shadow-inset-sm">
            <Bot className="h-7 w-7" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">CodeAgent</h2>
            <div className="flex items-center gap-2 text-sm text-muted">
              <Badge variant="success">Active</Badge>
              <span>Running for 2h 34m</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="flex flex-col items-center gap-1 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <MessageSquare className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">47</span>
          <span className="text-xs text-muted">Tasks Done</span>
        </div>
        <div className="flex flex-col items-center gap-1 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <GitBranch className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">12</span>
          <span className="text-xs text-muted">Active Branches</span>
        </div>
        <div className="flex flex-col items-center gap-1 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <Clock className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">89%</span>
          <span className="text-xs text-muted">Success Rate</span>
        </div>
      </div>

      <Tabs tabs={detailTabs} activeTab={activeTab} onChange={setActiveTab} />

      {activeTab === "tasks" && (
        <div className="flex flex-col gap-2">
          {taskHistory.map((t) => (
            <div
              key={t.id}
              className="flex items-center justify-between rounded-2xl bg-[#E0E5EC] p-3 transition-colors hover:bg-white/30"
            >
              <div className="flex items-center gap-3">
                <span
                  className={cn(
                    "h-2 w-2 rounded-full",
                    t.status === "completed" && "bg-[#38B2AC]",
                    t.status === "in-progress" && "bg-accent",
                    t.status === "pending" && "bg-muted",
                  )}
                />
                <span className="text-sm text-foreground">{t.task}</span>
              </div>
              <span className="text-xs text-muted">{t.time}</span>
            </div>
          ))}
        </div>
      )}

      {activeTab === "memory" && (
        <div className="flex flex-col gap-4">
          <div>
            <div className="mb-1 flex items-center justify-between text-sm">
              <span className="text-foreground">Memory Usage</span>
              <span className="text-muted">156 MB / 512 MB</span>
            </div>
            <ProgressBar value={30} variant="accent" showLabel />
          </div>
          <div className="flex flex-col gap-2 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
            <p className="text-sm font-medium text-foreground">Recent Context</p>
            <p className="text-xs text-muted">
              Stored 1,247 conversation fragments from the last 3 hours
            </p>
          </div>
        </div>
      )}

      {activeTab === "comm" && (
        <div className="flex flex-col gap-3">
          <div className="rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">BrowserAgent</span>
              <span className="text-xs text-muted">2m ago</span>
            </div>
            <p className="mt-1 text-xs text-muted">
              Sent request: "Extract data from page"
            </p>
          </div>
          <div className="rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">MemoryAgent</span>
              <span className="text-xs text-muted">5m ago</span>
            </div>
            <p className="mt-1 text-xs text-muted">
              Received: "Indexing complete - 234 new entries"
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}
