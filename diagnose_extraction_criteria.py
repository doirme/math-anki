"""
DIAGNOSTIC : Vérifier le 'kind' assigné à chaque bloc et voir lesquels sont extraits
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

# Simuler les kinds possibles
print("=" * 100)
print("DIAGNOSTIC : Critères d'extraction sémantique")
print("=" * 100)

print("\n📋 KINDS DE BLOCS QUI DÉCLENCHENT UNE EXTRACTION :")
print("   1. definition → _extract_definition()")
print("   2. theorem → _extract_theorem()")
print("   3. proposition → _extract_theorem()")
print("   4. lemma → _extract_theorem()")
print("   5. corollary → _extract_theorem()")
print("   6. formula → _extract_formula()")
print("   7. proof → _extract_proof()")
print("   8. exercise → _extract_exercise()")

print("\n❌ KINDS DE BLOCS IGNORÉS (pas d'extraction) :")
print("   - context")
print("   - example")
print("   - remark")
print("   - unknown")
print("   - Tout autre kind non listé ci-dessus")

print("\n" + "=" * 100)
print("VÉRIFICATION : Quel 'kind' a le bloc 10 ?")
print("=" * 100)

print("\n💡 Pour vérifier dans Streamlit :")
print("   1. Allez dans l'onglet 'Processed Results'")
print("   2. Cherchez le bloc contenant 'Il est équivalent de dire que'")
print("   3. Regardez l'expander : 'Block X: <KIND> - [tags]'")
print("   4. Notez le <KIND> affiché")

print("\n🔍 Si le kind n'est PAS dans la liste ci-dessus :")
print("   → Le bloc ne sera JAMAIS extrait sémantiquement")
print("   → Il faut vérifier le block_creator ou le block_validator")

print("\n📊 Pour un diagnostic complet, on peut :")
print("   1. Lister tous les blocs créés avec leur kind")
print("   2. Compter combien sont extraits vs ignorés")
print("   3. Identifier les blocs qui devraient être extraits mais ne le sont pas")

print("\n" + "=" * 100)
print("SCRIPT À EXÉCUTER DANS STREAMLIT")
print("=" * 100)

script = """
# Ajouter ce code dans streamlit_app.py après l'analyse (st.session_state.stage == "done")
if st.button("🔍 Diagnostic Extraction"):
    validated = st.session_state.validated_blocks
    
    extraction_kinds = {'theorem', 'proposition', 'lemma', 'corollary', 
                       'definition', 'formula', 'proof', 'exercise'}
    
    extracted_count = 0
    skipped_count = 0
    
    st.write("### Blocs par Kind :")
    for block in validated:
        kind = block.get('kind', 'unknown')
        is_extracted = kind in extraction_kinds
        
        with st.expander(f"{'✅' if is_extracted else '❌'} Block: {kind} - {block.get('tags', [])}"):
            st.write(f"**Kind:** {kind}")
            st.write(f"**Sera extrait:** {'OUI' if is_extracted else 'NON'}")
            st.text_area("Texte validé", block.get('validated_text', '')[:200], height=100)
        
        if is_extracted:
            extracted_count += 1
        else:
            skipped_count += 1
    
    st.write(f"**Résumé : {extracted_count} blocs extraits, {skipped_count} blocs ignorés**")
"""

print(script)
print("=" * 100)
