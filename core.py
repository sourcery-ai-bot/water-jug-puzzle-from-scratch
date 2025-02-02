#!/usr/bin/env python

from typing import Any, Optional


class Node:
    """Node for a singly linked list.

    Attributes:
        data: The value stored in the node.
        next: The next node in the list.
    """

    def __init__(self, data: Any) -> None:
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list implementation.

    Attributes:
        head: The first node in the list.
        size: The number of nodes.
    """

    def __init__(self, data: Optional[Any] = None) -> None:
        self.head = Node(data) if data is not None else None
        self.size = 1 if self.head is not None else 0

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return f'LinkedList(head={self.head}, size={self.size})'

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self) -> 'LinkedList':
        self.current = self.head
        return self

    def __next__(self) -> Any:
        if self.current is None:
            raise StopIteration('No more items in the list.')

        data = self.current.data
        self.current = self.current.next
        return data

    def __getitem__(self, index: int) -> Any:
        if not 0 <= index < self.size:
            raise IndexError('Index out of range.')

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def __setitem__(self, index: int, data: Any) -> None:
        if not 0 <= index < self.size:
            raise IndexError('Index out of range.')

        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data

    def __delitem__(self, index: int) -> None:
        if not 0 <= index < self.size:
            raise IndexError('Index out of range.')

        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
            current.next = current.next.next
        self.size -= 1

    def __add__(self, other: Any) -> 'LinkedList':
        """Adds two puzzles together."""
        self.append(other)
        return self

    def append(self, data: Any) -> None:
        """Appendes a node to the end of the list."""
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.size += 1

    def insert(self, index: int, data: Any) -> None:
        """Inserts a node at the specified index."""
        if not 0 <= index < self.size:
            raise IndexError('Index out of range.')

        node = Node(data)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
            node.next = current.next
            current.next = node
        self.size += 1

    def find(self, data: Any) -> int:
        """Returns the index of the first node with the specified data."""
        current = self.head
        for i in range(self.size):
            if current.data == data:
                return i
            current = current.next
        return -1

    def pop(self, index: int) -> Any:
        """Removes and returns the node at the specified index."""
        if not 0 <= index < self.size:
            raise IndexError('Index out of range.')

        current = self.head
        for _ in range(index-1):
            current = current.next
        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data

    def clear(self) -> None:
        """Removes all nodes from the list."""
        self.head = None
        self.size = 0


def _string_to_int_list(data: str, seperator: Optional[str] = '/') -> list:
    """Converts a string by the seperator into an integer list."""
    return [int(x) for x in data.split(seperator)]


def _list_to_string(data: list, joiner: Optional[str] = '/') -> str:
    """Converts a list by the joiner into a string."""
    return joiner.join([str(x) for x in data])


class WaterJugPuzzle:
    """Water jug puzzle implementation.

    Attributes:
        jug_a: The capacity and current amount of water in jug A.
        jug_b: The capacity and current amount of water in jug B.
        goal: The goal amount of water in the jugs.
        states_seen: A list of all states seen by the puzzle.
    """

    def __init__(self, jug_a: str, jug_b: str, goal: int) -> None:
        self.update(jug_a, jug_b, goal)

    def __str__(self) -> str:
        return f'WaterJugPuzzle(jug_a={_list_to_string(self.jug_a)}, jug_b={_list_to_string(self.jug_b)}, goal={self.goal}, states_seen={self.states_seen})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return self.jug_a == other.jug_a and self.jug_b == other.jug_b and \
               self.goal == other.goal

    def update(self, jug_a: str, jug_b: str, goal: int) -> None:
        """Updates the puzzle with the specified jugs and goal."""
        jug_a, jug_b = _string_to_int_list(jug_a), _string_to_int_list(jug_b)

        if len(jug_a) != 2 or len(jug_b) != 2:
            raise ValueError('Jugs must have two values. e.g. 3/7 or 1/5')
        elif jug_a[1] <= 0 or jug_b[1] <= 0:
            raise ValueError('Jugs capacity must be greater than zero.')
        elif jug_a[0] > jug_a[1] or jug_b[0] > jug_b[1]:
            raise ValueError('Jugs must have a capacity greater than the current amount.')
        elif jug_a[1] < goal and jug_b[1] < goal:
            raise ValueError('The goal must be less than or equal to the biggest capacity.')

        self.jug_a = jug_a
        self.jug_b = jug_b
        self.goal = goal
        self.states_seen = LinkedList(f'({_list_to_string(self.jug_a)}, {_list_to_string(self.jug_b)})')

    def done(self) -> bool:
        """Returns true if the puzzle is solved, false otherwise."""
        return self.jug_a[0] == self.goal or self.jug_b[0] == self.goal

    def states(self) -> LinkedList:
        """Returns a list of all states seen by the puzzle."""
        return self.states_seen

    def apply(self, rule: int) -> bool:
        """Applies the specified rule to the puzzle."""
        jug_a_amount, jug_a_capacity = self.jug_a
        jug_b_amount, jug_b_capacity = self.jug_b

        if rule == 0:
            jug_a_amount, jug_b_amount = 0, 0
        elif rule == 1:
            jug_a_amount = 0
        elif rule == 2:
            jug_b_amount = 0
        elif rule == 3:
            jug_a_amount, jug_b_amount = jug_a_capacity, jug_b_capacity
        elif rule == 4:
            jug_a_amount = jug_a_capacity
        elif rule == 5:
            jug_b_amount = jug_b_capacity
        elif rule == 6:
            addition = jug_a_amount + jug_b_amount
            addition = addition if addition <= jug_b_capacity else jug_b_capacity
            reduction = jug_a_amount - (jug_b_capacity-jug_b_amount)
            reduction = max(reduction, 0)
            jug_a_amount, jug_b_amount = reduction, addition
        elif rule == 7:
            addition = jug_a_amount + jug_b_amount
            addition = addition if addition <= jug_a_capacity else jug_a_capacity
            reduction = jug_b_amount - (jug_a_capacity-jug_a_amount)
            reduction = max(reduction, 0)
            jug_a_amount, jug_b_amount = addition, reduction
        else:
            raise ValueError('Rule must be between 0 and 7.')

        self.jug_a[0], self.jug_b[0] = jug_a_amount, jug_b_amount
        self.states_seen += f'({_list_to_string(self.jug_a)}, {_list_to_string(self.jug_b)})'
        return self.done()

    def solve(self) -> bool:
        """Solves the puzzle and returns the solution."""
        jug_a_amount, jug_a_capacity = self.jug_a
        jug_b_amount, jug_b_capacity = self.jug_b

        if self.goal == 0:
            if jug_a_amount > 0 or jug_b_amount > 0:
                self.apply(1 if jug_a_amount > 0 else 2)  # Empty the jug with the most water
        elif jug_a_capacity == self.goal or jug_b_capacity == self.goal:
            self.apply(4 if jug_a_capacity >= self.goal else 5)  # Fill the suitable jug
        elif jug_a_amount + jug_b_amount == self.goal and max(jug_a_capacity, jug_b_capacity) >= self.goal:  # Checks for a suitable jug
            self.apply(6 if jug_a_capacity <= jug_b_capacity else 7)
        elif jug_a_amount - (jug_b_capacity-jug_b_amount) == self.goal:
            self.apply(6)  # Pour jug A into jug B
        elif jug_b_amount - (jug_a_capacity-jug_a_amount) == self.goal:
            self.apply(7)  # Pour jug B into jug A
        elif max(jug_a_amount, jug_b_amount) - min(jug_a_capacity, jug_b_capacity) == self.goal:
            self.apply(1 if jug_a_capacity <= jug_b_capacity else 2)  # Empty the smaller jug
            self.apply(7 if jug_a_capacity <= jug_b_capacity else 6)  # Pour from the bigger jug
        elif max(jug_a_capacity, jug_b_capacity) - min(jug_a_capacity, jug_b_capacity) == self.goal:
            self.apply(3)  # Fill both jugs and then act like the above
            self.apply(1 if jug_a_capacity <= jug_b_capacity else 2)
            self.apply(7 if jug_a_capacity <= jug_b_capacity else 6)

        return self.done()


if __name__ == '__main__':
    import re
    import sys

    jugs = input('Enter the capacity and initial state of the jugs (e.g. 3/4, 7/8): ')
    values = [int(x) for x in re.findall(r'\d+', jugs)]
    if len(values) != 4:
        print('Format must be initial amount A/capacity A, initial amount B/capacity B. e.g. 1/2 as A and 0/85 as B.')
        sys.exit(1)

    goal = input('What is the goal amount of water in the jugs? ')
    if not goal.isnumeric():
        print('Goal must be greater or equal to zero. e.g. 0, 1, 2, etc.')
        sys.exit(1)

    try:
        water_juz_puzzle = WaterJugPuzzle(f'{values[0]}/{values[1]}', f'{values[2]}/{values[3]}', int(goal))
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f'\nIs the puzzle solved?! {"Yeah, of course" if water_juz_puzzle.solve() else "No, sorry dude"}...')
    print(f'Solution: {" -> ".join(water_juz_puzzle.states())}')
