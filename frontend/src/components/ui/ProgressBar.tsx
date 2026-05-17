"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
  value: number;
  variant?: "accent" | "secondary";
  className?: string;
  showLabel?: boolean;
}

const MotionDiv = motion.create("div");

export function ProgressBar({
  value,
  variant = "accent",
  className,
  showLabel = false,
}: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, value));
  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="h-3 flex-1 rounded-full bg-[#E0E5EC] shadow-inset-sm">
        <MotionDiv
          initial={{ width: 0 }}
          animate={{ width: `${clamped}%` }}
          transition={{ type: "spring", stiffness: 100, damping: 20 }}
          className={cn(
            "h-full rounded-full shadow-extruded-sm",
            variant === "accent" ? "bg-accent" : "bg-accent-secondary",
          )}
        />
      </div>
      {showLabel && (
        <span className="min-w-[3ch] text-sm font-medium text-foreground">
          {Math.round(clamped)}%
        </span>
      )}
    </div>
  );
}
