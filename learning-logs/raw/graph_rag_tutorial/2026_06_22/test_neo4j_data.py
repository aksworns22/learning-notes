from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password123",)

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    session.run("""
        CREATE (p: Person {name: '김철수', age: 30})
        CREATE (c: Company {name: 'AI 스타트업'})
        CREATE (p)-[:WORKS_AT]->(c)
    """)
    print("데이터 생성 완료!")

    result = session.run("""
        MATCH (p:Person)-[:WORKS_AT]->(c:Company)
        RETURN p.name as person, c.name as company
    """)

    for record in result:
        print(f"{record['person']}님은 {record['company']}에서 일합니다.")

driver.close()