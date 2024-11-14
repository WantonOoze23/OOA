import copy
import time

class Data:
    def __init__(self, node_id):
        self.id = node_id
        self.data = {}
        self.last_updated = time.time()

    def add_data(self, inject_data):
        self.data = inject_data
        self.last_updated = time.time()

    def __str__(self):
        return f'{self.id}: {self.data}'

class DataReplicationManager:
    def __init__(self):
        self.node = []

    def add_node(self, node: Data):
        self.node.append(node)

    def register(self, node: Data):
        self.node.append(node)

    def resolve_conflicts(self, node1: Data, node2: Data):
        if node1.last_updated > node2.last_updated:
            return node1
        else:
            return node2

    def replicate(self, source_node: Data, target_node: Data):
        if target_node.last_updated < source_node.last_updated:
            target_node.data = copy.deepcopy(source_node.data)
            target_node.last_updated = source_node.last_updated
            print(f"Data replicated from Node {source_node.id} to Node {target_node.id}")
        else:
            print(f"No replication needed. Node {target_node.id} has newer or equal data.")

    def __str__(self):
        return '\n'.join([str(node) for node in self.node])

def main():
    data1 = Data(1)
    time.sleep(0.1)
    data2 = Data(2)
    time.sleep(0.1)
    data3 = Data(3)
    time.sleep(0.1)


    manager = DataReplicationManager()


    manager.register(data1)
    manager.register(data2)
    manager.register(data3)


    data1.add_data('Daniil')
    data2.add_data('Kyiv')

    print("\nДані після додавання:")
    print(data1)
    print(data2)
    print(data3)

    # Реплікація даних із Node 1 до Node 3
    print("\nРеплікація даних з Node 1 до Node 3:")
    manager.replicate(data1, data3)

    print("\nСтан всіх вузлів після реплікації:")
    print(manager)

    # Реплікація даних із Node 2 до Node 1
    print("\nРеплікація даних з Node 2 до Node 1:")
    manager.replicate(data2, data1)

    print("\nСтан всіх вузлів після другої реплікації:")
    print(manager)


if __name__ == '__main__':
    main()