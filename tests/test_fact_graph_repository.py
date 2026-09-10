from backend.app.db.session import SessionLocal
from backend.app.models import Source
from backend.app.services.fact_graph import FactGraphRepository


def main():
    if SessionLocal is None:
        raise RuntimeError("Database is not configured.")

    repository = FactGraphRepository()

    with SessionLocal() as db:
        source = Source(
            source_type="text",
            title="Fact Graph Version Test",
            content="310 customers were affected.",
            source_metadata={},
        )

        db.add(source)
        db.flush()

        graph_v1 = repository.create(
            db,
            source_id=source.id,
            graph_data={
                "facts": [
                    {
                        "id": "fact-001",
                        "category": "metric",
                        "subject": "Affected customers",
                        "predicate": "count",
                        "object": "310",
                        "source_reference": "text:section-1",
                        "confidence": 1.0,
                    }
                ]
            },
            extraction_metadata={
                "extraction_method": "test",
            },
        )

        graph_v2 = repository.create(
            db,
            source_id=source.id,
            graph_data={
                "facts": [
                    {
                        "id": "fact-001",
                        "category": "metric",
                        "subject": "Affected customers",
                        "predicate": "count",
                        "object": "340",
                        "source_reference": "text:section-1",
                        "confidence": 1.0,
                    }
                ]
            },
            extraction_metadata={
                "extraction_method": "test",
            },
        )
        latest = repository.get_latest(
            db,
            source.id,
        )

        assert latest is not None
        assert latest.version == 2
        assert latest.graph_data["facts"][0]["object"] == "340"

        print(f"Latest Graph Version: {latest.version}")

        version_one = repository.get_version(
            db,
            source.id,
            1,
        )

        assert version_one is not None
        assert version_one.version == 1
        assert version_one.graph_data["facts"][0]["object"] == "310"

        print(f"Retrieved Graph V1: {version_one.version}")



        db.commit()

        print(f"Source ID: {source.id}")
        print(f"Graph V1: {graph_v1.version}")
        print(f"Graph V2: {graph_v2.version}")

        assert graph_v1.version == 1
        assert graph_v2.version == 2

        print("Fact Graph versioning: PASS")


if __name__ == "__main__":
    main()