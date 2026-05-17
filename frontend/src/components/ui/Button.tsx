"use client";

import { forwardRef, type ButtonHTMLAttributes } from "react";
import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

const variants = {
  primary:
    "bg-accent text-white shadow-extruded hover:bg-accent-light hover:shadow-extruded-hover active:shadow-inset",
  secondary:
    "bg-[#E0E5EC] text-foreground shadow-extruded hover:shadow-extruded-hover active:shadow-inset-sm",
  ghost:
    "bg-transparent text-foreground shadow-none hover:shadow-inset-sm active:shadow-inset-sm",
};

const sizes = {
  sm: "px-3 py-1.5 text-sm gap-1.5",
  md: "px-5 py-2.5 text-base gap-2",
  lg: "px-7 py-3.5 text-lg gap-2.5",
};

interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onAnimationStart" | "onDrag" | "onDragStart" | "onDragEnd" | "onDragEnter" | "onDragLeave" | "onDragOver"> {
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}

const MotionButton = motion.create("button");

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    return (
      <MotionButton
        ref={ref}
        whileHover={{ y: -1 }}
        whileTap={{ y: 0.5 }}
        className={cn(
          "inline-flex items-center justify-center rounded-2xl font-medium transition-shadow duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-[#E0E5EC] disabled:pointer-events-none disabled:opacity-50",
          variants[variant],
          sizes[size],
          className,
        )}
        {...(props as HTMLMotionProps<"button">)}
      >
        {children}
      </MotionButton>
    );
  },
);

Button.displayName = "Button";
