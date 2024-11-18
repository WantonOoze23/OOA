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

    def resolve_conflicts(node1: Data, node2: Data):
        if node1.last_updated > node2.last_updated:
            return node1
        else:
            return node2

    def replicate(self, source_node: Data, target_node: Data):
        if source_node.data is None:
            print(f"Replication impossible: Source Node {source_node.id} has no data.")
            return

        if target_node.last_updated < source_node.last_updated:
            target_node.data = copy.deepcopy(source_node.data)
            target_node.last_updated = source_node.last_updated
            print(f"Data replicated from Node {source_node.id} to Node {target_node.id}")
        else:
            print(f"No replication needed. Node {target_node.id} has newer or equal data.")

    def delete_data(self, node: Data):
        if node in self.node:
            node.data = None
            node.last_updated = time.time()
            print(f"Data deleted from Node {node.id}")
        else:
            print(f"Node {node.id} has no data to delete.")

    def __str__(self):
        return '\n'.join([str(node) for node in self.node])

def main():
    data1 = Data(1)
    time.sleep(0.1)
    data2 = Data(2)
    time.sleep(0.1)
    data3 = Data(3)
    time.sleep(0.1)

    data4 = Data(4)
    time.sleep(0.1)

    manager = DataReplicationManager()


    manager.register(data1)
    manager.register(data2)
    manager.register(data3)
    manager.register(data4)


    data1.add_data('Daniil')
    data2.add_data('Kyiv')

    print("\nДані після додавання:")
    print(manager.node[0])
    print(manager.node[1])
    print(manager.node[2])

    # Реплікація даних із Node 1 до Node 3
    print("\nРеплікація даних з Node 1 до Node 3:")
    manager.replicate(manager.node[0], manager.node[2])

    print("\nСтан всіх вузлів після реплікації:")
    print(manager)

    # Реплікація даних із Node 2 до Node 1
    print("\nРеплікація даних з Node 2 до Node 1:")
    manager.replicate(manager.node[1], manager.node[0])

    print("\nСтан всіх вузлів після другої реплікації:")
    print(manager)

    manager.delete_data(manager.node[0])

    print("\nСтан всіх вузлів після видалення:")
    print(manager)

    manager.replicate(manager.node[0], manager.node[3])

if __name__ == '__main__':
    main()