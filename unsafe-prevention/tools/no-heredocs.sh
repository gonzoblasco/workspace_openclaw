#!/bin/bash
# No-Heredocs Protection Tool
# ENFORCES echo-based file writing over heredocs to avoid bash parsing issues

usage() {
    cat << 'USAGE'
   === NO-HEREDOC TOOL (2026-07-17+ VERSION) ===
  
  RULE: Always use heredocs WITHOUT backticks or code blocks
  
  EXAMPLES WORK:
     # Heredoc with plain text
    cat > file.md << 'EOF'
Line 1
Line 2
Line 3
EOF
    
     # Variable expansion inside heredoc
    cat > script.sh << EOF
#!/bin/bash
curl http://localhost:11434/api/generate
echo "Hello world"
EOF
    
     # Using $() syntax instead of backticks
    cat > notes.txt << EOF
Line 1
Line 2
$VAR
EOF

  EXAMPLES DON'T USE:
     # Backticks in heredoc will fail
    cat > file.sh << 'EOF'
\`\`\`bash
curl http://localhost:11434/api/generate
\`\`\`
EOF
    
     # Markdown code blocks in heredoc
    cat > docs.md << 'EOF'
\`\`\`markdown
Here's the doc
\`\`\`
EOF

  WORKAROUND FOR TECHNICAL SCRIPTS:
    Write technical scripts with your text editor (vi/nano)
    Then use: cat > filename.sh << SHELL (no code blocks)
  
  EXAMPLE PROPER:
    echo '#!/bin/bash' > script.sh
    echo 'curl http://localhost:11434/api/generate' >> script.sh
    
    OR write in editor then:
      cat > filename.sh << SHELL
       # Shell-only content, no backticks
      SHELL

USAGE
}

echo "=== NO-HEREDOC TOOL ==="
echo "Version: 2026.07.17+ (Heredoc-safe edition)"
echo ""

usage
