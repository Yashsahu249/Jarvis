"use client";

import { type ReactNode } from "react";
import { motion } from "framer-motion";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface MainLayoutProps {
  children: ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#E0E5EC]">
      <Sidebar />
      <div className="flex flex-col flex-1 min-w-0">
        <Header />
        <motion.main
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="flex-1 overflow-y-auto p-4 lg:p-6 scrollbar-thin"
        >
          {children}
        </motion.main>
      </div>
    </div>
  );
}
