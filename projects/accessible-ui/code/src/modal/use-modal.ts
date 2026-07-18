import { useState, useRef, useEffect } from "react";

type ModalProps = {
   title?: string;
   isOpen: boolean;
   onClose?: () => void;
};

/**
 * Modal Hook - WAI-APG Dialog pattern implementation
 * 
 * Returns pure functions for unit testing without full component setup.
 */
export function useModal(props: ModalProps): {
   isOpen: boolean;
   focusTrap: (target: HTMLDivElement) => void;
   onClose: () => void;
} {
   // Controlled open state
   const [isOpen, setIsOpen] = useState(false);

   // Refs for focus management
   const firstFocusableRef = useRef<HTMLElement>(null);
   const lastFocusableRef = useRef<HTMLElement>(null);

    // Track initial and current focusable elements
   useEffect(() => {
      if (!isOpen) return;

      // Store reference to modal content
      firstFocusableRef.current = document.activeElement;
      
      // Find first and last tabbable elements in dialog
      const dialogContent = props.children as HTMLElement;
      const focusables = dialogContent.querySelectorAll<HTMLElement>("button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])");
      
      if (focusables.length > 0) {
         firstFocusableRef.current = focusables[0];
         lastFocusableRef.current = focusables[focusables.length - 1];
      }
   }, [isOpen]);

    // Close modal with proper focus management
   const onClose = () => {
      setIsOpen(false);
       // Focus should return to previous element after close
      setTimeout(() => firstFocusableRef.current?.focus(), 500);
   };

   // Focus trap function for current dialog state
   const focusTrap = (target: HTMLElement): void => {
      target.focus();
    };

   return {
      isOpen,
      focusTrap,
      onClose,
   };
}
