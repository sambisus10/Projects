from typing import Dict, List, Optional, Set

L_LIKE = "└"
HOR_LINE = "─ "
T_LIKE = "├"
VER_LINE = "│  "
SPACE = "   "


class Person:
    def __init__(self, pid: int, name: str,
                 birth_year: int, parent: Optional['Person']) -> None:
        self.pid = pid
        self.name = name
        self.birth_year = birth_year
        self.parent: Optional[Person] = parent
        self.children: List[Person] = []

    def is_valid(self) -> bool:
        if len(self.name) == 0:
            return False

        if not self.children:
            return True

        child_names = [child.name for child in self.children]
        for name in child_names:
            if child_names.count(name) != 1:
                return False

        for child in self.children:
            if not validate_children(child):
                return False

        return True

    def draw(self, names_only: bool) -> None:
        print(self.name) if names_only else \
            print(f'{self.name} ({self.birth_year}) [{self.pid}]')

        for index, child in enumerate(self.children):
            last = True if index == len(self.children) - 1 else False
            draw(child, names_only, last, "", [])

    def parents_younger_than(self, age_limit: int) -> Set[int]:
        return find_parents(self, age_limit, True, set())

    def parents_older_than(self, age_limit: int) -> Set[int]:
        return find_parents(self, age_limit, False, set())

    def childless(self) -> Set[int]:
        return find_childless(self, set())

    def ancestors(self) -> List['Person']:
        return [] if not self.parent else find_ancestors(self.parent)

    def order_of_succession(self, alive: Set[int]) -> Dict[int, int]:
        result = {}
        order_all = find_order(self, [])
        order = 1

        for pid in order_all[1:]:
            if pid in alive:
                result[pid] = order
                order += 1

        return result

    def remove_extinct_branches(self, alive: Set[int]) -> None:
        for child in self.children[:]:
            if remove_branch(child, alive):
                self.children.remove(child)


def validate_children(person: 'Person') -> bool:
    if not person.children:
        return validate_person(person)

    if not validate_person(person):
        return False

    for child in person.children:
        if not validate_children(child):
            return False

    return True


def validate_person(person: 'Person') -> bool:
    if len(person.name) == 0:
        return False

    if person.parent and person.parent.birth_year >= person.birth_year:
        return False

    child_names = [child.name for child in person.children]
    for name in child_names:
        if child_names.count(name) != 1:
            return False

    return True


def draw(person: 'Person', names_only: bool, last: bool, prev: str,
         to_print: List[str]) -> None:

    if prev == L_LIKE + HOR_LINE:
        to_print = to_print[:-1] + [SPACE]
    elif prev == T_LIKE + HOR_LINE:
        to_print = to_print[:-1] + [VER_LINE]

    to_print.append((L_LIKE if last else T_LIKE) + HOR_LINE)

    for item in to_print:
        print(item, end="")

    print(person.name) if names_only else \
        print(f'{person.name} ({person.birth_year}) [{person.pid}]')

    for index, child in enumerate(person.children):
        last = True if index == len(person.children) - 1 else False
        draw(child, names_only, last, to_print[-1], to_print)


def find_parents(person: 'Person', age: int,
                 smaller: bool, result: Set[int]) -> Set[int]:
    for child in person.children:
        if smaller and child.birth_year - person.birth_year < age:
            result.add(person.pid)
        elif not smaller and child.birth_year - person.birth_year > age:
            result.add(person.pid)

        find_parents(child, age, smaller, result)

    return result


def find_childless(person: 'Person', result: Set[int]) -> Set[int]:
    for child in person.children:
        find_childless(child, result)

    if not person.children:
        result.add(person.pid)

    return result


def find_ancestors(person: Optional['Person']) -> List['Person']:
    if not person:
        return []

    return find_ancestors(person.parent) + [person]


def sort_children(children: List['Person']) -> List[int]:
    births = [(child.birth_year, child.pid) for child in children]
    births.sort(key=lambda x: x[0])

    return [child[1] for child in births]


def find_order(person: 'Person', result: List[int]) -> List[int]:
    result.append(person.pid)
    sorted_children = sort_children(person.children)

    while sorted_children:
        for child in person.children:
            if child.pid == sorted_children[0]:
                sorted_children.pop(0)
                find_order(child, result)
                break

    return result


def remove_branch(person: Person, alive: Set[int]) -> bool:
    remove = True

    if person.pid in alive:
        remove = False

    for child in person.children[:]:
        if remove_branch(child, alive):
            person.children.remove(child)
        else:
            remove = False

    return remove


def find_root(names: Dict[int, str],
              children: Dict[int, List[int]]) -> Optional[int]:
    all_pids: Set[int] = set(names.keys())
    kids = []

    for pid, kids_pids in children.items():
        for kid in kids_pids:
            if kid not in all_pids:
                return None

            kids.append(kid)

    for pid in all_pids:
        if kids.count(pid) > 1:
            return None

    root = all_pids.difference(set(kids))

    return None if len(root) != 1 else root.pop()


def build_family_tree_rec(person: Person, names: Dict[int, str],
                          children: Dict[int, List[int]],
                          birth_years: Dict[int, int]) -> Person:
    for kid in children.get(person.pid, []):
        person.children.append(build_family_tree_rec(
            Person(kid, names[kid], birth_years[kid], person),
            names, children, birth_years))

    return person


def build_family_tree(names: Dict[int, str],
                      children: Dict[int, List[int]],
                      birth_years: Dict[int, int]) -> Optional[Person]:
    if len(names.keys()) == 0 or names.keys() != birth_years.keys():
        return None

    childless = set(names.keys()) - set(children.keys())
    if set(names.keys()) != set(children.keys()) | childless:
        return None

    root = find_root(names, children)
    if root is None:
        return None

    first = build_family_tree_rec(
        Person(root, names[root], birth_years[root], None),
        names, children, birth_years)

    return first


def find_root_in_tree(person: 'Person') -> 'Person':
    return person if not person.parent else find_root_in_tree(person.parent)


def valid_family_tree(person: Person) -> bool:
    return find_root_in_tree(person).is_valid()


def example_family_tree():
    return build_family_tree(
        {
            1: "Queen Elizabeth II",
            2: "Prince Charles",
            3: "Princess Anne",
            4: "Prince Andrew",
            5: "Prince Edward",
            6: "Prince William",
            7: "Prince Harry",
            8: "Prince George",
            9: "Princess Charlotte",
            10: "Prince Louis",
            11: "Lady Louise",
            12: "James Viscount Severn",
            13: "Archie Harrison",
            14: "Lilibet Diana"
        },
        {
            1: [2, 3, 4, 5],
            2: [6, 7],
            5: [11, 12],
            6: [8, 9, 10],
            7: [13, 14]
        },
        {
            1: 1926,
            2: 1948,
            3: 1950,
            4: 1960,
            5: 1964,
            6: 1982,
            7: 1984,
            8: 2013,
            9: 2015,
            10: 2018,
            11: 2003,
            12: 2007,
            13: 2019,
            14: 2021
        }
    )


if __name__ == '__main__':
    queen = example_family_tree()

    print("BRITISH ROYAL FAMILY TREE:")
    queen.draw(False)

    succession = \
        queen.order_of_succession(
            {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
    print()
    print("PIDs in order of succession -> " + str(list(succession.keys())))
