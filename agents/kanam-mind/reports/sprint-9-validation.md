- Verificación de directorios de skills Hermes:
```
ls -d /Users/gonzoblasco/.openclaw/workspace/skills/hermes-* | wc -l
9
```
- Verificación de skills de patrones:
```
ls -d /Users/gonzoblasco/.openclaw/workspace/skills/sdd-agent-loop /Users/gonzoblasco/.openclaw/workspace/skills/verification-gates /Users/gonzoblasco/.openclaw/workspace/skills/trust-vocabulary-report 2>/dev/null | wc -l
3
```
- Conteo de archivos MD en fuentes Hermes SDD:
```
find ~/.openclaw/wiki/main/sources/hermes-sdd -name '*.md' | wc -l
83
```
