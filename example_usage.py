from client import PersonalVaultZeroKnowledgeSanitizer
import json

vault = PersonalVaultZeroKnowledgeSanitizer()
print("=== PERSONAL VAULT ZERO-KNOWLEDGE SANITIZER BENCHMARK ===")
res = vault.run_privacy_benchmark()
print(json.dumps(res, indent=2))
