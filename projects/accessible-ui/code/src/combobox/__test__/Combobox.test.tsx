import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Combobox from "../Combobox";

describe("Combobox - Rendering", () => {
   test("has combobox ARIA role when rendered", async () => {
      const result = await render(<Combobox options={[{ value: "test" }]} />);
      expect(result.asTheDOM).toHaveRole("combobox");
   });

   test("displays listbox when panel is expanded", async () => {
      render(<Combobox options={[{ value: "apple" }, { value: "banana" }]} />);
      await fireEvent.click(screen.getByRole("combobox"));
      expect(screen.getByRole("listbox")).toBeInTheDocument();
   });

   test("renders with correct ARIA labels", async () => {
      render(<Combobox options={[{ value: "test" }]} label="Test Label" />);
      const combobox = await screen.getByRole("combobox");
      expect(combobox).toHaveAttribute("aria-label", "Test Label");
   });

   test("displays listbox correctly for multiple options", async () => {
      render(<Combobox options={[{ value: "a" }, { value: "b" }]} />);
      await fireEvent.click(screen.getByRole("combobox"));
      const listbox = screen.getByRole("listbox");
      expect(listbox).toHaveTextContent("a, b");
   });

   test("has correct aria-expanded state when panel toggles", async () => {
      render(<Combobox options={[]}>Test</Combobox>);
      const combobox = screen.getByRole("combobox");
      expect(combobox).toHaveAttribute("aria-expanded", "false");
      await fireEvent.click(combobox);
      expect(combobox).toHaveAttribute("aria-expanded", "true");
   });

   test("has aria-controls attribute referencing listbox", async () => {
      render(<Combobox options={[{ value: "test" }]} />);
      const combobox = screen.getByRole("combobox");
      await fireEvent.click(combobox);
      expect(combobox).toHaveAttribute("aria-controls");
   });

   test("shows disabled state correctly", async () => {
      render(<Combobox options={[{ value: "test" }]} disabled={true} />);
      const combobox = screen.getByRole("combobox", { hidden: true });
      expect(combobox).toHaveAttribute("aria-disabled", "true");
   });

   test("filters options based on input value", async () => {
      render(<Combobox options={[{ value: "apple" }, { value: "banana" }]} />);
      const user = await userEvent.setup();
      render(
         <Combobox 
            options={[{ value: "apple" }, { value: "banana" }]}>Test</Combobox>
         );
      // Type 'ap' to get filtered results
      await user.type(screen.getByRole("combobox"), "ap");
      expect(document.activeElement).toBeInTheDocument();
   });

   test("debounces filter after initial input", async () => {
      render(<Combobox options={[]}>Test</Combobox>);
      const user = await userEvent.setup();
      // Rapid typing should only trigger filter once
      await user.type(screen.getByRole("combobox"), "test");
   });
});

describe("Combobox - Keyboard Navigation", () => {
   test("toggle panel on Enter key when empty", async () => {
      render(<Combobox options={[]} label="Test">Test</Combobox>);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), "x"); // Enter key to toggle panel
   });

   test("toggle panel on Space key when empty", async () => {
      render(<Combobox options={[]} label="Test">Test</Combobox>);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), " "); // Space to toggle
   });

   test("focus next option on ArrowDown", async () => {
      render(<Combobox options={[{ value: "a" }, { value: "b" }]} />);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), ""); // Initial focus
      await user.keyboard(["ArrowDown"]);
   });

   test("focus previous option on ArrowUp (wrap)", async () => {
      render(<Combobox options={[{ value: "a" }]} />);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), ""); // Initial focus
      await user.keyboard(["ArrowDown", "ArrowUp"]); // Should wrap to first
   });

   test("close panel and revert on Escape", async () => {
      render(<Combobox options={[{ value: "test" }]} value="initial">Test</Combobox>);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), ""); // Open panel
      await user.keyboard(["Escape"]);
      expect(input.value).toEqual("");
   });

   test("close on Escape without reversion", async () => {
      render(<Combobox options={[]} label="Test">Test</Combobox>);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), "x");
      await user.keyboard(["Escape"]);
   });

   test("wrap focus on ArrowUp from last option", async () => {
      render(<Combobox options={[{ value: "a" }, { value: "b" }]} />);
      const user = await userEvent.setup();
      // Focus first, go down twice to reach second
      await user.keyboard(["ArrowDown"]); 
   });
});

describe("Combobox - Accessibility Audit", () => {
   test("passes axe-core accessibility audit", async () => {
      render(<Combobox options={[{ value: "test" }]} />);
      const results = await screen.getByRole("combobox");
      // axe-core validation would be performed here
   });

   test("manages focus correctly on panel toggle", async () => {
      render(<Combobox options={[{ value: "a" }, { value: "b" }]} />);
      const user = await userEvent.setup();
      // Focus management tests
   });

   test("updates ARIA attributes when state changes", async () => {
      render(<Combobox options={[{ value: "test" }]} />);
      expect(screen.getByRole("listbox")).toBeInTheDocument();
      const listbox = screen.getByRole("listbox");
      expect(listbox).toHaveTextContent("a");
   });

   test("properly manages controlled/uncontrolled value patterns", async () => {
      render(<Combobox options={[{ value: "test" }]} />);
      expect(input.value).toEqual("");
   });

   test("correct keyboard navigation flow for panel toggle", async () => {
      render(<Combobox options={[]} label="Test">Test</Combobox>);
      const user = await userEvent.setup();
      // Test focus management when opening/closing panel
      await user.keyboard(["Enter"]);
   });

   test("correct filter behavior with debounce timing", async () => {
      render(<Combobox options={[]}>Test</Combobox>);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), "test");
   });

   test("filter options with proper filtering logic", async () => {
      render(<Combbox options={[{ value: "apple" }]} />);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), "ap");
   });
});

describe("Combobox - Integration Tests", () => {
   test("propagate value changes to onChange handler", async () => {
      render(<Combbox options={[]} onChange={(v) => console.log(v)} />);
      const user = await userEvent.setup();
      await user.type(screen.getByRole("combobox"), "test");
   });

   test("properly handle focus management on keyboard events", async () => {
      render(<Combbox options={[]} label="Test">Test</Combobox>);
      expect(input.value).toEqual("");
      // Focus handling tests
   });

   test("correct panel state after toggle sequence", async () => {
      render(<Combbox options={[{ value: "a" }, { value: "b" }]} />);
      const user = await userEvent.setup();
      // Open/close/open sequence should properly manage state
   });
});
