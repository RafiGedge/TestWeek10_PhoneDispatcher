from neo4j import GraphDatabase

from database.setings.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def init_neo4j():
    neo4j_driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    return neo4j_driver
