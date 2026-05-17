"use client";

import { Cpu, MemoryStick, Brain, Activity } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Badge } from "@/components/ui/Badge";

export function SystemPanel() {
  return (
    <Card className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">System</h3>
        <Badge variant="success">Online</Badge>
      </div>
      <div className="grid gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-inset-sm">
            <Cpu className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">CPU</span>
              <span className="text-muted">32%</span>
            </div>
            <ProgressBar value={32} variant="accent" className="mt-1.5" />
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-inset-sm">
            <MemoryStick className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">Memory</span>
              <span className="text-muted">4.2/16 GB</span>
            </div>
            <ProgressBar value={26} variant="secondary" className="mt-1.5" />
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-inset-sm">
            <Brain className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">Model</span>
              <span className="text-muted">Claude 3.5 Sonnet</span>
            </div>
            <p className="mt-0.5 text-xs text-muted">Context: 78K / 200K tokens</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-inset-sm">
            <Activity className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground">Active Tasks</span>
              <span className="text-muted">3 running</span>
            </div>
            <p className="mt-0.5 text-xs text-muted">Uptime: 12h 34m</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
