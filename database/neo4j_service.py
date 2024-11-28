class Neo4jService:
    def __init__(self, driver):
        self.driver = driver

    def insert_devices(self, devices: list):
        query = """
        MERGE (d:Device {id: $id})
            SET d.name = $name,
            d.brand = $brand,
            d.model = $model,
            d.os = $os
        """
        result = []
        with self.driver.session() as session:
            for d in devices:
                session.run(query, d)
                result.append(d['id'])

        return result

    def create_interaction(self, interaction: dict):
        query = """
        MATCH (from:Device {id: $from_device}), (to:Device {id: $to_device})
        CREATE (from)-[r:CONNECTED {
            method: $method,
            bluetooth_version: $bluetooth_version,
            signal_strength_dbm: $signal_strength_dbm,
            distance_meters: $distance_meters,
            duration_seconds: $duration_seconds,
            timestamp: $timestamp}]->(to)
        """
        with self.driver.session() as session:
            session.run(query, interaction)

        return 'created'

    def get_by_bluetooth(self):
        query = """
        MATCH (start:Device)
        MATCH (end:Device)
        WHERE start <> end
        MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
        WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
        WITH path, length(path) AS pathLength
        ORDER BY pathLength DESC
        LIMIT 1
        RETURN path
        """
        with self.driver.session() as session:
            result = session.run(query).data()

        return result

    def get_by_stronger_than(self, signal_strength):
        query = """
        MATCH (d1:Device)-[r:CONNECTED]->(d2:Device)
        WHERE r.signal_strength_dbm > $signal_strength
        RETURN d1, r, d2
        """
        with self.driver.session() as session:
            result = session.run(query, signal=signal_strength).data()

        return result

    def get_devices_connected(self, device_id):
        query = """
        MATCH (:Device {id: $device_id})-[:CONNECTED]-(:Device) 
        RETURN count(*) as count
        """
        with self.driver.session() as session:
            result = session.run(query, device=device_id).single()

        return result['count']

    def check_direct_connection(self, from_device_id, to_device_id):
        query = """
        MATCH (from:Device {id: $from_device_id})-[:CONNECTED]-(to:Device {id: $to_device_id})
        RETURN count(*) as count
        """
        with self.driver.session() as session:
            result = session.run(query, from_device=from_device_id, to=to_device_id).single()

        return result['count'] > 0
