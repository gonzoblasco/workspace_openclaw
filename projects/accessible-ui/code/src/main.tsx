import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
   <React.StrictMode>
      <>
         <Combobox />
         <Modal title="Test Modal" />
         <Tabs label="Tabs Group">
            <TabPanel value={0} label="Item 1">Content 1</TabPanel>
            <TabPanel value={1} label="Item 2">Content 2</TabPanel>
            <TabPanel value={2} label="Item 3">Content 3</TabPanel>
         </Tabs>
      </>
   </React.StrictMode>
);