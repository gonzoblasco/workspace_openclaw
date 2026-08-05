import { useState, useRef, useEffect } from 'react';

function useOutsideClick(ref, callback) {
  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        callback();
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [ref, callback]);
}

export default function Dropdown({ trigger, children }) {
  const [show, setShow] = useState(false);
  const wrapperRef = useRef(null);

  useOutsideClick(wrapperRef, () => setShow(false));

  return (
    <div className="dropdown">
      <div>
        <div className="trigger" onClick={() => setShow(!show)}>
          {trigger}
        </div>
        <div ref={wrapperRef}>
          {show && <div className="content">{children}</div>}
        </div>
      </div>
    </div>
  );
}
