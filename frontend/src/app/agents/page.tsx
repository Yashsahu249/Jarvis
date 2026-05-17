"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { AgentGrid } from "@/components/agents/AgentGrid";
import { AgentDetail } from "@/components/agents/AgentDetail";

const MotionDiv = motion.create("div");

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col gap-6 p-6"
    >
      <div>
        <h1 className="text-2xl font-bold text-foreground">Agents</h1>
        <p className="text-sm text-muted">Manage your Jarvis agents</p>
      </div>
      {selectedAgent ? <AgentDetail /> : <AgentGrid />}
    </MotionDiv>
  );
}
