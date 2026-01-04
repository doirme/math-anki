"""Test BlockKind enum comparison"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from core.enums import BlockKind

print("=" * 80)
print("TEST: BlockKind enum comparison")
print("=" * 80)

# Test 1: Enum comparison
kind = BlockKind.proposition
print(f"\n1. kind = BlockKind.proposition")
print(f"   kind == BlockKind.proposition: {kind == BlockKind.proposition}")
print(
    f"   kind in (BlockKind.theorem, BlockKind.proposition): {kind in (BlockKind.theorem, BlockKind.proposition)}"
)
print(f"   type(kind): {type(kind)}")
print(f"   value: {kind}")
print(f"   str(kind): {str(kind)}")

# Test 2: String comparison
kind_str = "proposition"
print(f"\n2. kind_str = 'proposition'")
print(f"   kind_str == BlockKind.proposition: {kind_str == BlockKind.proposition}")
print(
    f"   kind_str in (BlockKind.theorem, BlockKind.proposition): {kind_str in (BlockKind.theorem, BlockKind.proposition)}"
)

# Test 3: What does Pydantic do?
from core.semantic_schemas import ValidatedBlock

block = ValidatedBlock(
    id="test", kind=BlockKind.proposition, raw_text="test", validated_text="test"
)

print(f"\n3. ValidatedBlock with kind=BlockKind.proposition")
print(f"   block.kind: {block.kind}")
print(f"   type(block.kind): {type(block.kind)}")
print(f"   block.kind == BlockKind.proposition: {block.kind == BlockKind.proposition}")
print(
    f"   block.kind in (BlockKind.theorem, BlockKind.proposition): {block.kind in (BlockKind.theorem, BlockKind.proposition)}"
)

# Test 4: After serialization/deserialization
import json

block_dict = block.model_dump()
print(f"\n4. After model_dump()")
print(f"   kind in dict: {block_dict['kind']}")
print(f"   type: {type(block_dict['kind'])}")

# Recreate from dict
block2 = ValidatedBlock(**block_dict)
print(f"\n5. After recreating from dict")
print(f"   block2.kind: {block2.kind}")
print(f"   type(block2.kind): {type(block2.kind)}")
print(
    f"   block2.kind == BlockKind.proposition: {block2.kind == BlockKind.proposition}"
)

print("\n" + "=" * 80)
