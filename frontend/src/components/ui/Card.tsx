"use client";

import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface CardProps {
  children: ReactNode;
  className?: string;
  hoverable?: boolean;
  padding?: "sm" | "md" | "lg";
}

const paddings = {
  sm: "p-4",
  md: "p-6",
  lg: "p-8",
};

const MotionDiv = motion.create("div");

export function Card({
  children,
  className,
  hoverable = true,
  padding = "md",
}: CardProps) {
  return (
    <MotionDiv
      whileHover={hoverable ? { y: -4 } : undefined}
      transition={{ type: "spring", stiffness: 200, damping: 15 }}
      className={cn(
        "rounded-[32px] bg-[#E0E5EC] shadow-extruded transition-shadow duration-300",
        hoverable && "hover:shadow-extruded-hover",
        paddings[padding],
        className,
      )}
    >
      {children}
    </MotionDiv>
  );
}
