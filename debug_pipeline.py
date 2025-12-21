import json
import os
import sys
from pathlib import Path

# Add src to sys.path for direct execution
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from core.block_creator import BlockCreator
from core.block_linker import BlockLinker
from core.semantic_extractor import SemanticExtractor
from core.semantic_schemas import LinkedBlock


def debug_pipeline(file_path: str):
    """Run the full pipeline on a file and print results for debugging."""
    print(f"\n{'='*80}")
    print(f"DEBUGGING PIPELINE FOR: {file_path}")
    print(f"{'='*80}\n")

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return

    # Load content
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Phase 1: Block Creation (Extraction + Deduplication)
    print(f"{'#'*40}")
    print("# PHASE 1: BLOCK CREATION (EXTRACT + DEDUPE)")
    print(f"{'#'*40}\n")

    creator = BlockCreator()
    blocks = creator.create_blocks(text)

    print(f"Generated {len(blocks)} blocks:")
    for i, b in enumerate(blocks):
        print(f"[{i:03}] ID={b.id[:8]} KIND={b.kind.value:<12} TAGS={b.tags}")
        if b.metadata:
            # Show interesting bits of metadata
            meta = b.metadata
            print(
                f"      META: terms={meta.get('term')} norm={meta.get('normalized_name')}"
            )
    print()

    # Phase 2: Block Linking
    print(f"{'#'*40}")
    print("# PHASE 2: BLOCK LINKING")
    print(f"{'#'*40}\n")

    linker = BlockLinker()
    linked_blocks = linker.link_blocks(blocks)

    for i, lb in enumerate(linked_blocks):
        links = [f"{rel['relation']} -> {rel['block_id'][:8]}" for rel in lb.linked_to]
        if links or lb.context_blocks:
            print(
                f"[{i:03}] ID={lb.block.id[:8]} LINKS={links} CONTEXT_IDS={[cid[:8] for cid in lb.context_blocks]}"
            )
    print()

    # Phase 3: Semantic Extraction
    print(f"{'#'*40}")
    print("# PHASE 3: SEMANTIC EXTRACTION")
    print(f"{'#'*40}\n")

    semantic_extractor = SemanticExtractor()
    extracted_data = semantic_extractor.extract(linked_blocks)

    print(f"Extracted {len(extracted_data)} semantic objects:")
    for i, item in enumerate(extracted_data):
        kind = item["kind"]
        data = item["data"]
        print(f"[{i:03}] ID={item['block_id'][:8]} KIND={kind:<12}")

        # Display specific fields based on kind
        if kind == "definition":
            print(f"      TERM: {data.term}")
            print(f"      STATEMENT: {data.statement[:100]}...")
        elif kind == "theorem":
            print(f"      NAME: {data.name} (Normalized: {data.normalized_name})")
            print(f"      CONCLUSION: {data.conclusion[:100]}...")
        elif kind == "proof":
            print(f"      STEPS: {len(data.steps)} steps")
        elif kind == "exercise":
            print(f"      QUESTIONS: {len(data.questions)} questions")
        elif kind == "formula":
            print(f"      STATEMENT: {data.statement}")
        if hasattr(data, "domain_tags"):
            print(f"      TAGS: {data.domain_tags}")

    print(f"\n{'='*80}")
    print("PIPELINE DEBUG COMPLETE")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    target_file = r"C:\Users\axelc\Documents\math-anki\ressources\test.txt"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]

    debug_pipeline(target_file)
