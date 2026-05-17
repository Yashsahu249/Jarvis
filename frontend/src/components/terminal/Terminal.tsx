"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Terminal as TerminalIcon,
  Trash2,
  AlertTriangle,
  Shield,
  Info,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

interface CommandEntry {
  id: string;
  command: string;
  output: string;
  risk: "low" | "medium" | "high";
  timestamp: Date;
  approved?: boolean;
}

const riskColors = {
  low: "text-[#38B2AC]",
  medium: "text-[#F6AD55]",
  high: "text-[#FC8181]",
};

const initialHistory: CommandEntry[] = [
  {
    id: "1",
    command: "ls -la",
    output: "total 24\ndrwxr-xr-x  5 user  group   160 Mar 15 10:30 .\ndrwxr-xr-x  3 user  group    96 Mar 15 10:30 ..",
    risk: "low",
    timestamp: new Date(Date.now() - 1000 * 120),
  },
  {
    id: "2",
    command: "git status",
    output: "On branch main\nYour branch is up to date with 'origin/main'.\n\nnothing to commit, working tree clean",
    risk: "low",
    timestamp: new Date(Date.now() - 1000 * 60),
  },
];

const riskEmoji = {
  low: <Info className="h-4 w-4" />,
  medium: <AlertTriangle className="h-4 w-4" />,
  high: <AlertTriangle className="h-4 w-4" />,
};

export function Terminal() {
  const [history, setHistory] = useState<CommandEntry[]>(initialHistory);
  const [input, setInput] = useState("");
  const [pendingApproval, setPendingApproval] = useState<CommandEntry | null>(null);
  const outputRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    outputRef.current?.scrollTo(0, outputRef.current.scrollHeight);
  }, [history]);

  const executeCommand = () => {
    if (!input.trim()) return;

    const risk: "low" | "medium" | "high" =
      input.includes("rm -rf") || input.includes("sudo")
        ? "high"
        : input.includes("rm") || input.includes("chmod")
          ? "medium"
          : "low";

    const entry: CommandEntry = {
      id: crypto.randomUUID(),
      command: input.trim(),
      output: `[Simulated output] Ran: ${input.trim()}\n> Command completed successfully.`,
      risk,
      timestamp: new Date(),
      approved: risk === "low",
    };

    if (risk !== "low") {
      setPendingApproval(entry);
    } else {
      setHistory((prev) => [...prev, entry]);
    }
    setInput("");
  };

  const approveCommand = () => {
    if (pendingApproval) {
      setHistory((prev) => [...prev, { ...pendingApproval, approved: true }]);
      setPendingApproval(null);
    }
  };

  const rejectCommand = () => {
    setPendingApproval(null);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <TerminalIcon className="h-6 w-6 text-accent" />
          <h2 className="text-xl font-bold text-foreground">Terminal</h2>
        </div>
        <Button size="sm" variant="ghost" onClick={clearHistory}>
          <Trash2 className="h-4 w-4" /> Clear
        </Button>
      </div>

      <Card hoverable={false} className="flex flex-col gap-4 p-6">
        <div
          ref={outputRef}
          className="h-[400px] overflow-y-auto rounded-[32px] bg-[#1a1b2e] p-4 font-mono text-sm scrollbar-thin"
        >
          <AnimatePresence mode="popLayout">
            {history.map((entry) => (
              <motion.div
                key={entry.id}
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-3"
              >
                <div className="flex items-center gap-2 text-[#38B2AC]">
                  <ChevronRight className="h-4 w-4" />
                  <span className="text-[#8B84FF]">jarvis@os</span>
                  <span className="text-muted">:~$</span>
                  <span className="text-white">{entry.command}</span>
                  {entry.risk !== "low" && (
                    <Badge
                      variant={
                        entry.risk === "high" ? "error" : "warning"
                      }
                      className="ml-2"
                    >
                      {entry.risk}
                    </Badge>
                  )}
                </div>
                <pre className="mt-1 whitespace-pre-wrap pl-6 text-gray-400">
                  {entry.output}
                </pre>
              </motion.div>
            ))}
          </AnimatePresence>

          {pendingApproval && (
            <motion.div
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-3 rounded-2xl border border-[#F6AD55]/50 bg-[#F6AD55]/10 p-4"
            >
              <div className="flex items-center gap-2 text-[#F6AD55]">
                <AlertTriangle className="h-5 w-5" />
                <span className="font-medium">
                  {pendingApproval.risk === "high"
                    ? "High Risk Command"
                    : "Medium Risk Command"}
                </span>
              </div>
              <div className="mt-2 flex items-center gap-2 font-mono text-sm text-white">
                <ChevronRight className="h-4 w-4 text-[#F6AD55]" />
                <span>{pendingApproval.command}</span>
              </div>
              <div className="mt-3 flex gap-2">
                <Button size="sm" variant="primary" onClick={approveCommand}>
                  <Shield className="h-4 w-4" /> Approve
                </Button>
                <Button size="sm" variant="secondary" onClick={rejectCommand}>
                  Reject
                </Button>
              </div>
            </motion.div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#E0E5EC] text-accent shadow-inset-sm">
            <ChevronRight className="h-4 w-4" />
          </div>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") executeCommand();
            }}
            placeholder="Enter command..."
            className="flex-1 rounded-2xl bg-[#E0E5EC] px-4 py-2.5 text-sm text-foreground shadow-inset-sm placeholder:text-[#A0AEC0] focus:shadow-inset-deep focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-[#E0E5EC]"
          />
        </div>
      </Card>
    </div>
  );
}
