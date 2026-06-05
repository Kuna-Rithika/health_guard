import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "healthguard_symptoms"

# =====================================================
# SETUP CLIENT
# =====================================================

def get_qdrant_client():
    try:
        from qdrant_client import QdrantClient
        return QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
    except Exception as e:
        print(f"Qdrant connection error: {e}")
        return None

# =====================================================
# SETUP COLLECTION
# =====================================================

def setup_collection(client):
    try:
        from qdrant_client.models import Distance, VectorParams
        existing = [c.name for c in client.get_collections().collections]
        if COLLECTION_NAME not in existing:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection created: {COLLECTION_NAME}")
    except Exception as e:
        print(f"Qdrant setup error: {e}")

# =====================================================
# STORE HEALTH RECORD
# =====================================================

def store_health_record(user_id: int, symptoms: str, report: str):
    try:
        from qdrant_client.models import PointStruct
        import uuid
        import hashlib

        client = get_qdrant_client()
        if not client:
            return

        setup_collection(client)

        # Simple vector from text hash (no extra embedding model needed)
        text = f"{user_id} {symptoms}"
        hash_bytes = hashlib.md5(text.encode()).digest()
        vector = [float(b) / 255.0 for b in hash_bytes]
        vector = vector * 24  # 384 dimensions

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "user_id": user_id,
                "symptoms": symptoms,
                "report": report
            }
        )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        print(f"Qdrant: stored session for user {user_id}")

    except Exception as e:
        print(f"Qdrant store error: {e}")

# =====================================================
# SEARCH SIMILAR SYMPTOMS
# =====================================================

def search_health_history(user_id: int, query: str):
    try:
        import hashlib

        client = get_qdrant_client()
        if not client:
            return []

        text = f"{user_id} {query}"
        hash_bytes = hashlib.md5(text.encode()).digest()
        vector = [float(b) / 255.0 for b in hash_bytes]
        vector = vector * 24

        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=3
        )

        matches = []
        for r in results:
            if r.payload.get("user_id") == user_id:
                matches.append({
                    "symptoms": r.payload.get("symptoms"),
                    "report": r.payload.get("report"),
                    "score": r.score
                })

        return matches

    except Exception as e:
        print(f"Qdrant search error: {e}")
        return []