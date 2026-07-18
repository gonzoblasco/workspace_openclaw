import { render, screen, fireEvent } from "@testing-library/react";
import { axe } from "jest-axe";
import userEvent from "@testing-library/user-event";
import Modal from "../Modal";

describe("Modal", () => {
   describe("rendering", () => {
      test("has dialog ARIA role", async () => {
         render(<Modal isOpen={true} title="Test">Content</Modal>);
         const element = screen.getByRole("dialog");
         expect(element).toBeInTheDocument();
      });

      test("shows content when opened", async () => {
         render(<Modal isOpen={false}>Test</Modal>);
         await fireEvent.click(screen.getByRole("button"));
         const h2 = screen.getByRole("heading", { name: "Test" });
         expect(h2).toBeInTheDocument();
      });
   });

   describe("keyboard", () => {
      test("close on Escape key", async () => {
         render(<Modal isOpen={true} onClose={() => console.log("closed")}>Content</Modal>);
         const user = await userEvent.setup();
         await user.keyboard(["Escape"]);
         expect(document.activeElement).not.toBe(screen.getByRole("dialog"));
      });

      test("trap focus within dialog", async () => {
         render(<Modal isOpen={true} onClose={() => console.log()}>
            <button role="button">Test</button>
         </Modal>);
         const user = await userEvent.setup();
         screen.focus(
            screen.getByRole("button")
          ); // Initial focus
         fireEvent.keyDown(screen.getByText("Test")); // Tab
         expect(document.activeElement).closest(".modal-content").toBeTruthy();
      });
    });

   describe("axe audit", () => {
      test("passes axe-core audit", async () => {
         render(<Modal isOpen={true} title="Test" onClose={() => {}}>Content</Modal>);
         const results = await axe(screen.getByRole("dialog"));
         expect(results).toHaveNoViolations();
      });
    });
});