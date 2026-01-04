import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

cache_dir = Path("./data/llm_cache")

# Texte du bloc 10
block_text = "Il est équivalent de dire que"

print(f"Recherche dans {cache_dir}...")
print("=" * 80)

# Grouper par modèle (proxy pour le type de tâche)
results_by_model = defaultdict(list)

for json_file in cache_dir.glob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        prompt = meta.get("prompt", "")

        # Chercher le texte du bloc dans le PROMPT (pas le system)
        if block_text in prompt:
            hash_name = json_file.stem
            response_file = cache_dir / f"{hash_name}.txt"

            model = meta.get("model", "unknown")

            # Déterminer la tâche à partir du modèle
            task_type = "unknown"
            if "mistral-7b" in model:
                task_type = "validation/linking"
            elif "mimo" in model or "mixtral" in model:
                task_type = "extraction"

            results_by_model[model].append(
                {
                    "hash": hash_name,
                    "task": task_type,
                    "backend": meta.get("backend"),
                    "response_file": response_file,
                    "mtime": json_file.stat().st_mtime,
                }
            )

    except Exception as e:
        continue

# Afficher les résultats
if not results_by_model:
    print("❌ Aucun fichier trouvé avec le texte du bloc")
    print("\n💡 Le cache peut avoir été vidé ou le bloc n'a pas encore été traité.")
else:
    for model, entries in sorted(results_by_model.items()):
        # Trier par date
        entries.sort(key=lambda x: x["mtime"], reverse=True)

        print(f"\n{'='*80}")
        print(f"🤖 MODÈLE : {model}")
        print(f"📋 Tâche probable : {entries[0]['task']}")
        print(f"{'='*80}")

        for i, entry in enumerate(entries, 1):
            mtime = datetime.fromtimestamp(entry["mtime"])
            print(f"\n#{i} Hash : {entry['hash'][:16]}...")
            print(f"   Date : {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

            if entry["response_file"].exists():
                response = entry["response_file"].read_text(encoding="utf-8")

                print(f"\n📄 Réponse (300 premiers caractères) :")
                print("-" * 80)
                print(response[:300])
                print("-" * 80)

                # Tenter de parser comme JSON
                try:
                    parsed = json.loads(response)
                    if "equivalent_statements" in parsed:
                        print(f"\n🎯 EXTRACTION TROUVÉE !")
                        print(f"   - name: {parsed.get('name', 'N/A')}")
                        print(
                            f"   - conclusion: {parsed.get('conclusion', 'N/A')[:60]}..."
                        )
                        equiv = parsed.get("equivalent_statements", [])
                        print(f"   - equivalent_statements: {len(equiv)} item(s)")
                        for j, stmt in enumerate(equiv, 1):
                            print(f"      {j}. {stmt[:70]}...")
                except:
                    pass

            print(f"\n💾 Fichier : ./data/llm_cache/{entry['hash']}.txt")

    total = sum(len(v) for v in results_by_model.values())
    print(f"\n{'='*80}")
    print(f"✅ Total : {total} fichier(s) trouvé(s)")
