import sys, json
from client import PersonalVaultZeroKnowledgeSanitizer

def handle_mcp():
    vault = PersonalVaultZeroKnowledgeSanitizer()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(vault.run_privacy_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-personal-vault-zero-knowledge-sanitizer-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "sanitize_and_mask_pii", "description": "Mask PII and secrets with cryptographic placeholders.", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}}},
                    {"name": "rehydrate_sanitized_text", "description": "Restore original secrets on client side.", "inputSchema": {"type": "object", "properties": {"model_response": {"type": "string"}}}},
                    {"name": "run_privacy_benchmark", "description": "Run zero-knowledge privacy benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "sanitize_and_mask_pii":
                    res = vault.sanitize_and_mask_pii(args.get("text", ""))
                elif tname == "rehydrate_sanitized_text":
                    res = vault.rehydrate_sanitized_text(args.get("model_response", ""))
                else:
                    res = vault.run_privacy_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
