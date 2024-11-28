import uuid


class DeviceDetails:
    def __init__(self, driver):
        self.driver = driver

    def create_data(self, data):
        with self.driver.session() as session:
            query = """
            MERGE (source:Device {
                device_id: $source_id,
                name: $source_name,
                brand: $source_brand,
                model: $source_model,
                os: $source_os
            })
            MERGE (target:Device {
                device_id: $target_id,
                name: $target_name,
                brand: $target_brand,
                model: $target_model,
                os: $target_os
            })
            MERGE (source)-[interaction:CONNECTED {
                transaction_id: $transaction_id,
                method: $method,
                bluetooth_version: $bluetooth_version,
                signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters,
                duration_seconds: $duration_seconds,
                timestamp: datetime($timestamp)
            }]->(target)
            RETURN interaction.transaction_id as transaction_id
            """

            transaction_id = str(uuid.uuid4())

            result = session.run(query, {
                'source_id': data["devices"][0]['id'],
                'source_name': data["devices"][0]['name'],
                'source_brand': data["devices"][0]['brand'],
                'source_model': data["devices"][0]['model'],
                'source_os': data["devices"][0]['os'],

                'target_id': data["devices"][1]['id'],
                'target_name': data["devices"][1]['name'],
                'target_brand': data["devices"][1]['brand'],
                'target_model': data["devices"][1]['model'],
                'target_os': data["devices"][1]['os'],

                'transaction_id': transaction_id,
                'method': data['interaction']['method'],
                'bluetooth_version': data['interaction']['bluetooth_version'],
                'signal_strength_dbm': data['interaction']['signal_strength_dbm'],
                'distance_meters': data['interaction']['distance_meters'],
                'duration_seconds': data['interaction']['duration_seconds'],
                'timestamp': data['interaction']['timestamp']
            })

        return result.single()
