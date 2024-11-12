#19. Клас "Реплікація даних у розподіленій системі"
#Реалізувати реплікацію даних у розподіленій системі з підтримкою консистентності та відновлення після помилок. Створити класи для реплікаційних вузлів та менеджера для обробки конфліктів.

import threading
import time

class ReplicationNode:
    def __init__(self, node_id, data=None):
        self.node_id = node_id
        self.data = data if data else {}
        self.lock = threading.Lock()
        self.replicas = []  # Список реплік, до яких синхронізується цей вузол

    def update_data(self, key, value):
        with self.lock:
            self.data[key] = value
        # Синхронізація з усіма репліками
        for replica in self.replicas:
            replica.sync_data(self.node_id, key, value)

    def sync_data(self, node_id, key, value):
        # Отримуємо оновлення від іншого вузла
        with self.lock:
            if key not in self.data:
                self.data[key] = value  # Синхронізуємо дані
            else:
                # Обробка конфлікту
                self.resolve_conflict(key, value)

    def resolve_conflict(self, key, new_value):
        # Стратегія вирішення конфліктів (наприклад, пріоритет останнього запису)
        with self.lock:
            print(f"Conflict detected for key {key}. Resolving...")
            self.data[key] = new_value  # Можна реалізувати складніші стратегії

    def add_replica(self, replica_node):
        self.replicas.append(replica_node)


class ReplicationManager:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def start_replication(self):
        # Починаємо реплікацію даних між вузлами
        for node in self.nodes.values():
            for replica in self.nodes.values():
                if node != replica:
                    node.add_replica(replica)

    def simulate_failure(self, node_id):
        # Симуляція збою вузла (наприклад, відключення вузла)
        if node_id in self.nodes:
            failed_node = self.nodes[node_id]
            print(f"Node {failed_node.node_id} failed. Starting recovery...")
            self.recover_node(failed_node)

    def recover_node(self, failed_node):
        # Відновлення вузла після збою (синхронізація з іншими вузлами)
        time.sleep(2)  # Затримка для відновлення
        for replica in failed_node.replicas:
            failed_node.sync_data(replica.node_id, failed_node.data)
        print(f"Node {failed_node.node_id} successfully recovered.")

# Приклад використання
manager = ReplicationManager()

# Створення вузлів
node1 = ReplicationNode("node1", {"key1": "value1"})
node2 = ReplicationNode("node2", {"key2": "value2"})
node3 = ReplicationNode("node3", {"key3": "value3"})

# Додавання вузлів до менеджера
manager.add_node(node1)
manager.add_node(node2)
manager.add_node(node3)

# Початок реплікації
manager.start_replication()

# Оновлення даних на одному з вузлів
node1.update_data("key4", "value4")

# Симуляція збою вузла
manager.simulate_failure("node2")

# Оновлення даних на іншому вузлі після відновлення
node3.update_data("key5", "value5")
