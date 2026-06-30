from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password123")

driver = GraphDatabase.driver(URI, auth=AUTH)

try:
    driver.verify_connectivity()
    print("Neo4j 연결 성공!")

    with driver.session() as session:
        result = session.run("RETURN 'Hello from Python!' AS message")
        record = result.single()
        print(f"응답: {record['message']}")
except Exception as e:
    print(f"연결 실패: {e}")
finally:
    driver.close()
