"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { MemoryBrowser } from "@/components/memory/MemoryBrowser";
import { MemoryConversation } from "@/components/memory/MemoryConversation";

const MotionDiv = motion.create("div");

export default function MemoryPage() {
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null);

  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col gap-6 p-6"
    >
      {selectedConversation ? <MemoryConversation /> : <MemoryBrowser />}
    </MotionDiv>
  );
}
