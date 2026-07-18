import { defineConfig } from "vitest/config";
import reactPlugin from "@vitejs/plugin-react";

export default defineConfig({
   plugins: [reactPlugin()],
   test: {
      globals: true,
      environment: "jsdom",
      include: ["src/**/*test.ts", "src/**/*test.tsx"],
    }
});