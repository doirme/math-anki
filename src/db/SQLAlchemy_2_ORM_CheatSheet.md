
# 🧩 SQLAlchemy 2.0 ORM Cheat Sheet  
*(version moderne, typée, compatible avec Pydantic v2)*

---

## 🔹 1. Base déclarative typée

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Classe de base commune à tous les modèles."""
    pass
```

✅ Plus besoin de `declarative_base()` (ancienne API).

---

## 🔹 2. Colonnes avec `Mapped[]` et `mapped_column()`

### Exemple complet

```python
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    source_path: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

---

### 🧠 `Mapped[...]`  
Type d’attribut ORM.  
→ Dit à SQLAlchemy : “ce champ fait partie du mapping vers la base”.

| Exemple | Signification |
|----------|----------------|
| `Mapped[int]` | Colonne d’entiers |
| `Mapped[str]` | Colonne de texte |
| `Mapped[list["Other"]]` | Relation 1→N |
| `Mapped["Other"]` | Relation N→1 |

---

### ⚙️ `mapped_column()` : options importantes

| Option | Exemple | Description |
|--------|----------|-------------|
| `primary_key=True` | `mapped_column(primary_key=True)` | Clé primaire |
| `ForeignKey("table.col", ondelete="CASCADE")` | | Clé étrangère |
| `index=True` | | Crée un index SQL |
| `unique=True` | | Crée une contrainte d’unicité |
| `default=value` | | Valeur par défaut côté Python |
| `server_default=text("...")` | | Valeur par défaut côté SQL |
| `nullable=False` | | Empêche les NULL |
| `String`, `Integer`, `Text`, `Float`, `DateTime` | `mapped_column(String)` | Type SQL explicite |
| `onupdate=func.now()` | | Mise à jour automatique d’un timestamp |

---

## 🔹 3. Relations (`relationship()`)

```python
from sqlalchemy.orm import relationship
from typing import List

class Document(Base):
    __tablename__ = "document"
    id: Mapped[int] = mapped_column(primary_key=True)
    text_blocks: Mapped[List["TextBlock"]] = relationship(back_populates="document")

class TextBlock(Base):
    __tablename__ = "text_block"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id", ondelete="CASCADE"))
    document: Mapped["Document"] = relationship(back_populates="text_blocks")
```

| Option | Rôle |
|--------|------|
| `back_populates="..."` | crée la liaison bidirectionnelle |
| `cascade="all, delete-orphan"` | supprime automatiquement les enfants quand le parent est supprimé |
| `foreign_keys=[...]` | explicite quelle clé est utilisée (utile pour self-relations) |
| `uselist=False` | relation 1→1 au lieu de 1→N |
| `post_update=True` | permet de résoudre les cycles de FK (auto-références) |

---

### 🔁 Exemple de relation auto-référente (self-relation)

```python
class SemanticBlock(Base):
    __tablename__ = "semantic_block"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    statement_id: Mapped[int | None] = mapped_column(ForeignKey("semantic_block.id", ondelete="SET NULL"))

    # self-relation (théorème → énoncé)
    statement: Mapped["SemanticBlock | None"] = relationship(
        "SemanticBlock",
        foreign_keys=[statement_id],
        remote_side="SemanticBlock.id",
        uselist=False,
        post_update=True,
    )
```

---

## 🔹 4. Contraintes et index (`__table_args__`)

```python
from sqlalchemy import UniqueConstraint, Index

__table_args__ = (
    UniqueConstraint("name", name="uq_math_object_name"),
    Index("idx_document_title", "title"),
)
```

---

## 🔹 5. Sessions et engine

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///math_semantics.db", echo=True)
Session = sessionmaker(bind=engine)

with Session() as db:
    db.add(Document(title="Cours d'analyse"))
    db.commit()
```

---

## 🔹 6. Pydantic v2 et ORM

Pydantic v2 sait lire directement les objets SQLAlchemy grâce à :

```python
from pydantic import BaseModel, ConfigDict

class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
```

Cela permet :

```python
doc = db.query(Document).first()
DocumentRead.model_validate(doc)
```

---

## 🔹 7. Auto-création de la base

```python
from .models import Base
Base.metadata.create_all(engine)
```

---

## 🧭 8. Bonnes pratiques

- Toujours **typer** : `Mapped[int]`, `Mapped[str]`, etc.
- Déclarer les **liens ORM** bidirectionnels avec `back_populates`.
- Regrouper les indices et contraintes dans `__table_args__`.
- Préférer `default=` (Python) à `server_default` (SQL) sauf si on veut un timestamp SQL côté serveur.
- Utiliser `sessionmaker(..., expire_on_commit=False)` pour éviter la déconnexion automatique des objets après `commit()`.
