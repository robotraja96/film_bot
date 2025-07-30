"use client";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useState, useEffect } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {isClient && (
          <CopilotKit
            runtimeUrl="/api/copilotkit"
            agent="agent" // the name of the agent you want to use
          >
            <CopilotSidebar
              defaultOpen={true}
              instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
              labels={{
                title: "Sidebar Assistant",
                initial: "How can I help you today?",
              }}
            >
              {children}
            </CopilotSidebar>
          </CopilotKit>
        )}
      </body>
    </html>
  );
}