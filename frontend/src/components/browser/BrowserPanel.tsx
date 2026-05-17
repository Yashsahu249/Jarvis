"use client";

import { useState } from "react";
import { Globe, Play, Square, Search, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Toggle } from "@/components/ui/Toggle";
import { Tabs } from "@/components/ui/Tabs";
import { Badge } from "@/components/ui/Badge";
import { BrowserControls } from "./BrowserControls";
import { BrowserViewport } from "./BrowserViewport";
import { BrowserLogs } from "./BrowserLogs";

const tabs = [
  { id: "view", label: "Viewport" },
  { id: "logs", label: "Logs" },
  { id: "queue", label: "Queue" },
];

export function BrowserPanel() {
  const [isRunning, setIsRunning] = useState(true);
  const [activeTab, setActiveTab] = useState("view");
  const [url, setUrl] = useState("https://github.com");

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Globe className="h-6 w-6 text-accent" />
          <h2 className="text-xl font-bold text-foreground">Browser Automation</h2>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant={isRunning ? "success" : "default"}>
            {isRunning ? "Running" : "Stopped"}
          </Badge>
          <Toggle enabled={isRunning} onChange={setIsRunning} />
        </div>
      </div>

      <Card hoverable={false} className="flex flex-col gap-4 p-6">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Globe className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter URL..."
              className="w-full rounded-2xl bg-[#E0E5EC] py-2.5 pl-10 pr-4 text-sm text-foreground shadow-inset-sm placeholder:text-[#A0AEC0] focus:shadow-inset-deep focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-[#E0E5EC]"
            />
          </div>
          <BrowserControls
            canGoBack
            canGoForward
            onBack={() => {}}
            onForward={() => {}}
            onRefresh={() => {}}
            onNewTab={() => {}}
          />
        </div>

        <Tabs
          tabs={tabs}
          activeTab={activeTab}
          onChange={setActiveTab}
        />

        {activeTab === "view" && (
          <BrowserViewport url={url} className="h-[500px]" />
        )}
        {activeTab === "logs" && <BrowserLogs />}
        {activeTab === "queue" && (
          <div className="flex flex-col items-center gap-4 py-12 text-muted">
            <Search className="h-12 w-12" />
            <p className="text-sm">Task queue is empty</p>
          </div>
        )}
      </Card>
    </div>
  );
}
