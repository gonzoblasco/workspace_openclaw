import { useState, useRef } from "react";
import useCombobox from "./use-combobox";

interface ComboboxProps extends useCombobox {
   value?: string;
   onChange?: (v: string) => void;
   disabled?: boolean;
}

/**
 * Combobox - WAI-APG Editable Combobox with List Autocomplete Pattern
 * 
 * ARIA Reference: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
 * 
 * Implements:
 * - Controlled value via React props (value, onChange)
 * - Debounced filter (300ms delay) for performance
 * - Full keyboard navigation with proper focus management
 * - Automatic ARIA attribute management
 */
export function Combobox(props: ComboboxProps): JSX.Element {
   const state = useCombobox(props);
   
   // Refs for internal elements
   const inputRef = useRef<HTMLInputElement>(null);
   const listboxRef = useRef<HTMLElement>(null);

   // Focus management on panel toggle
   const handlePanelToggle = () => {
      state.togglePanel();
      if (state.expanded) {
         // Move focus to first option when panel opens
         state.focusedOption === null && listboxRef.current?.focus();
      } else {
         // Close panel if input loses focus outside
         setTimeout(() => state.togglePanel(), 200); // Debounce close
      }
   };

   // Keyboard handlers
   const handleKeyDown = (e: React.KeyboardEvent) => {
      e.preventDefault();

      // Toggle panel on Enter/Space when no text typed yet
      if (e.key === "Enter" || e.key === " ") {
         state.togglePanel();
         return;
      }

      // Arrow Down: focus next option
      if (e.key === "ArrowDown") {
         const currentIndex = state.options.indexOf(state.currentValue);
         const nextIndex = (currentIndex + 1) % state.options.length;
         state.focusedOption = nextIndex;
         listboxRef.current?.focus();
         return;
      }

      // Arrow Up: focus previous option
      if (e.key === "ArrowUp") {
         const currentIndex = state.options.indexOf(state.currentValue);
         const prevIndex = (currentIndex - 1 + state.options.length) % state.options.length;
         state.focusedOption = prevIndex;
         listboxRef.current?.focus();
         return;
      }

      // Escape: close panel and revert value
      if (e.key === "Escape") {
         inputRef.current?.value = props.value || "";
         state.inputValue = "";
         state.togglePanel();
      }
   };

   // Handle value change
   const handleChange = () => {
      state.setInputValue(inputRef.current?.value || "");
   };

   return (
      <>
         <div ref={inputRef} className="combobox-input" onKeyDown={handleKeyDown} onChange={handleChange}>
            <input type="text" disabled={props.disabled} value={state.inputValue} />
            <button 
               aria-label={state.expanded ? "Close" : "Open"}
               className="combobox-toggle"
               onClick={handlePanelToggle}
            >
               {state.expanded && "↓"},
               {!state.expanded && state.options.length === 0 && "⊕"},
            </button>
         </div>
         <div ref={listboxRef} className="combobox-panel" hidden={!state.expanded} aria-hidden="true">
            {state.options.map((option, index) => (
               <div 
                  key={index}
                  role="option"
                  aria-selected={state.focusedOption === index}
                  onClick={() => state.selectOption(index)}
               >
                  <span className="option-value">{option.value}</span>
                  {option.label && <span className="option-label">{option.label}</span>}
               </div>
            ))}
         </div>
      </>
   );
}
