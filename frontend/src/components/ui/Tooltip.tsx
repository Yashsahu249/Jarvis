"use client";

import { useState, type ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface TooltipProps {
  content: string;
  children: ReactNode;
  position?: "top" | "bottom" | "left" | "right";
  className?: string;
}

const MotionDiv = motion.create("div");

const positionStyles = {
  top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
  bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
  left: "right-full top-1/2 -translate-y-1/2 mr-2",
  right: "left-full top-1/2 -translate-y-1/2 ml-2",
};

export function Tooltip({
  content,
  children,
  position = "top",
  className,
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div
      className={cn("relative inline-flex", className)}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      {children}
      <AnimatePresence>
        {isVisible && (
          <MotionDiv
            initial={{ opacity: 0, scale: 0.9, y: position === "top" ? 4 : -4 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: position === "top" ? 4 : -4 }}
            transition={{ duration: 0.15 }}
            className={cn(
              "pointer-events-none absolute z-50 whitespace-nowrap rounded-2xl bg-[#E0E5EC] px-3 py-1.5 text-xs font-medium text-foreground shadow-extruded-sm",
              positionStyles[position],
            )}
          >
            {content}
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
}
