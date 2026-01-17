import random
import importlib
import pkgutil

from topics_registry import TOPICS
import topic_directory

def random_topic_module(package):
    modules = [
        name for _, name, is_pkg
        in pkgutil.iter_modules(package.__path__)
        if not is_pkg
    ]
    return random.choice(modules)

def load_tree(package_name, module_name):
    module = importlib.import_module(f"{package_name}.{module_name}")
    return module.TREE

def random_tree_path(tree):
    path = []
    node = tree

    while isinstance(node, dict) and node:
        key = random.choice(list(node.keys()))
        path.append(key)
        node = node[key]

    return path

def pick_random_topic():
    module_name = random_topic_module(topic_directory)
    tree = load_tree("topic_directory", module_name)

    path = random_tree_path(tree)
    leaf_id = path[-1]

    topic = TOPICS.get(leaf_id)
    if topic is None:
        raise KeyError(f"Leaf '{leaf_id}' not found in topic registry")

    return {
        "source": module_name,
        "path": path,
        "topic": topic
    }

result = pick_random_topic()

print("This is what you're about to learn:")
print()
print(f"Topic: {result['topic']['name']}")
print(f"Path: {result['source'].capitalize()} -> {' -> '.join([x.capitalize() for x in result['path']])}")
print(f"Description: {result['topic']['description']}")