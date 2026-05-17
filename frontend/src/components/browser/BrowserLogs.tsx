"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Terminal, CheckCircle, XCircle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";

interface Log {
  id: string;
  message: string;
  type: "info" | "success" | "error";
  timestamp: Date;
}

const logs: Log[] = [
  { id: "1", message: "Navigated to github.com", type: "success", timestamp: new Date(Date.now() - 1000 * 10) },
  { id: "2", message: "Clicked on repository link", type: "info", timestamp: new Date(Date.now() - 1000 * 20) },
  { id: "3", message: "Scrolling to find element...", type: "info", timestamp: new Date(Date.now() - 1000 * 30) },
  { id: "4", message: "Element not found, retrying", type: "error", timestamp: new Date(Date.now() - 1000 * 40) },
  { id: "5", message: "New tab opened", type: "success", timestamp: new Date(Date.now() - 1000 * 50) },
];

export function BrowserLogs() {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2 text-sm font-medium text-foreground">
        <Terminal className="h-4 w-4" />
        <span>Activity Log</span>
      </div>
      <div className="flex flex-col gap-1">
        <AnimatePresence mode="popLayout">
          {logs.map((log, i) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.03 }}
              className="flex items-center gap-2 rounded-xl px-3 py-2 text-xs"
            >
              {log.type === "success" && (
                <CheckCircle className="h-3.5 w-3.5 shrink-0 text-[#38B2AC]" />
              )}
              {log.type === "error" && (
                <XCircle className="h-3.5 w-3.5 shrink-0 text-[#FC8181]" />
              )}
              {log.type === "info" && (
                <Clock className="h-3.5 w-3.5 shrink-0 text-accent" />
              )}
              <span className="text-muted">{log.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
