from db.models import Document, SemanticBlock, Tag
from db.session import get_db_session


def check_db():
    with get_db_session() as session:
        blocks_count = session.query(SemanticBlock).count()
        docs_count = session.query(Document).count()
        tags_count = session.query(Tag).count()
        print(f"Blocks: {blocks_count}")
        print(f"Documents: {docs_count}")
        print(f"Tags: {tags_count}")

        if blocks_count > 0:
            block = session.query(SemanticBlock).first()
            print(f"Sample Block Kind: {block.kind}")
            print(f"Sample Block Sources: {len(block.sources)}")


if __name__ == "__main__":
    check_db()
