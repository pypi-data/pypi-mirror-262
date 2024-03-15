class PrefixAmounts:
    def __init__(self, container):
        assert hasattr(container, '__getitem__'), "Container must have operator []"
        assert hasattr(type(container[0]), '__add__'), "Type T must have operator +"

        self.prefix_amounts = [container[0]]
        for i in range(1, len(container)):
            self.prefix_amounts.append(self.prefix_amounts[i - 1] + container[i])

    def size(self):
        return len(self.prefix_amounts)

    def ask(self, left, right):
        return self.prefix_amounts[right] - (0 if left == 0 else self.prefix_amounts[left - 1])
