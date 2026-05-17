"use client";

import { ArrowLeft, ArrowRight, RefreshCw, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

interface BrowserControlsProps {
  canGoBack: boolean;
  canGoForward: boolean;
  onBack: () => void;
  onForward: () => void;
  onRefresh: () => void;
  onNewTab: () => void;
  className?: string;
}

export function BrowserControls({
  canGoBack,
  canGoForward,
  onBack,
  onForward,
  onRefresh,
  onNewTab,
  className,
}: BrowserControlsProps) {
  return (
    <div className={cn("flex items-center gap-1", className)}>
      <button
        onClick={onBack}
        disabled={!canGoBack}
        className="flex h-9 w-9 items-center justify-center rounded-xl text-muted transition-all hover:bg-white/30 hover:text-foreground disabled:pointer-events-none disabled:opacity-30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <ArrowLeft className="h-4 w-4" />
      </button>
      <button
        onClick={onForward}
        disabled={!canGoForward}
        className="flex h-9 w-9 items-center justify-center rounded-xl text-muted transition-all hover:bg-white/30 hover:text-foreground disabled:pointer-events-none disabled:opacity-30 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <ArrowRight className="h-4 w-4" />
      </button>
      <button
        onClick={onRefresh}
        className="flex h-9 w-9 items-center justify-center rounded-xl text-muted transition-all hover:bg-white/30 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <RefreshCw className="h-4 w-4" />
      </button>
      <button
        onClick={onNewTab}
        className="flex h-9 w-9 items-center justify-center rounded-xl text-muted transition-all hover:bg-white/30 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <Plus className="h-4 w-4" />
      </button>
    </div>
  );
}
