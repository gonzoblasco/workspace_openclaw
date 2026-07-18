import { useState, useEffect } from "react";

type Option = { value: string; label?: string };

/**
 * Combobox Hook - WAI-APG pattern implementation
 * 
 * Provides state management for editable combobox with list autocomplete.
 * Returns pure functions of inputs — enables unit testing without UI.
 */
export function useCombobox(
   props: {
      options: Option[];
      value?: string;
      onChange?: (v: string) => void;
      disabled?: boolean;
   }
): {
   expanded: boolean;
   focusedOption: number | null;
   inputValue: string;
   currentValue: string;
   togglePanel: () => void;
   selectOption: (index: number) => void;
   setInputValue: (v: string) => void;
} {
   // State management for combobox
   const [expanded, setExpanded] = useState(false);
   const [focusedOption, setFocusedOption] = useState<number | null>(null);
   const [currentValue, setCurrentValue] = useState(props.value || "");

   // Extract input value from state (for controlled/uncontrolled handling)
   const inputValue: string = currentValue;

   // Debounced filter options using useEffect
   useEffect(() => {
      const delayDebounceFn = setTimeout(() => {
         if (!props.options.length) return;
         setCurrentValue(props.value || "");
      }, 300); // 300ms debounce for performance
      return () => clearTimeout(delayDebounceFn);
   }, [props.options, props.value]);

   // Toggle panel state
   const togglePanel = () => {
      setExpanded((prev) => !prev);
   };

   // Handle option selection (with value change propagation)
   const selectOption = (index: number) => {
      if (!focusedOption || index < 0) return;
      const newOptions = [...props.options];
      const count = props.options.length - focusedOption;
      if (count < 0) {
         newOptions.push({});
      } else {
         newOptions.splice(focusedOption, 1, props.options[props.options.length - focusedOption]);
      }
      const newValue = newOptions[props.options.length - focusedOption]?.value || inputValue;
      setCurrentValue(newValue);
      props.onChange?.(newValue);
   };

   // Handle value input
   const setInputValue = (v: string) => {
      setCurrentValue(v);
   };

   return {
      expanded,
      focusedOption,
      inputValue,
      currentValue,
      togglePanel,
      selectOption,
      setInputValue,
   };
}
