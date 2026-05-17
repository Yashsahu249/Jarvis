"use client";

import { Globe, CheckCircle, XCircle, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export function BrowserPanel() {
  return (
    <Card className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">Browser</h3>
        <Badge variant="success">Active</Badge>
      </div>
      <div className="flex items-center gap-3 rounded-2xl bg-[#E0E5EC] p-3 shadow-inset-sm">
        <Globe className="h-5 w-5 text-accent" />
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-foreground">
            github.com/anomalyco/opencode
          </p>
          <p className="text-xs text-muted">Active Tab</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2 text-muted">
          <CheckCircle className="h-4 w-4 text-[#38B2AC]" />
          <span>3 tabs open</span>
        </div>
        <div className="flex items-center gap-2 text-muted">
          <RefreshCw className="h-4 w-4 text-accent" />
          <span>Auto-refresh on</span>
        </div>
      </div>
    </Card>
  );
}
