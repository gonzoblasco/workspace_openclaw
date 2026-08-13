# Data Model — Kanam Story

> Modelo de dominio. Se implementa sobre IndexedDB (como `sudolab`), un store por entidad vía `idb`.

## Núcleo

### Project
```ts
interface Project {
  id: string;
  title: string;
  description: string;
  // brújula
  premise: string;          // la idea en 1-2 frases
  promise: string;          // qué le prometemos al lector
  theme: string;            // tema central
  protagonist: string;      // id de Character protagonista
  pov: string;              // 1a/3a/...
  createdAt: Date;
  updatedAt: Date;
}
```

### Chapter
```ts
interface Chapter {
  id: string;
  projectId: string;
  title: string;
  summary: string;
  position: number;
  beats: Beat[];            // mapa de beats del capítulo
  createdAt: Date;
  updatedAt: Date;
}
```

### Scene
```ts
interface Scene {
  id: string;
  chapterId: string;
  title: string;
  position: number;
  beats: Beat[];            // beats de la escena
  content: string;          // manuscrito (tipTap JSON)
  createdAt: Date;
  updatedAt: Date;
}
```

### Beat (mapa de estructura)
```ts
interface Beat {
  id: string;
  kind: 'inciting' | 'rising' | 'climax' | 'falling' | 'resolution' | 'custom';
  title: string;
  description: string;      // qué pasa en este beat
  notes: string;            // intención, tono, elementos a cuidar
  characters: string[];     // ids de Character involucrados
  location: string;         // id de WorldEntity (lugar)
  status: 'draft' | 'done' | 'revising';
  source: 'manual' | 'ai';  // definido a mano o sugerido por IA
  position: number;
}
```

### Character
```ts
interface Character {
  id: string;
  projectId: string;
  name: string;
  role: string;             // protagonista, antagonista, secundario
  age: string;
  appearance: string;
  personality: string;
  voice: string;            // cómo habla (estilo de diálogo)
  wants: string;            // qué quiere
  needs: string;            // qué necesita de verdad
  backstory: string;
  goals: string[];          // arco: objetivos
  arc: string;              // descripción del arco
  updatedAt: Date;
}
```

### WorldEntity
```ts
interface WorldEntity {
  id: string;
  projectId: string;
  kind: 'place' | 'lore' | 'rule' | 'object' | 'other';
  name: string;
  description: string;
  updatedAt: Date;
}
```

### StoryBible (vista auto-generada)
```ts
interface StoryBible {
  projectId: string;
  sections: {
    summary: string;    // resumen del manuscrito
    themes: string;
    characters: string;
    world: string;
    rules: string;
  };
  overrides: Record<string, string>;  // override manual por sección
  generatedAt: Date;
}
```

## Chat (lo nuevo — el corazón)

### Conversation
```ts
interface Conversation {
  id: string;
  projectId: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### Message
```ts
interface Message {
  id: string;
  conversationId: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  // acciones que el agente ejecutó sobre el contenido
  actions: ContentAction[];
  createdAt: Date;
}
```

### ContentAction (el agente "tiene manos")
```ts
type ContentAction =
  | { type: 'rewrite_scene'; sceneId: string; before: string; after: string; summary: string }
  | { type: 'update_beat'; beatId: string; changes: Partial<Beat>; summary: string }
  | { type: 'add_beat'; chapterId: string; beat: Beat; summary: string }
  | { type: 'update_character'; characterId: string; changes: Partial<Character>; summary: string }
  | { type: 'add_character'; character: Character; summary: string }
  | { type: 'update_world'; entityId: string; changes: Partial<WorldEntity>; summary: string }
  | { type: 'update_bible'; section: keyof StoryBible['sections']; value: string; summary: string }
  | { type: 'append_scene'; chapterId: string; content: string; summary: string };
```

## Relaciones

```
Project 1─* Chapter 1─* Scene 1─1 Content (tipTap)
  │           └── Beats[]            Beats[]
  │
  ├──1─* Character
  ├──1─* WorldEntity
  ├──1─1 StoryBible
  └──1─* Conversation 1─* Message ─── ContentAction[]
```

## Persistencia

- IndexedDB vía `idb`, un store por entidad (patrón `sudolab/lib/db.ts`).
- **Nuevo store:** `conversations`, `messages` (con `actions` embebidas o store propio).
- Los `ContentAction` deben ser **aplicables y reversibles** (para deshacer/aceptar/rechazar una propuesta del agente antes de que quede firme).
