"""
Diagnostic : Vérifier si l'extraction sémantique a été appelée pour le bloc 10
"""

import json
from pathlib import Path

cache_dir = Path("./data/llm_cache")

# Chercher les appels d'extraction (task_name="extraction")
print("=" * 80)
print("DIAGNOSTIC : Recherche des appels d'extraction sémantique")
print("=" * 80)

extraction_calls = []

for json_file in cache_dir.glob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # Vérifier si c'est un appel d'extraction
        model = meta.get("model", "")
        prompt = meta.get("prompt", "")

        # Les extractions utilisent mimo ou mixtral
        is_extraction = "mimo" in model or "mixtral" in model

        # Et contiennent "Extract the theorem" ou "Extract the definition"
        is_extraction = is_extraction and ("Extract the" in prompt)

        if is_extraction and "Il est équivalent de dire que" in prompt:
            hash_name = json_file.stem
            response_file = cache_dir / f"{hash_name}.txt"
            equi_st = prompt.lower().find("equivalent")
            print(f"\t {prompt[equi_st:equi_st+100]}")

            extraction_calls.append(
                {"hash": hash_name, "model": model, "response_file": response_file}
            )
    except:
        continue

if not extraction_calls:
    print("\n❌ AUCUN appel d'extraction trouvé pour le bloc 10 !")
    print("\nCela signifie que :")
    print("1. Le bloc n'a pas le bon 'kind' (theorem/proposition/lemma/corollary)")
    print("2. OU l'extraction a été skippée pour une raison")
    print(
        "\n💡 Solution : Vérifiez le 'kind' du bloc dans l'UI (onglet 'Processed Results')"
    )
else:
    print(f"\n✅ Trouvé {len(extraction_calls)} appel(s) d'extraction\n")

    for i, call in enumerate(extraction_calls, 1):
        print(f"=== Appel #{i} ===")
        print(f"Hash : {call['hash'][:16]}...")
        print(f"Modèle : {call['model']}")

        if call["response_file"].exists():
            response = call["response_file"].read_text(encoding="utf-8")

            # Parser la réponse
            try:
                parsed = json.loads(response)
                print("\n📄 Réponse JSON :")
                print(f"   name: {parsed.get('name')}")
                print(f"   conclusion: {parsed.get('conclusion', '')[:60]}...")

                equiv = parsed.get("equivalent_statements", [])
                print(f"   equivalent_statements: {len(equiv)} item(s)")

                if equiv:
                    for j, stmt in enumerate(equiv, 1):
                        print(f"      {j}. {stmt}")
                else:
                    print("      ❌ LISTE VIDE !")
                    print(
                        "\n   → Le modèle n'a pas extrait les propositions équivalentes"
                    )
                    print(
                        "   → Problème : prompt pas assez clair OU modèle trop faible"
                    )
            except Exception as e:
                print(f"\n❌ Erreur de parsing JSON : {e}")
                print(f"\nRéponse brute (300 chars) :\n{response[:300]}")

        print(f"\n💾 Fichier : ./data/llm_cache/{call['hash']}.txt")
        print()

print("=" * 80)
