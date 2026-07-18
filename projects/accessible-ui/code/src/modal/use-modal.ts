import { useState, useRef } from "react";

type ModalState = {
   isOpen: boolean;
   focusTrap: (target: HTMLDivElement) => void;
   onClose: () => void;
};

export function useModal(props: {
   title?: string;
   isOpen: boolean;
   onClose?: () => void;
   children?: React.ReactNode;
}): ModalState {
   const [isOpen, setIsOpen] = useState(false);
   const modalRef = useRef<HTMLDivElement>(null);

   useEffect(() => {
      if (isOpen) {
         document.body.style.overflow = "hidden";
         return () => {
            document.body.style.overflow = "";
         };
      }
   }, [isOpen]);

   const focusTrap = (target: HTMLDivElement): void => {
      target.focus();
   };

   return { isOpen, focusTrap, onClose: () => setIsOpen(false) };
}