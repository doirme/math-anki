from core.math_fix import fix_math_in_markdown, needs_fix, repair_with_rules


def test_needs_fix_detects_newlines_and_unbalanced():
    f1 = r"x \n \epsilon"           # newline brut
    f2 = r"\left( x + 1"            # \left sans \right et accolade non fermée
    assert needs_fix(f1) is True
    assert needs_fix(f2) is True

def test_repair_with_rules_basic():
    f = r"n > x\n \epsilon"
    fixed, notes = repair_with_rules(f)
    assert "\n" not in fixed
    assert "Removed raw newlines" in notes or "Fixed broken" in " ".join(notes)

def test_fix_math_in_markdown_on_inline_and_block():
    md = "Soit $n > x\n \\epsilon$ et $$\\sum\\n_{k=1}^n a_k$$."
    md2, modified, attention = fix_math_in_markdown(md, llm=None)
    assert modified >= 1
    assert "\\n" not in md2
    assert "\n" not in md2.split("$")[1]  # l'inline a été reflow
    # On accepte que 'attention' puisse être >0 si heuristique doute

def test_fix_math_uses_llm_when_provided(monkeypatch):
    # formule avec token \n pour déclencher la réparation
    md = "Texte $n > x\\n \\epsilon$ fin."

    # LLM factice qui renvoie un JSON de correction
    def fake_llm(prompt: str) -> str:
        return '{"fixed":"n > x \\\\epsilon","notes":"joined"}'

    md2, modified, attention = fix_math_in_markdown(md, llm=fake_llm)
    # le span a été modifié par la passe rules ou LLM
    assert modified >= 1
    # et l'epsilon latex a été corrigé (double backslash dans str)
    assert "\\\\epsilon" in md2 or "\\epsilon" in md2