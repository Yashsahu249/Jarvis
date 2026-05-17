"use client";

import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

const badgeVariants = {
  default:
    "bg-[#E0E5EC] text-foreground shadow-extruded-sm",
  accent:
    "bg-accent text-white shadow-extruded-sm",
  success:
    "bg-[#38B2AC] text-white shadow-extruded-sm",
  warning:
    "bg-[#F6AD55] text-white shadow-extruded-sm",
  error:
    "bg-[#FC8181] text-white shadow-extruded-sm",
};

interface BadgeProps {
  children: ReactNode;
  variant?: keyof typeof badgeVariants;
  className?: string;
}

export function Badge({ children, variant = "default", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-medium",
        badgeVariants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
