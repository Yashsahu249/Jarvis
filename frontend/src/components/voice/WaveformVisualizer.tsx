"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface WaveformVisualizerProps {
  isActive: boolean;
  className?: string;
}

const MotionDiv = motion.create("div");

export function WaveformVisualizer({ isActive, className }: WaveformVisualizerProps) {
  return (
    <div className={cn("flex items-center justify-center gap-1", className)}>
      {Array.from({ length: 32 }).map((_, i) => (
        <MotionDiv
          key={i}
          animate={
            isActive
              ? {
                  height: [8, Math.random() * 40 + 12, 8],
                  transition: {
                    duration: 0.4 + Math.random() * 0.4,
                    repeat: Infinity,
                    delay: i * 0.03,
                    ease: "easeInOut",
                  },
                }
              : { height: 8 }
          }
          className="w-1.5 rounded-full bg-accent"
          style={{ height: 8 }}
        />
      ))}
    </div>
  );
}
