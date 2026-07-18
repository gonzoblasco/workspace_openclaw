// Shared utility for ARIA attributes across components
import { useState } from "react";

/**
 * Helper for managing aria-expanded attribute on dynamic elements
 */
export function useAriaExpanded(expanded: boolean | null): JSX.AttributeValue {
   return { property: "aria-expanded", value: expanded ?? "false" as string };
}

/**
 * Helper for managing aria-selected attribute (required by WAI-APG)
 */
export function useAriaSelected(selected: boolean): JSX.AttributeValue {
   return { property: "aria-selected", value: selected ? "true" : "false" as string };
}

/**
 * Helper for managing focused option tracking
 * Used in Combobox component
 */
export interface UseComboboxState {
   expanded: boolean;
   focusedOption: number | null;
   inputValue: string;
   options: any[];
}
