import { useState, useRef } from "react";
import useCombobox from "./use-combobox";

interface ComboboxProps extends useCombobox {
   value?: string;
   onChange?: (v: string) => void;
}

export function Combobox(props: ComboboxProps): JSX.Element {
   const state = useCombobox(props);
   return <div>{/* component implementation */}</div>;
}