"use client";

import { motion } from "framer-motion";
import { Bot, User, Clock, Calendar, ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { format } from "date-fns";

const messages = [
  { id: "1", role: "user", content: "How do I optimize React components?", timestamp: Date.now() - 1000 * 60 * 30 },
  { id: "2", role: "assistant", content: "Use React.memo for pure components, useCallback for function props, and useMemo for expensive computations. Also consider virtualization for long lists.", timestamp: Date.now() - 1000 * 60 * 28 },
  { id: "3", role: "user", content: "Can you show me a code example?", timestamp: Date.now() - 1000 * 60 * 25 },
  { id: "4", role: "assistant", content: "```tsx\nconst ExpensiveList = React.memo(({ items }: { items: Item[] }) => {\n  return items.map(item => <ListItem key={item.id} item={item} />);\n});\n```\n\nThis prevents re-renders when items reference hasn't changed.", timestamp: Date.now() - 1000 * 60 * 23 },
];

export function MemoryConversation() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm">
          <ArrowLeft className="h-4 w-4" /> Back
        </Button>
        <div>
          <h2 className="text-lg font-bold text-foreground">React component optimization</h2>
          <div className="flex items-center gap-3 text-xs text-muted">
            <span className="flex items-center gap-1">
              <Calendar className="h-3.5 w-3.5" /> {format(new Date(), "MMM d, yyyy")}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-3.5 w-3.5" /> 12 messages
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        {messages.map((msg, i) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className={cn(
              "flex gap-3",
              msg.role === "user" ? "flex-row-reverse" : "flex-row",
            )}
          >
            <div
              className={cn(
                "flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl",
                msg.role === "user"
                  ? "bg-accent text-white shadow-extruded-sm"
                  : "bg-[#E0E5EC] text-accent shadow-inset-sm",
              )}
            >
              {msg.role === "user" ? (
                <User className="h-4 w-4" />
              ) : (
                <Bot className="h-4 w-4" />
              )}
            </div>
            <div
              className={cn(
                "max-w-[75%] rounded-[32px] px-5 py-3",
                msg.role === "user"
                  ? "bg-accent text-white"
                  : "bg-[#E0E5EC] text-foreground shadow-extruded-sm",
              )}
            >
              <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
              <p
                className={cn(
                  "mt-1 text-xs",
                  msg.role === "user" ? "text-white/70" : "text-muted",
                )}
              >
                {format(new Date(msg.timestamp), "h:mm a")}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
