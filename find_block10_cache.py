import json
from pathlib import Path

cache_dir = Path("./data/llm_cache")

# Texte caractéristique du bloc 10
search_text = "Théorème des intervalles emboîtés"

print(f"Recherche dans {cache_dir}...")
print(f"Critère : '{search_text}'\n")

found = []

for txt_file in cache_dir.glob("*.txt"):
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        prompt = "\n".join(lines)

        if search_text in prompt:
            hash_name = txt_file.stem
            json_file = cache_dir / f"{hash_name}.json"
            with open(json_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            print(f"✅ TROUVÉ : {hash_name}")
            print(f"   Modèle : {meta.get('model')}")
            print(f"   Backend : {meta.get('backend')}")

            print(f"\n📄 Réponse du modèle :")
            print("=" * 80)
            print(prompt[:500])  # Premiers 500 caractères
            print("=" * 80)

            # Tenter de parser comme JSON
            try:
                parsed = json.loads(prompt)
                print("\n🔍 Équivalent statements :")
                equiv = parsed.get("equivalent_statements", [])
                if equiv:
                    for i, stmt in enumerate(equiv, 1):
                        print(f"   {i}. {stmt}")
                else:
                    print("   (liste vide)")
            except:
                print("\n⚠️  Impossible de parser le JSON")

            found.append(hash_name)
            print("\n" + "=" * 80 + "\n")

    except Exception as e:
        continue

if not found:
    print(f"❌ Aucun fichier trouvé contenant '{search_text}'")
    print("\nEssayez avec un autre critère de recherche, par exemple:")
    print("  - 'intervalles emboîtés'")
    print("  - 'suite décroissante de segments'")
else:
    print(f"\n✅ Trouvé {len(found)} fichier(s)")
    print(f"\nPour voir la réponse complète : cat ./data/llm_cache/")
    for _f in found:
        print(f"\n{_f}.txt")
