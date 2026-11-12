import assert from "node:assert";
import { execSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const out = execSync(`node "${join(aqui, "caja-resuelta.mjs")}"`).toString();
const total = Number(out.trim().split("\n").pop().replace(/[^\d.]/g, ""));

assert.equal(total, 1512.5, `esperaba 1512.5 (1250 + IVA 21%), obtuve ${total}`);
console.log("test: pasa (IVA 21% aplicado)");
