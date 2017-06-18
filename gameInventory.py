import unicodedata


class Inventory():

    def __init__(self, inventory):
        self.inventory = inventory

    def display_inventory(self):
        '''Simple inventory display'''
        print("Inventory: ")
        for key, value in self.inventory.items():
            print("{} {}".format(value, key))
        print("Total number of items:", sum(self.inventory.values()))

    def add_to_inventory(self, added_items):
        '''Adds loot from a given list'''
        for i in added_items:
            if i in self.inventory.keys():
                self.inventory[i] += 1
            else:
                self.inventory[i] = 1
        return self.inventory

    def max_unicode_char(self):
        '''Returns the most wide unicode characters in a single key'''
        max_char = 0
        for key in self.inventory.keys():
            count = 0
            for k in key:
                if unicodedata.east_asian_width(k) in ("W", "F"):
                    count += 1
            if count > max_char:
                max_char = count
        return max_char

    def print_table(self, order=None):
        '''
        Decorator for inventory display. Unoganized by deafault.
        You can set the order to 'count,desc' for descending order
        or 'count,asc' for ascending order.
        '''
        max_len_k = len(max(self.inventory.keys(), key=lambda x: len(x)))
        max_len_v = len(str(max(self.inventory.values(), key=lambda x: len(str(x)))))
        col_t = ["count", "item name"]
        col_w = [max_len_v, max_len_k]
        uni_char = self.max_unicode_char()
        pad_b = " " * (2 + uni_char)
        keys = self.inventory.keys()
        values = self.inventory.values()
        # compare the column titles lenght with the max lenght key and value
        for i, j in zip(col_t, range(len(col_w))):
            if len(i) > col_w[j]:
                col_w[j] = len(i)
        # if positional argument is given, sorts the list by values
        if order == "count,desc":
            values = sorted(self.inventory.values(), reverse=True)
            keys = sorted(self.inventory, key=self.inventory.get, reverse=True)
        elif order == "count,asc":
            values = sorted(self.inventory.values())
            keys = sorted(self.inventory, key=self.inventory.get)
        # print process
        print("Inventory:")
        print("{0:>{width_v}}{2}{1:>{width_k}}".format(col_t[0], col_t[1], pad_b, width_v=col_w[0], width_k=col_w[1]))
        print("-" * (sum(col_w)+len(pad_b)))

        for key, value in zip(keys, values):
            pad = " " * (2 + uni_char - sum(1 for k in key if unicodedata.east_asian_width(k) in ("W", "F")))
            print("{0:>{width_v}}{2}{1:>{width_k}}".format(value, key, pad, width_v=col_w[0], width_k=col_w[1]))

        print("-" * (sum(col_w)+len(pad_b)))
        print("Total number of items:", sum(values))

    def import_inventory(self, filename="import_inventory.csv"):
        '''Imports items from a given CSV file'''
        with open(filename, "r") as f:
            items = f.read()
        list_of_items = items.strip().split(",")
        self.inventory = self.add_to_inventory(list_of_items)
        return self.inventory

    def export_inventory(self, filename="export_inventory.csv"):
        '''Exports items to a given CSV file'''
        items_to_write = []
        for key in self.inventory.keys():
            for value in range(self.inventory[key]):
                items_to_write.append(key)
        with open(filename, "w") as f:
            to_write = ",".join(items_to_write)
            f.write(to_write)


def Main():
    inv = {
        # holds the items and the corresponding amounts
        "rope": 1,
        "torch": 6,
        "深入深入 katana": 42,
        "dagger": 1,
        "arrow": 12,
        "herbal root of the fallen king": 121,
        "golden rod": 2,
        "heirloom helm": 3
    }

    dragon_loot = [
        # loot from dragon
        "gold coin",
        "dagger",
        "gold coin",
        "gold coin",
        "ruby"
    ]

    inventory = Inventory(inv)
    inventory.print_table("count,desc")
    inventory.add_to_inventory(dragon_loot)
    print("Dragon loot added.")
    inventory.print_table()
    inventory.export_inventory()
    print("Inventory exported.")
    inventory.import_inventory()
    print("Inventory imported.")
    inventory.print_table()
    inventory.import_inventory("export_inventory.csv")
    print("Previously exported inventory imported.")
    inventory.print_table("count,asc")

if __name__ == "__main__":
    Main()
