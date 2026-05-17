"use client";

import { MessageSquare, Search, Trash2, Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";

interface Conversation {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
}

const sampleConversations: Conversation[] = [
  { id: "1", title: "Help with React hooks", createdAt: Date.now() - 1000 * 3600, updatedAt: Date.now() - 1000 * 1800 },
  { id: "2", title: "Python data analysis script", createdAt: Date.now() - 1000 * 7200, updatedAt: Date.now() - 1000 * 3600 },
  { id: "3", title: "Docker deployment setup", createdAt: Date.now() - 1000 * 86400, updatedAt: Date.now() - 1000 * 43200 },
  { id: "4", title: "API design review", createdAt: Date.now() - 1000 * 172800, updatedAt: Date.now() - 1000 * 86400 },
  { id: "5", title: "Database schema optimization", createdAt: Date.now() - 1000 * 259200, updatedAt: Date.now() - 1000 * 172800 },
];

interface ConversationListProps {
  activeId?: string | null;
  onSelect?: (id: string) => void;
  onDelete?: (id: string) => void;
  onNew?: () => void;
}

export function ConversationList({
  activeId,
  onSelect,
  onDelete,
  onNew,
}: ConversationListProps) {
  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
          <input
            type="text"
            placeholder="Search conversations..."
            className="w-full rounded-2xl bg-[#E0E5EC] py-2.5 pl-10 pr-4 text-sm text-foreground shadow-inset-sm placeholder:text-[#A0AEC0] focus:shadow-inset-deep focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-[#E0E5EC]"
          />
        </div>
        <button
          onClick={onNew}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-extruded-sm transition-all hover:shadow-extruded-hover active:shadow-inset-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          <Plus className="h-5 w-5" />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto scrollbar-thin">
        {sampleConversations.map((conv) => (
          <button
            key={conv.id}
            onClick={() => onSelect?.(conv.id)}
            className={cn(
              "group flex w-full items-center gap-3 rounded-2xl p-3 text-left transition-all",
              activeId === conv.id
                ? "bg-[#E0E5EC] shadow-inset-sm"
                : "hover:bg-white/30",
            )}
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#E0E5EC] text-accent shadow-inset-sm">
              <MessageSquare className="h-4 w-4" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-foreground">
                {conv.title}
              </p>
              <p className="text-xs text-muted">
                {format(new Date(conv.updatedAt), "MMM d, h:mm a")}
              </p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete?.(conv.id);
              }}
              className="shrink-0 rounded-xl p-1.5 text-muted opacity-0 transition-opacity hover:text-[#FC8181] group-hover:opacity-100 focus-visible:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </button>
        ))}
      </div>
    </div>
  );
}
