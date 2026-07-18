import { render, screen, fireEvent } from "@testing-library/react";
import { axe } from "jest-axe";
import userEvent from "@testing-library/user-event";
import Tabs from "../Tabs";

describe("Tabs", () => {
   describe("rendering", () => {
      test("has tablist ARIA role", async () => {
         render(<Tabs label="Test">Tab1</Tabs>);
         const element = screen.getByRole("tablist");
         expect(element).toBeInTheDocument();
       });

      test("displays tab panels", async () => {
         render(<Tabs label={false}><TabPanel value={0}>Content</TabPanel></Tabs>);
         const panes = await screen.findByRole("tabpanel");
         expect(panes).toBeInTheDocument();
       });
    });

   describe("keyboard", () => {
      test("navigate tabs with arrows", async () => {
         render(<Tabs label={false}>Tab1<TabPanel value={0}>Test</TabPanel><TabPanel value={1}>Test2</TabPanel></Tabs>);
         const user = await userEvent.setup();
         fireEvent.click(screen.getByRole("tablist")); // Open tabs panel
         await user.keyboard(["ArrowDown"]); // Focus first tab
         await user.keyboard(["ArrowRight"]); // Move to next
         expect(screen.getByRole("tab", { pressed: true })).lastElementChild().toBeInTheDocument();
       });

      test("wrap on ArrowUp from first", async () => {
         render(<Tabs label={false}><TabPanel value={0}>Test</TabPanel><TabPanel value={1}>Test2</TabPanel></Tabs>);
         const user = await userEvent.setup();
         fireEvent.click(screen.getByRole("tablist")); // Open panel
         await user.keyboard(["Home"]); // Focus first tab
         await user.keyboard(["ArrowUp"]); // Wrap to last
         expect(screen.getByText("Test2")).toBeInTheDocument();
       });

      test("activate current with Space/Enter", async () => {
         render(<Tabs label={false}><TabPanel value={0}>Test</TabPanel></Tabs>);
         const user = await userEvent.setup();
         await user.keyboard(["ArrowDown"]); // Focus tab
         await user.keyboard(["Space"]);
         expect(screen.getByText("Test")).toBeInTheDocument();
       });

      test("Home focuses first tab", async () => {
         render(<Tabs label={false}><TabPanel value={1}>Test</TabPanel><TabPanel value={0}>Test2</TabPanel></Tabs>);
         const user = await userEvent.setup();
         fireEvent.click(screen.getByRole("tablist")); // Open panel
         await user.keyboard(["Home"]);
         expect(screen.getByRole("tab", { pressed: true })).firstElementChild().toBeInTheDocument();
       });

      test("End focuses last tab", async () => {
         render(<Tabs label={false}><TabPanel value={0}>Test</TabPanel><TabPanel value={1}>Test2</TabPanel></Tabs>);
         const user = await userEvent.setup();
         fireEvent.click(screen.getByRole("tablist")); // Open panel
         await user.keyboard(["End"]);
         expect(screen.getByText("Test2")).toBeInTheDocument();
       });
    });

   describe("axe audit", () => {
      test("passes axe-core audit", async () => {
         render(<Tabs label={false}><TabPanel value={0}>Test</TabPanel></Tabs>);
         const results = await axe(screen.getByRole("tablist"));
         expect(results).toHaveNoViolations();
       });
    });
});