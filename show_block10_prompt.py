"""
Chercher dans le cache le prompt d'extraction pour le bloc 10
"""

import hashlib
import json
from pathlib import Path

cache_dir = Path("./data/llm_cache")

# Texte caractéristique du bloc 10
block_signature = "Il est équivalent de dire que 1. l'ensemble"

print("=" * 100)
print("RECHERCHE : Prompt d'extraction pour le bloc 10")
print("=" * 100)
print(f"Signature de recherche : '{block_signature[:50]}...'\n")

found = []

for json_file in cache_dir.glob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        prompt = meta.get("prompt", "")
        model = meta.get("model", "")

        # Vérifier si c'est une extraction de théorème
        is_theorem_extraction = "Extract the theorem" in prompt

        # Et que ça contient notre bloc
        has_block10 = block_signature in prompt

        if is_theorem_extraction and has_block10:
            hash_name = json_file.stem
            response_file = cache_dir / f"{hash_name}.txt"

            found.append(
                {
                    "hash": hash_name,
                    "model": model,
                    "prompt_file": json_file,
                    "response_file": response_file,
                }
            )
    except:
        continue

if not found:
    print("❌ Aucun prompt d'extraction trouvé pour le bloc 10")
    print("\nLe cache a peut-être été vidé ou le bloc n'a pas encore été traité.")
else:
    print(f"✅ Trouvé {len(found)} prompt(s) d'extraction\n")

    for i, item in enumerate(found, 1):
        print(f"{'='*100}")
        print(f"APPEL #{i}")
        print(f"{'='*100}")
        print(f"Hash : {item['hash']}")
        print(f"Modèle : {item['model']}")
        print(f"\nFichiers :")
        print(f"  - Prompt (metadata) : {item['prompt_file']}")
        print(f"  - Réponse (JSON)    : {item['response_file']}")

        # Lire et afficher le prompt
        with open(item["prompt_file"], "r", encoding="utf-8") as f:
            meta = json.load(f)

        prompt_full = meta.get("prompt", "")

        print(f"\n📄 PROMPT COMPLET ({len(prompt_full)} caractères) :")
        print("-" * 100)
        # Afficher les 1500 premiers caractères
        print(prompt_full[:1500])
        print("\n[...suite tronquée...]\n")
        print("-" * 100)

        # Chercher la section sur les équivalences
        if "EQUIVALENCE THEOREMS" in prompt_full:
            idx = prompt_full.find("EQUIVALENCE THEOREMS")
            equiv_section = prompt_full[idx : idx + 500]
            print(f"\n🎯 SECTION ÉQUIVALENCES :")
            print("-" * 100)
            print(equiv_section)
            print("-" * 100)

        # Lire la réponse
        if item["response_file"].exists():
            response = item["response_file"].read_text(encoding="utf-8")

            print(f"\n📤 RÉPONSE DU MODÈLE :")
            print("-" * 100)
            print(response[:800])
            print("\n[...suite tronquée...]\n")
            print("-" * 100)

            # Parser la réponse
            try:
                parsed = json.loads(response)
                print(f"\n🔍 ANALYSE DE LA RÉPONSE :")
                print(f"  - name: {parsed.get('name')}")
                print(f"  - normalized_name: {parsed.get('normalized_name')}")
                print(f"  - conclusion: {parsed.get('conclusion', '')[:80]}...")

                equiv = parsed.get("equivalent_statements", [])
                print(f"  - equivalent_statements: {len(equiv)} item(s)")

                if equiv:
                    print("    ✅ EXTRAIT :")
                    for j, stmt in enumerate(equiv, 1):
                        print(f"      {j}. {stmt}")
                else:
                    print(
                        "    ❌ LISTE VIDE - Le modèle n'a pas détecté les équivalences !"
                    )
            except Exception as e:
                print(f"\n⚠️ Erreur de parsing : {e}")

print(f"\n{'='*100}")
