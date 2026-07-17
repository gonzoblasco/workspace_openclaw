import React from "react";

export interface DivergencePathsProps {
   paths: DivergencePath[];
   onSelect: (path: DivergencePath) => void;
}

interface DivergencePath {
   id: number;
   type: "sublime" | "comic" | "tragic";
   title: string;
   sample: string;
}

function DivergenceCard({ paths, onSelect }: DivergencePathsProps) {
 return (
 <div className="grid md:grid-cols-3 gap-4">
    {paths.map((path) => (
       <div
          key={path.id}
          className={`p-6 rounded-lg border-2 transition-all ${
             path.type === "sublime" ? "border-primary/50 bg-secondary" :
             path.type === "comic" ? "border-accent/50 bg-accent" :
            "border-destructive/50 bg-danger"
          }`}
       >
         <h3 className="font-bold text-lg mb-2">{path.title}</h3>
         <p className="text-sm text-muted-foreground mb-4">{path.sample}</p>
         <button onClick={() => onSelect(path)} className="px-4 py-2 bg-accent-primary text-white rounded-md">
          Generate Full Scene
        </button>
       </div>
     ))}
  </div>
 );
}

export default DivergenceCard;
