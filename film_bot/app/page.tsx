"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useState, useEffect } from "react";

export default function Home() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <>
      {isClient && (
        <CopilotChat
          instructions="You are assisting the user as best as you can. Answer in the best way possible given the data you have."
          labels={{
            title: "Film Bot",
            initial: "Hi! 👋 How can I assist you today?",
          }}
        />
      )}
    </>
  );
}
