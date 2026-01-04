"""
Lister toutes les réponses en cache avec equivalent_statements NON VIDE
"""

import json
from pathlib import Path

cache_dir = Path("./data/llm_cache")

print("=" * 100)
print("RECHERCHE : Extractions avec equivalent_statements NON VIDE")
print("=" * 100)

found_with_equiv = []
found_without_equiv = []

for json_file in cache_dir.glob("*.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        model = meta.get("model", "")
        prompt = meta.get("prompt", "")

        # Vérifier si c'est un appel d'extraction
        is_extraction = (
            "Extract the theorem" in prompt
            or "Extract the definition" in prompt
            or "Extract the formula" in prompt
        )

        if not is_extraction:
            continue

        hash_name = json_file.stem
        response_file = cache_dir / f"{hash_name}.txt"

        if not response_file.exists():
            continue

        response = response_file.read_text(encoding="utf-8")

        try:
            parsed = json.loads(response)

            # Vérifier s'il y a des equivalent_statements
            equiv = parsed.get("equivalent_statements", [])

            if equiv and len(equiv) > 0:
                # Extraire le nom du bloc depuis le prompt
                block_name = "N/A"
                if 'name":' in response:
                    try:
                        name_val = parsed.get("name", "N/A")
                        block_name = name_val if name_val else "N/A"
                    except:
                        pass

                found_with_equiv.append(
                    {
                        "hash": hash_name,
                        "model": model,
                        "name": block_name,
                        "equiv_count": len(equiv),
                        "equiv": equiv,
                        "conclusion": parsed.get("conclusion", "N/A"),
                    }
                )
            else:
                # Pour stats : compter ceux sans
                found_without_equiv.append(hash_name)
        except:
            # Pas du JSON valide
            continue

    except Exception as e:
        continue

# === AFFICHAGE DES RÉSULTATS ===
print(f"\n📊 STATISTIQUES :")
print(f"   - Extractions avec equivalent_statements: {len(found_with_equiv)}")
print(f"   - Extractions sans equivalent_statements: {len(found_without_equiv)}")
print(
    f"   - Total extractions analysées: {len(found_with_equiv) + len(found_without_equiv)}"
)

if found_with_equiv:
    print(f"\n{'='*100}")
    print(f"✅ BLOCS AVEC ÉQUIVALENCES DÉTECTÉES ({len(found_with_equiv)})")
    print(f"{'='*100}")

    for i, item in enumerate(found_with_equiv, 1):
        print(f"\n#{i} - {item['name']}")
        print(f"   Hash : {item['hash'][:16]}...")
        print(f"   Modèle : {item['model']}")
        print(f"   Conclusion : {item['conclusion'][:80]}...")
        print(f"   Nombre d'équivalences : {item['equiv_count']}")
        print(f"   Équivalences extraites :")
        for j, eq in enumerate(item["equiv"], 1):
            print(f"      {j}. {eq[:100]}{'...' if len(eq) > 100 else ''}")
        print(f"\n   💾 Fichier : ./data/llm_cache/{item['hash']}.txt")

    print(f"\n{'='*100}")
    print(
        "✅ CONCLUSION : Le modèle PEUT extraire des équivalences dans certains cas !"
    )
    print("💡 Analyser ces cas pour comprendre ce qui diffère du bloc 10.")
else:
    print(f"\n{'='*100}")
    print("❌ AUCUNE extraction avec equivalent_statements trouvée !")
    print("{'='*100}")
    print("\nCela signifie que :")
    print("1. Le modèle n'a JAMAIS réussi à extraire des équivalences")
    print("2. OU le corpus traité ne contient pas de théorèmes d'équivalence")
    print("3. OU le prompt n'est pas assez clair pour ce modèle particulier")
    print("\n💡 Recommandations :")
    print("   - Tester manuellement avec un modèle plus puissant (Gemini/Claude)")
    print("   - Ou simplifier drastiquement les instructions d'équivalence")

print(f"\n{'='*100}")
