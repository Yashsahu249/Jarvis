"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  FileText,
  Globe,
  Code,
  Terminal,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";

interface Activity {
  id: string;
  type: "chat" | "file" | "browse" | "code" | "command";
  message: string;
  timestamp: Date;
}

const activityIcons: Record<Activity["type"], LucideIcon> = {
  chat: Bot,
  file: FileText,
  browse: Globe,
  code: Code,
  command: Terminal,
};

const recentActivities: Activity[] = [
  { id: "1", type: "chat", message: "Responded to user query about Python", timestamp: new Date(Date.now() - 1000 * 30) },
  { id: "2", type: "code", message: "Generated authentication middleware", timestamp: new Date(Date.now() - 1000 * 120) },
  { id: "3", type: "browse", message: "Scraped documentation from React.dev", timestamp: new Date(Date.now() - 1000 * 300) },
  { id: "4", type: "file", message: "Analyzed project structure", timestamp: new Date(Date.now() - 1000 * 600) },
  { id: "5", type: "command", message: "Executed git pull on main branch", timestamp: new Date(Date.now() - 1000 * 900) },
];

function timeAgo(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  return `${hours}h ago`;
}

export function ActivityFeed() {
  return (
    <Card className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">Activity Feed</h3>
        <span className="flex h-2 w-2 rounded-full bg-accent shadow-extruded-sm" />
      </div>
      <div className="flex flex-col gap-2">
        <AnimatePresence mode="popLayout">
          {recentActivities.map((activity, i) => {
            const Icon = activityIcons[activity.type];
            return (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-start gap-3 rounded-2xl p-3 transition-colors hover:bg-white/30"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#E0E5EC] text-accent shadow-inset-sm">
                  <Icon className="h-4 w-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-foreground">{activity.message}</p>
                  <p className="mt-0.5 text-xs text-muted">{timeAgo(activity.timestamp)}</p>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </Card>
  );
}
