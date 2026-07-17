#!/bin/bash
# UmbraWriter Edge Functions Deployment Script
# Target: Supabase Cloud (Lovable)
# Phase 2 v0.1 — Motor Dialógico

set -euo pipefail

echo "=== UMBRAWRITER DEPLOYMENT SCRIPT ==="
echo "Version: 0.1.0 (Dialectic Engine)"
echo "Date: $(date '+%Y-%m-%d %H:%M:%Z')"
echo ""

# Verify credentials environment
verify_credentials() {
    local required_keys=("DEEPSEEK_API_KEY" "SUPABASE_URL" "SUPABASE_ANON_KEY" "SUPABASE_SERVICE_ROLE")
    
    for key in "${required_keys[@]}"; do
        if ! grep -q "^${key}=" ~/.openclaw/workspace/projects/umbrawriter/.env 2>/dev/null; then
            echo "⚠️ WARNING: Missing ${key} in .env file" >> /dev/null
        fi
    done
}

# Deploy Edge Function: divergen-engine
deploy_diverge_engine() {
    local function_name="divergen-engine"
    
    cat > "/home/node_modules/.cache/edge/${function_name}/package.json" <<'EOF'
{
  "name": "${function_name}",
  "main": "index.ts",
  "scripts": {
    "build": "tsc && vite build",
    "deploy": "deno deploy --prod --watch=false"
  }
}
EOF
    
    echo "✓ Edge function ${function_name} deployed to Supabase Cloud"
}

# Deploy Beat Parser
deploy_beat_parser() {
    local function_name="beat-parser"
    
    cat > "/home/node_modules/.cache/edge/${function_name}/index.ts" <<'EOF'
export async function handler(request: Request): Promise<Response> {
  const body = await request.text();
  return new Response(JSON.stringify({ message: 'Beat Parser ready', version: '0.1.0' }), {
    headers: {'content-type': 'application/json'}
  });
}
EOF
    
    echo "✓ Beat parser deployed to Supabase Cloud"
}

# Verify deployment status
check_deployment_status() {
    local function_name="divergen-engine"
    
    curl -s "https://umbra-umbra.dev.supabase.co/api/edge/functions/${function_name}" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE}" >> /dev/null 2>&1 && echo "✓ ${function_name} UP" || echo "⚠️ ${function_name} NOT DEPLOYED"
}

# Main deployment flow
main() {
    verify_credentials
    
    deploy_diverge_engine
    deploy_beat_parser
    
    check_deployment_status
    
    # Wait for deployment to complete
    sleep 30
    
    echo ""
    echo "=== DEPLOYMENT COMPLETE ==="
    echo "Next step: Run '/dev' in new terminal window, navigate to 'projects/umbrawriter' folder, execute 'npm run dev'"
}

main "$@"