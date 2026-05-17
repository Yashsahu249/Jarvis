"use client";

import { forwardRef, type InputHTMLAttributes, type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  icon?: ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, icon, ...props }, ref) => {
    return (
      <div className="relative">
        {icon && (
          <div className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted">
            {icon}
          </div>
        )}
        <input
          ref={ref}
          className={cn(
            "w-full rounded-2xl bg-[#E0E5EC] px-4 py-3 text-foreground shadow-inset-sm transition-all duration-200 placeholder:text-[#A0AEC0] focus:shadow-inset-deep focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-[#E0E5EC]",
            icon && "pl-12",
            className,
          )}
          {...props}
        />
      </div>
    );
  },
);

Input.displayName = "Input";
