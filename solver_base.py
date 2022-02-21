from util import prep_dir
import itertools


class Solver_Base:
    def __init__(self, name):

        self.name = name
        self.num_clients = None
        self.ing_liked = []
        self.ing_disliked = []
        self.ingredients = []

        self.read_data()

    def read_data(self):
        path = "data/" + self.name + ".txt"
        lines = open(path).read().splitlines()
        self.num_clients = int(lines[0])

        for i in range(1,self.num_clients*2,2):
            ing_liked = lines[i].split(' ')
            ing_disliked = lines[i+1].split(' ')
            print("ing_liked:", ing_liked)
            print("ing_disliked:", ing_disliked)
            self.ing_liked.append(ing_liked[1:])
            self.ing_disliked.append(ing_disliked[1:])

    # Remember: only save if new solution is better
    def save_solution(self, name=None):
        if name is None:
            name = self.name

        prep_dir("solutions")
        save_path = "solutions/" + name + "_solution.txt"
        save_file = open(save_path, "w+")

        save_file.write(str(len(self.ingredients)))
        for ing in self.ingredients:
            save_file.write(" " + ing)

    def validate(self):
        pass

    def overall_score(self):
        """Ingredients for only pizza saved in self.ingredients"""
        score = 0

        for ing_liked, ing_disliked in zip(self.ing_liked, self.ing_disliked):
            pizza_liked = set(ing_liked) & set(self.ingredients) == set(ing_liked)
            pizza_disliked = set(ing_disliked) & set(self.ingredients) != set()
            if pizza_liked and not pizza_disliked:
                score += 1

        return score


if __name__ == '__main__':
    test = Solver_Base("a_an_example.in")
    test.ingredients = ["cheese", "mushrooms", "tomatoes", "peppers"]
    print(test.overall_score())
    print(test.num_clients)
    print(test.ing_liked)
    print(test.ing_disliked)
    test.save_solution()
