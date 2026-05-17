"use client";

import { Globe, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";

interface BrowserViewportProps {
  url?: string;
  screenshot?: string;
  className?: string;
}

export function BrowserViewport({
  url = "https://example.com",
  screenshot,
  className,
}: BrowserViewportProps) {
  return (
    <div
      className={cn(
        "flex flex-col overflow-hidden rounded-[32px] bg-[#E0E5EC] shadow-inset-sm",
        className,
      )}
    >
      <div className="flex items-center gap-2 border-b border-[#D1D5DB]/40 px-4 py-2">
        <Globe className="h-4 w-4 text-accent" />
        <span className="truncate text-sm text-muted">{url}</span>
        <ExternalLink className="h-3.5 w-3.5 shrink-0 text-muted" />
      </div>
      <div className="flex flex-1 items-center justify-center bg-white/50 p-8">
        {screenshot ? (
          <img
            src={screenshot}
            alt="Page screenshot"
            className="h-full w-full rounded-2xl object-contain shadow-extruded-sm"
          />
        ) : (
          <div className="flex flex-col items-center gap-3 text-muted">
            <Globe className="h-12 w-12" />
            <p className="text-sm">Page preview will appear here</p>
          </div>
        )}
      </div>
    </div>
  );
}
