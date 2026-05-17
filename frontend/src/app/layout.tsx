import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Jarvis OS",
  description:
    "Jarvis OS — An intelligent operating system for the modern age.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#E0E5EC] font-sans antialiased">{children}</body>
    </html>
  );
}
