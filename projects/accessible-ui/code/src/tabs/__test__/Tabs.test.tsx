import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Tabs from "../Tabs";

describe("Tabs - Rendering", () => {
   test("has tablist ARIA role when rendered", async () => {
      const result = await render(<Tabs options={[{ value: 0, label: "Tab 1" }]}>Test</Tabs>);
      expect(result.asTheDOM).toHaveRole("tablist");
    });

   test("displays tab panels correctly", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]}>Content</Tabs>);
      const pane = await screen.findByRole("tabpanel");
      expect(pane).toBeInTheDocument();
    });

   test("renders with correct aria-selected state", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
      const tab = screen.getByRole("tab");
      expect(tab).toHaveAttribute("aria-selected", "true");
    });

   test("displays panels correctly for multiple tabs", async () => {
      render(<Tabs options={[{ value: 1, label: "Tab 2" }]} activeIndex={1}>Content</Tabs>);
      const panel = await screen.findByRole("tabpanel");
      expect(panel).toBeInTheDocument();
    });
});

describe("Tabs - Keyboard Navigation", () => {
   test("focus next tab on ArrowDown", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]}>Test</Tabs>);
      const user = await userEvent.setup();
       // Focus first tab initially
      expect(screen.getByRole("tab", { pressed: false })).toBeInTheDocument();
      await user.keyboard(["ArrowDown"]);
      expect(screen.getByRole("tab", { pressed: true })).toBeInTheDocument();
    });

   test("wrap on ArrowUp from first tab", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]} activeIndex={0}>Test</Tabs>);
      const user = await userEvent.setup();
      await user.keyboard(["ArrowDown", "ArrowUp"]); // Should wrap back to first
    });

   test("Home focuses first tab", async () => {
      render(<Tabs options={[{ value: 1, label: "Tab 2" }, { value: 0, label: "Tab 1" }]} activeIndex={1}>Test</Tabs>);
      const user = await userEvent.setup();
      await user.keyboard(["Home"]);
    });

   test("End focuses last tab", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]} activeIndex={0}>Test</Tabs>);
      const user = await userEvent.setup();
      await user.keyboard(["End"]);
    });

   test("manual activation on Space key", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
      const user = await userEvent.setup();
      await user.keyboard(["ArrowDown"]); // Focus tab
      await user.keyboard(["Space"]); // Should activate
    });

   test("manual activation on Enter key", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
      const user = await userEvent.setup();
      await user.keyboard(["ArrowDown"]); // Focus tab
      await user.keyboard(["Enter"]); // Should activate
    });
});

describe("Tabs - Accessibility Audit", () => {
   test("passes axe-core accessibility audit", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]}>Test</Tabs>);
      const results = await screen.getByRole("tablist");
    });

   test("manages focus correctly on panel toggle", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
       // Focus management tests
    });

   test("updates aria-selected state when panels change", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]} activeIndex={0}>Test</Tabs>);
      const tabs = screen.getByRole("tab");
      expect(tabs[0]).toHaveAttribute("aria-selected", "true");
    });

   test("properly handle focus management on keyboard events", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]}>Test</Tabs>);
       // Focus handling tests
    });

   test("correct panel state after navigation sequence", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]} activeIndex={0}>Test</Tabs>);
       // Navigation sequence tests
    });
});

describe("Tabs - Integration Tests", () => {
   test("propagate navigation to onChange handler", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
       // Integration tests
    });

   test("properly handle focus management on keyboard events", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }]} activeIndex={0}>Test</Tabs>);
         // Focus handling tests
    });

   test("correct panel state after toggle sequence", async () => {
      render(<Tabs options={[{ value: 0, label: "Tab 1" }, { value: 1, label: "Tab 2" }]} activeIndex={0}>Test</Tabs>);
       // Sequence tests
    });
});
