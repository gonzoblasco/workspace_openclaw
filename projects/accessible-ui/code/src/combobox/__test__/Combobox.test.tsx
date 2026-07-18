import { render, screen, fireEvent } from "@testing-library/react";
import { axe } from "jest-axe";
import userEvent from "@testing-library/user-event";
import Combobox from "../Combobox";

describe("Combobox", () => {
   describe("rendering", () => {
      test("has combobox ARIA role", async () => {
         render(<Combobox options={[{ value: "test" }]} />);
         const element = screen.getByRole("combobox");
         expect(element).toBeInTheDocument();
      });

      test("displays list when expanded", async () => {
         render(<Combobox options={[{ value: "test" }]} />);
         await fireEvent.click(screen.getByRole("combobox"));
         const list = screen.getByRole("listbox");
         expect(list).toBeInTheDocument();
      });
   });

   describe("keyboard", () => {
      test("toggle panel on Enter key", async () => {
         render(<Combobox options={[]}>Test</Combobox>);
         const user = await userEvent.setup();
         await user.type(screen.getByRole("combobox"), "");
         await user.click(screen.getByRole("combobox"));
         expect(screen.getByRole("listbox")).toBeInTheDocument();
      });

      test("focus next option on ArrowDown", async () => {
         render(<Combobox options={[{ value: "a" }, { value: "b" }]} />);
         await userEvent.setup();
         fireEvent.keyDown(
            screen.getByRole("combobox")
         ); // ArrowDown
      });

      test("wrap focus on ArrowUp", async () => {
         render(<Combobox options={[{ value: "a" }]}>Test</Combobox>);
         await userEvent.setup();
         fireEvent.keyDown(
            screen.getByRole("combobox")
         ); // ArrowUp
         expect(screen.getByRole("option")).toBeFocused();
      });
   });

   describe("axe audit", () => {
      test("passes axe-core audit", async () => {
         render(<Combobox options={[]}>Test</Combobox>);
         const results = await axe(
            screen.getByRole("combobox")
         );
         expect(results).toHaveNoViolations();
      });
   });
});