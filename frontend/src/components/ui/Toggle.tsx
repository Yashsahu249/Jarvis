"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ToggleProps {
  enabled: boolean;
  onChange: (enabled: boolean) => void;
  className?: string;
}

const MotionDiv = motion.create("div");
const MotionButton = motion.create("button");

export function Toggle({ enabled, onChange, className }: ToggleProps) {
  return (
    <MotionButton
      whileTap={{ scale: 0.95 }}
      onClick={() => onChange(!enabled)}
      className={cn(
        "relative inline-flex h-7 w-12 cursor-pointer items-center rounded-full transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-[#E0E5EC]",
        enabled
          ? "bg-accent shadow-inset-sm"
          : "bg-[#E0E5EC] shadow-extruded-sm",
        className,
      )}
      role="switch"
      aria-checked={enabled}
    >
      <MotionDiv
        animate={{ x: enabled ? 22 : 3 }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
        className="h-5 w-5 rounded-full bg-white shadow-md"
      />
    </MotionButton>
  );
}
