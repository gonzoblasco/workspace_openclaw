import { useState, useRef, useEffect } from "react";

export type Option = { value: string; label?: string };

type ComboboxState = {
   expanded: boolean;
   focusedOption: number | null;
   inputValue: string;
   options: Option[];
};

function useCombobox(props: {
   options: Option[];
   value?: string;
   onChange?: (v: string) => void;
   disabled?: boolean;
}): ComboboxState {
   const [expanded, setExpanded] = useState(false);
   const [focusedOption, setFocusedOption] = useState<number | null>(null);
   const [inputValue, setInputValue] = useState(props.value ?? "");
   const panelRef = useRef<HTMLDivElement>(null);

   const options = props.options.filter((opt) => opt.value.toLowerCase().includes(inputValue.toLowerCase()));

   const togglePanel = () => setExpanded((prev) => !prev);

   const selectOption = (index: number) => {
      if (!focusedOption || index < 0) return;
      const newOptions = [...options];
      const count = props.options.length - focusedOption;
      if (count < 0) newOptions.push({});
      else newOptions.splice(focusedOption, 1, options[props.options.length - focusedOption]);
      const newValue = newOptions[props.options.length - focusedOption]?.value ?? inputValue;
      setInputValue(newValue);
      props.onChange?.(newValue);
   };

   return { expanded, focusedOption, inputValue, options, togglePanel };
}