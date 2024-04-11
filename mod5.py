from collections import defaultdict
def find_functional_dependencies(relation_instance):
    fds = defaultdict(set)
    for tuple1 in relation_instance:
        for tuple2 in relation_instance:
            differing_attribute = None
            for attr in tuple1:
                if tuple1[attr] != tuple2[attr]:
                    if differing_attribute is not None:
                        differing_attribute = None
                        break
                    differing_attribute = attr
            if differing_attribute is not None:
                fds[differing_attribute].add((tuple1[differing_attribute], tuple2[differing_attribute]))
    functional_dependencies = []
    for lhs, rhs_set in fds.items():
        for rhs_tuple in rhs_set:
            functional_dependencies.append((lhs, rhs_tuple[0]))
    return functional_dependencies
relation_instance = [
    {'A': '1', 'B': '2', 'C': '3'},
    {'A': '1', 'B': '2', 'C': '4'},
    {'A': '1', 'B': '5', 'C': '6'},
]
functional_dependencies = find_functional_dependencies(relation_instance)
print("Functional Dependencies:")
for fd in functional_dependencies:
    print(fd[0], "->", fd[1])