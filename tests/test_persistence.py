import pytest
from core.semantic_schemas import (
    ExtractedDefinition,
    LinkedBlock,
    SemanticBlockIndex,
    ValidatedBlock,
)
from db.models import Base, BlockKind, SemanticBlock, Tag
from db.persister import SemanticPersister
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_persist_simple_block(session):
    persister = SemanticPersister(session)
    
    # Create dummy data
    block_id = "block_1"
    validated_block = ValidatedBlock(
        id=block_id,
        kind=BlockKind.definition,
        raw_text="Definition of Group...",
        validated_text="Definition of Group...",
        page=1,
        start_line=1,
        end_line=5,
        is_self_contained=True
    )
    
    linked_block = LinkedBlock(
        block=validated_block,
        linked_to=[],
        context_blocks=[]
    )
    
    extracted_data = ExtractedDefinition(
        name="Group",
        term="Group",
        statement="A group is...",
        domain_tags=["algebra"],
        characteristics=["algebraic structure"]
    )
    
    index = SemanticBlockIndex(
        normalized_name="Group",
        domain_tags=["algebra"],
        characteristics=["algebraic structure"],
        embedding_text="Group | A group is...",
        key_phrases=["Group"]
    )
    
    analysis_results = {
        "blocks": [validated_block.model_dump()],
        "linked_blocks": [{
            "block": validated_block.model_dump(),
            "linked_to": [],
            "context_blocks": []
        }],
        "extracted": [{
            "block_id": block_id,
            "kind": "definition",
            "data": extracted_data.model_dump()
        }],
        "indexes": [{
            "block_id": block_id,
            "kind": "definition",
            "index": index,
            "embedding": [0.1, 0.2, 0.3]
        }],
        "language": "en"
    }
    
    # Run persistence
    persister.persist_analysis_results(analysis_results, doc_title="Test Doc", doc_path="/tmp/test.pdf")
    
    # Verify
    saved_block = session.query(SemanticBlock).first()
    assert saved_block is not None
    assert saved_block.kind == BlockKind.definition
    assert saved_block.name == "Group"
    assert saved_block.tags[0].name == "algebra"
    assert saved_block.importance_score is None # Or whatever default
