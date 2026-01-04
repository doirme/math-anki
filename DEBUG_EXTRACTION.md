# Mode Debug pour l'Extraction Sémantique

## Activation

Pour activer le mode debug qui logue les prompts au lieu d'appeler le LLM :

```powershell
# Windows PowerShell
$env:DEBUG_EXTRACTION="true"
```

Ou dans le fichier `.env` :
```
DEBUG_EXTRACTION=true
```

## Utilisation

1. Activez le mode debug (voir ci-dessus)
2. Lancez Streamlit : `streamlit run src/ui/streamlit_app.py`
3. Traitez votre PDF normalement

## Résultat

Au lieu d'appeler le LLM, le système créera des fichiers de log dans :
```
./debug_extraction_logs/
```

Chaque fichier contient :
- **Nom** : `001_proposition_analyse.txt` (numéro_kind_tag)
- **Contenu** :
  - État complet du bloc (raw_text, validated_text, normalized_text, metadata)
  - Le prompt exact qui aurait été envoyé au LLM
  - Informations de diagnostic (kind, tags, self-contained, etc.)

## Désactivation

```powershell
$env:DEBUG_EXTRACTION="false"
```

Ou supprimez la ligne du `.env`

## Vérifier les logs

```powershell
# Lister les fichiers créés
ls ./debug_extraction_logs/

# Chercher le bloc 10 (proposition sur intervalles emboîtés)
Get-ChildItem ./debug_extraction_logs/ | Where-Object { $_.Name -like "*proposition*" }

# Voir le contenu d'un log
cat ./debug_extraction_logs/010_proposition_analyse.txt
```

## Ce que vous pouvez diagnostiquer

1. **Le bloc est-il extrait ?** → Si aucun fichier n'est créé pour "Il est équivalent", le bloc n'arrive pas à l'extracteur
2. **Le prompt est-il correct ?** → Vérifiez que le texte complet est présent
3. **Les métadonnées sont-elles vides ?** → Vérifiez le champ "Metadata" dans le log
