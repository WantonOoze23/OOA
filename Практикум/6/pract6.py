import time

class ReplicationNode:
    def __init__(self, node_id):
        self.id = node_id
        self.data = {}
        self.last_updated = time.time()

    def update_data(self, key, value):
        self.data[key] = value
        self.last_updated = time.time()

    def get_data(self, key):
        return self.data.get(key)

    def get_last_updated(self):
        return self.last_updated

class ReplicationManager:
    def __init__(self, nodes):
        self.nodes = nodes

    def handle_conflict(self, conflicting_data):
        # Логіка вирішення конфлікту
        # Наприклад, можна використовувати таймстампи для вибору найновішої версії
        resolved_data = {}
        for key, values in conflicting_data.items():
            latest_value = max(values, key=lambda x: x[1])
            resolved_data[key] = latest_value[0]
        return resolved_data

def main():
    # Створення вузлів
    node1 = ReplicationNode(1)
    node2 = ReplicationNode(2)

    # Створення менеджера
    manager = ReplicationManager([node1, node2])

    # Оновлення даних на різних вузлах
    node1.update_data("key1", "value1")
    node2.update_data("key1", "value2")

    # Виявлення конфлікту та його вирішення
    conflicting_data = {"key1": [(node1.get_data("key1"), node1.get_last_updated()), (node2.get_data("key1"), node2.get_last_updated())]}
    resolved_data = manager.handle_conflict(conflicting_data)
    print(resolved_data)
    node1.update_data("key1", "value3")
    conflicting_data2 = {"key1": [(node1.get_data("key1"), node1.get_last_updated()),
                                 (node2.get_data("key1"), node2.get_last_updated())]}
    resolved_data2 = manager.handle_conflict(conflicting_data2)
    print(resolved_data2)


if __name__ == '__main__':
    main()