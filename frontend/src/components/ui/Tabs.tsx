"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface Tab {
  id: string;
  label: string;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (id: string) => void;
  className?: string;
}

const MotionButton = motion.create("button");

export function Tabs({ tabs, activeTab, onChange, className }: TabsProps) {
  return (
    <div
      className={cn(
        "inline-flex rounded-2xl bg-[#E0E5EC] p-1.5",
        "shadow-inset-sm",
        className,
      )}
    >
      {tabs.map((tab) => (
        <MotionButton
          key={tab.id}
          whileTap={{ scale: 0.97 }}
          onClick={() => onChange(tab.id)}
          className={cn(
            "relative rounded-xl px-4 py-2 text-sm font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-[#E0E5EC]",
            activeTab === tab.id
              ? "text-foreground shadow-inset-sm"
              : "text-muted shadow-extruded-sm hover:text-foreground",
          )}
        >
          {tab.label}
        </MotionButton>
      ))}
    </div>
  );
}
