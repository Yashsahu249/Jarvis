"use client";

import { motion } from "framer-motion";
import { TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/Card";

interface StatCardProps {
  icon: React.ReactNode;
  value: string;
  label: string;
  trend?: number;
  trendLabel?: string;
  className?: string;
}

const MotionDiv = motion.create("div");

export function StatCard({
  icon,
  value,
  label,
  trend,
  trendLabel,
  className,
}: StatCardProps) {
  const isUp = (trend ?? 0) >= 0;
  return (
    <Card className={cn("flex flex-col gap-3", className)} padding="lg">
      <div className="flex items-center justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#E0E5EC] text-accent shadow-inset-sm">
          {icon}
        </div>
        {trend !== undefined && (
          <MotionDiv
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            className={cn(
              "flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium",
              isUp ? "bg-[#38B2AC]/10 text-[#38B2AC]" : "bg-[#FC8181]/10 text-[#FC8181]",
            )}
          >
            {isUp ? (
              <TrendingUp className="h-3.5 w-3.5" />
            ) : (
              <TrendingDown className="h-3.5 w-3.5" />
            )}
            {Math.abs(trend)}%
          </MotionDiv>
        )}
      </div>
      <div>
        <p className="text-3xl font-bold text-foreground">{value}</p>
        <p className="mt-1 text-sm text-muted">{label}</p>
        {trendLabel && <p className="mt-0.5 text-xs text-muted">{trendLabel}</p>}
      </div>
    </Card>
  );
}
