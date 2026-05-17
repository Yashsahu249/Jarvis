"use client";

import { MessageSquare, Database, Clock, History } from "lucide-react";
import { Card } from "@/components/ui/Card";

export function MemoryPanel() {
  return (
    <Card className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">Memory</h3>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col items-center gap-2 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <MessageSquare className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">247</span>
          <span className="text-xs text-muted">Conversations</span>
        </div>
        <div className="flex flex-col items-center gap-2 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <Database className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">84K</span>
          <span className="text-xs text-muted">Tokens</span>
        </div>
        <div className="flex flex-col items-center gap-2 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <Clock className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">3.2h</span>
          <span className="text-xs text-muted">Active Time</span>
        </div>
        <div className="flex flex-col items-center gap-2 rounded-2xl bg-[#E0E5EC] p-4 shadow-inset-sm">
          <History className="h-5 w-5 text-accent" />
          <span className="text-2xl font-bold text-foreground">12m</span>
          <span className="text-xs text-muted">Last Activity</span>
        </div>
      </div>
    </Card>
  );
}
