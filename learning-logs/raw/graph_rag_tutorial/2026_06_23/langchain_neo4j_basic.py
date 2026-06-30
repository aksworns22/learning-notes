from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv

load_dotenv()

graph = Neo4jGraph(
    url="neo4j://localhost:7687",
    username="neo4j",
    password="password123",
)

people = [
    {"name": "세종대왕", "born": 1397, "died": 1450, "role": "왕"},
    {"name": "장영실", "born": 1390, "role": "과학자"},
    {"name": "신숙주", "born": 1417, "died": 1475, "role": "학자"},
    {"name": "정조", "born": 1752, "died": 1800, "role": "왕"},
    {"name": "정약용", "born": 1762, "died": 1836, "role": "학자"},
]

achievements = [
    {"name": "훈민정음", "year": 1443, "type": "문자"},
    {"name": "측우기", "year": 1441, "type": "발명"},
    {"name": "수원화성", "year": 1796, "type": "건축"},
]

organizations = [
    {"name": "집현전", "type": "학술기관"},
    {"name": "규장각", "type": "학술기관"},
]

for person in people:
    graph.query("""
    MERGE (p:Person:HistoricalFigure {name: $name})
    SET p.born = $born,
        p.died = $died,
        p.role = $role
    """, params={
        "name": person["name"],
        "born": person.get("born"),
        "died": person.get("died"),
        "role": person.get("role")
    })

print(f"{len(people)}명의 인물 생성 완료")

for ach in achievements:
    graph.query("""
        MERGE (a:Achievement {name: $name})
        SET a.year = $year, a.type = $type
    """, params=ach)

print(f"{len(achievements)}개의 업적 생성 완료")

for org in organizations:
    graph.query("""
        MERGE (o:Organization {name: $name})
        SET o.type = $type
    """, params=org)

print(f"{len(organizations)}개의 기관 생성 완료")

relationships = [
    ("세종대왕", "CREATED", "훈민정음"),
    ("세종대왕", "ESTABLISHED", "집현전"),
    ("세종대왕", "COLLABORATED_WITH", "장영실"),
    ("장영실", "INVENTED", "측우기"),
    ("신숙주", "WORKED_AT", "집현전"),
    ("정조", "ESTABLISHED", "규장각"),
    ("정조", "ORDERED", "수원화성"),
    ("정조", "APPOINTED", "정약용"),
    ("정약용", "WORKED_AT", "규장각"),
]

for source, rel_type, target in relationships:
    graph.query(f"""
        MATCH (a {{name: $source}})
        MATCH (b {{name: $target}})
        MERGE (a)-[:{rel_type}]->(b)
    """, params={"source": source, "target": target})

print(f"{len(relationships)}개의 관계 생성 완료")
print("\n한국 역사 지식 그래프 구축 완료!")

# 세종대왕 관련 모든 정보
result1 = graph.query("""
    MATCH (sejong:Person {name: "세종대왕"})-[r]->(related)
    RETURN type(r) AS 관계, labels(related) AS 유형, related.name AS 대상
""")

print("세종대왕의 업적과 관계:")
for row in result1:
    print(f"  [{row['관계']}] → {row['대상']} ({row['유형'][0]})")

# 2단계 관계 탐색
result2 = graph.query("""
    MATCH (sejong:Person {name: "세종대왕"})-[:ESTABLISHED]->(org:Organization)<-[:WORKED_AT]-(scholar:Person)
    RETURN org.name AS 기관, scholar.name AS 학자
""")

print("\n세종대왕이 설립한 기관의 학자:")
for row in result2:
    print(f"  {row['기관']} → {row['학자']}")
