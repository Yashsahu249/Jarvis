"use client";

import { motion } from "framer-motion";
import {
  MessageSquare,
  Mic,
  Globe,
  Bot,
  GitBranch,
  Brain,
  Terminal,
  Cpu,
  Activity,
} from "lucide-react";
import { StatCard } from "@/components/dashboard/StatCard";
import { ActivityFeed } from "@/components/dashboard/ActivityFeed";
import { SystemPanel } from "@/components/dashboard/SystemPanel";
import { MemoryPanel } from "@/components/dashboard/MemoryPanel";
import { BrowserPanel } from "@/components/dashboard/BrowserPanel";
import { AgentPanel } from "@/components/dashboard/AgentPanel";

const MotionDiv = motion.create("div");

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.05 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function DashboardPage() {
  return (
    <MotionDiv
      variants={container}
      initial="hidden"
      animate="show"
      className="flex flex-col gap-6 p-6"
    >
      <div>
        <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
        <p className="text-sm text-muted">Jarvis OS System Overview</p>
      </div>

      <MotionDiv variants={item} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={<MessageSquare className="h-6 w-6" />}
          value="1,247"
          label="Total Conversations"
          trend={12}
          trendLabel="vs last week"
        />
        <StatCard
          icon={<Activity className="h-6 w-6" />}
          value="89%"
          label="Task Success Rate"
          trend={5}
          trendLabel="vs last week"
        />
        <StatCard
          icon={<Cpu className="h-6 w-6" />}
          value="32%"
          label="CPU Usage"
          trend={-8}
          trendLabel="vs last hour"
        />
        <StatCard
          icon={<Bot className="h-6 w-6" />}
          value="4"
          label="Active Agents"
          trend={0}
          trendLabel="All operational"
        />
      </MotionDiv>

      <MotionDiv variants={item} className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ActivityFeed />
        </div>
        <SystemPanel />
      </MotionDiv>

      <MotionDiv variants={item} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <MemoryPanel />
        <BrowserPanel />
        <AgentPanel />
      </MotionDiv>
    </MotionDiv>
  );
}
