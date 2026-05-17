"use client";

import { motion } from "framer-motion";
import { Bot, Activity, Cpu, Play, Square, RotateCcw } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Button } from "@/components/ui/Button";

interface AgentCardProps {
  name: string;
  status: "active" | "idle" | "error";
  currentTask: string;
  memoryUsage: number;
  onStart?: () => void;
  onStop?: () => void;
  onRestart?: () => void;
  className?: string;
}

const MotionDiv = motion.create("div");

const statusColors = {
  active: "bg-[#38B2AC]",
  idle: "bg-muted",
  error: "bg-[#FC8181]",
};

export function AgentCard({
  name,
  status,
  currentTask,
  memoryUsage,
  onStart,
  onStop,
  onRestart,
  className,
}: AgentCardProps) {
  return (
    <Card className={cn("flex flex-col gap-4", className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <MotionDiv
            animate={status === "active" ? { rotate: [0, 360] } : {}}
            transition={
              status === "active"
                ? { duration: 3, repeat: Infinity, ease: "linear" }
                : {}
            }
            className={cn(
              "flex h-11 w-11 items-center justify-center rounded-2xl",
              "bg-[#E0E5EC] shadow-inset-sm",
              status === "active" && "text-[#38B2AC]",
              status === "idle" && "text-muted",
              status === "error" && "text-[#FC8181]",
            )}
          >
            <Bot className="h-5 w-5" />
          </MotionDiv>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-foreground">{name}</span>
              <span className={cn("h-2 w-2 rounded-full", statusColors[status])} />
            </div>
            <Badge variant={status === "error" ? "error" : status === "active" ? "success" : "default"}>
              {status}
            </Badge>
          </div>
        </div>
      </div>

      <div className="rounded-2xl bg-[#E0E5EC] p-3 shadow-inset-sm">
        <div className="flex items-center gap-2 text-sm">
          <Activity className="h-4 w-4 text-accent" />
          <span className="text-muted">{currentTask}</span>
        </div>
      </div>

      <div>
        <div className="mb-1.5 flex items-center justify-between text-xs">
          <span className="text-muted">Memory</span>
          <span className="text-foreground">{memoryUsage}%</span>
        </div>
        <ProgressBar value={memoryUsage} variant="accent" />
      </div>

      <div className="flex gap-2">
        {status !== "active" && (
          <Button size="sm" variant="primary" onClick={onStart} className="flex-1">
            <Play className="h-4 w-4" /> Start
          </Button>
        )}
        {status === "active" && (
          <Button size="sm" variant="secondary" onClick={onStop} className="flex-1">
            <Square className="h-4 w-4" /> Stop
          </Button>
        )}
        <Button size="sm" variant="ghost" onClick={onRestart}>
          <RotateCcw className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
}
