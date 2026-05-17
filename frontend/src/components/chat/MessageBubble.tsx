"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Copy, Check, User, Bot } from "lucide-react";
import { cn } from "@/lib/utils";

interface MessageBubbleProps {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: number;
}

export function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const [copiedBlock, setCopiedBlock] = useState<string | null>(null);
  const isUser = role === "user";

  const copyToClipboard = async (code: string) => {
    await navigator.clipboard.writeText(code);
    setCopiedBlock(code);
    setTimeout(() => setCopiedBlock(null), 2000);
  };

  return (
    <div
      className={cn(
        "flex w-full gap-3",
        isUser ? "flex-row-reverse" : "flex-row",
      )}
    >
      <div
        className={cn(
          "flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl",
          isUser
            ? "bg-accent text-white shadow-extruded-sm"
            : "bg-[#E0E5EC] text-accent shadow-inset-sm",
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>
      <div className={cn("max-w-[75%]", isUser && "items-end")}>
        <div
          className={cn(
            "rounded-[32px] px-5 py-3",
            isUser
              ? "bg-accent text-white"
              : "bg-[#E0E5EC] text-foreground shadow-extruded-sm",
          )}
        >
          <div className={cn("prose prose-sm max-w-none", isUser && "prose-invert")}>
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className ?? "");
                  const codeString = String(children).replace(/\n$/, "");
                  if (match) {
                    return (
                      <div className="relative my-2 rounded-2xl bg-[#E0E5EC] shadow-inset-sm">
                        <div className="flex items-center justify-between rounded-t-2xl border-b border-[#D1D5DB]/50 px-4 py-2">
                          <span className="text-xs text-muted">{match[1]}</span>
                          <button
                            onClick={() => copyToClipboard(codeString)}
                            className="rounded-xl p-1.5 text-muted transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                          >
                            {copiedBlock === codeString ? (
                              <Check className="h-4 w-4" />
                            ) : (
                              <Copy className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                        <SyntaxHighlighter
                          style={oneLight}
                          language={match[1]}
                          PreTag="div"
                          customStyle={{
                            margin: 0,
                            borderRadius: "0 0 16px 16px",
                            background: "#E0E5EC",
                            fontSize: "0.875rem",
                          }}
                        >
                          {codeString}
                        </SyntaxHighlighter>
                      </div>
                    );
                  }
                  return (
                    <code
                      className="rounded-xl bg-[#D1D5DB]/40 px-2 py-0.5 text-sm"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
              }}
            >
              {content}
            </ReactMarkdown>
          </div>
        </div>
        {timestamp && (
          <p className="mt-1 px-2 text-xs text-muted">
            {new Date(timestamp).toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}
