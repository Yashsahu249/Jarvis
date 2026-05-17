"use client";

import { motion } from "framer-motion";
import { Search, MessageSquare, Clock, Calendar } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";

const conversations = [
  { id: "1", title: "React component optimization", preview: "We discussed memoization strategies...", date: "2h ago", messages: 12 },
  { id: "2", title: "API design for microservices", preview: "REST vs GraphQL comparison for...", date: "1d ago", messages: 8 },
  { id: "3", title: "Docker deployment guide", preview: "Multi-stage builds and compose...", date: "2d ago", messages: 15 },
  { id: "4", title: "Python async patterns", preview: "Asyncio vs trio for concurrent...", date: "3d ago", messages: 6 },
  { id: "5", title: "Database indexing strategies", preview: "B-tree vs hash indexes in...", date: "5d ago", messages: 9 },
];

export function MemoryBrowser() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-foreground">Memory Browser</h2>
        <span className="text-sm text-muted">247 conversations</span>
      </div>

      <Input
        icon={<Search className="h-4 w-4" />}
        placeholder="Search memories..."
        className="max-w-md"
      />

      <div className="flex flex-col gap-3">
        {conversations.map((conv, i) => (
          <motion.div
            key={conv.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.03 }}
          >
            <Card
              hoverable
              padding="md"
              className="cursor-pointer transition-all"
            >
              <div className="flex items-start justify-between">
                <div className="min-w-0 flex-1">
                  <h3 className="font-medium text-foreground">{conv.title}</h3>
                  <p className="mt-1 text-sm text-muted">{conv.preview}</p>
                </div>
              </div>
              <div className="mt-3 flex items-center gap-4 text-xs text-muted">
                <span className="flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5" /> {conv.date}
                </span>
                <span className="flex items-center gap-1">
                  <MessageSquare className="h-3.5 w-3.5" /> {conv.messages} messages
                </span>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
