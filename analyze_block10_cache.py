import json
from collections import defaultdict
from pathlib import Path

cache_dir = Path("./data/llm_cache")

# Textes caractéristiques du bloc 10
search_patterns = [
    "Soit $\\{a_n; b_n\\}$ une suite décroissante de segments",
    "Il est équivalent de dire que",
    "intervalles emboîtés",
    "borne supérieure",
]

print(f"Recherche dans {cache_dir}...")
print("=" * 80)

# Grouper par type de tâche
results_by_task = defaultdict(list)

for json_file in cache_dir.glob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        prompt = meta.get("prompt", "")
        system = meta.get("system", "")

        # Chercher dans prompt et system
        full_text = prompt + " " + system

        # Vérifier si l'un des patterns est présent
        for pattern in search_patterns:
            if pattern in full_text:
                hash_name = json_file.stem
                response_file = cache_dir / f"{hash_name}.txt"

                # Déterminer le type de tâche
                task_type = "unknown"
                if "self-contained" in system.lower() or "validation" in system.lower():
                    task_type = "validation"
                elif "relationship" in system.lower() or "lien" in system.lower():
                    task_type = "linking"
                elif "extract" in system.lower() or "théorème" in system.lower():
                    task_type = "extraction"

                results_by_task[task_type].append(
                    {
                        "hash": hash_name,
                        "model": meta.get("model"),
                        "backend": meta.get("backend"),
                        "response_file": response_file,
                        "pattern": pattern,
                    }
                )
                break  # Un seul match par fichier

    except Exception as e:
        continue

# Afficher les résultats groupés
if not results_by_task:
    print("❌ Aucun fichier trouvé")
else:
    for task_type in ["validation", "extraction", "linking", "unknown"]:
        if task_type not in results_by_task:
            continue

        entries = results_by_task[task_type]
        print(f"\n{'='*80}")
        print(f"📋 TÂCHE : {task_type.upper()} ({len(entries)} fichier(s))")
        print(f"{'='*80}")

        for entry in entries:
            print(f"\n🔑 Hash : {entry['hash'][:16]}...")
            print(f"   Modèle : {entry['model']}")
            print(f"   Pattern trouvé : {entry['pattern'][:50]}...")

            if entry["response_file"].exists():
                response = entry["response_file"].read_text(encoding="utf-8")
                print(f"\n📄 Réponse (premiers 300 caractères) :")
                print("-" * 80)
                print(response[:300])
                print("-" * 80)

                # Pour extraction, essayer de parser le JSON
                if task_type == "extraction":
                    try:
                        parsed = json.loads(response)
                        print("\n🎯 Champs clés extraits :")
                        print(f"   - name: {parsed.get('name', 'N/A')}")
                        print(
                            f"   - normalized_name: {parsed.get('normalized_name', 'N/A')}"
                        )
                        print(
                            f"   - conclusion: {parsed.get('conclusion', 'N/A')[:80]}..."
                        )
                        equiv = parsed.get("equivalent_statements", [])
                        print(f"   - equivalent_statements: {len(equiv)} item(s)")
                        if equiv:
                            for i, stmt in enumerate(equiv, 1):
                                print(f"      {i}. {stmt[:60]}...")
                        else:
                            print("      (liste vide)")
                    except:
                        pass

            print(f"\n💾 Fichier complet : ./data/llm_cache/{entry['hash']}.txt")

    print(f"\n{'='*80}")
    total = sum(len(v) for v in results_by_task.values())
    print(f"✅ Total : {total} fichier(s) trouvé(s)")
    print(f"{'='*80}")
