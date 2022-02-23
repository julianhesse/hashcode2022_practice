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

    def count_ing_list(self, ing_list):
        count = {}
        for list in ing_list:
            for ing in list:
                if ing not in count:
                    count[ing] = 1
                else:
                    count[ing] += 1
        
        return count

    def read_data(self):
        path = "data/" + self.name + ".txt"
        lines = open(path).read().splitlines()
        self.num_clients = int(lines[0])

        for i in range(1,self.num_clients*2,2):
            ing_liked = lines[i].split(' ')
            ing_disliked = lines[i+1].split(' ')
            # print("ing_liked:", ing_liked)
            # print("ing_disliked:", ing_disliked)
            self.ing_liked.append(ing_liked[1:])
            self.ing_disliked.append(ing_disliked[1:])

    def simple_solution(self):
        liked_counts = self.count_ing_list(self.ing_liked)
        disliked_counts = self.count_ing_list(self.ing_disliked)
        self.ingredients = list(liked_counts.keys())

        removed = []

        for key, value in disliked_counts.items():
            if key in liked_counts and liked_counts[key] < value:
                score_prev = self.overall_score()
                self.ingredients.remove(key)
                if self.overall_score() < score_prev:
                    self.ingredients.append(key)
                else:
                    removed.append(key)

        for ing in removed:
            score_prev = self.overall_score()
            self.ingredients.append(ing)
            if self.overall_score() < score_prev:
                self.ingredients.remove(ing)


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
        return self.ingredients is list

    def overall_score(self):
        """Ingredients for only pizza saved in self.ingredients"""
        score = 0

        # for ing_liked, ing_disliked in zip(self.ing_liked, self.ing_disliked):
        #     pizza_liked = set(ing_liked) & set(self.ingredients) == set(ing_liked)
        #     pizza_disliked = set(ing_disliked) & set(self.ingredients) != set()
        #     if pizza_liked and not pizza_disliked:
        #         score += 1

        for ing_liked, ing_disliked in zip(self.ing_liked, self.ing_disliked):
            pizza_liked = sum([ing in self.ingredients for ing in ing_liked]) == len (ing_liked)
            pizza_disliked = sum([ing in self.ingredients for ing in ing_disliked]) > 0
            if pizza_liked and not pizza_disliked:
                score += 1

        return score


if __name__ == '__main__':
    files = ["a_an_example.in", "b_basic.in", "c_coarse.in", "d_difficult.in", "e_elaborate.in"]
    test = Solver_Base(files[4])
    print(test.count_ing_list(test.ing_disliked))
    print(test.count_ing_list(test.ing_liked))
    print(test.num_clients)
    # print(test.ing_liked)
    # print(test.ing_disliked)
    test.simple_solution()
    print(test.overall_score())
    test.save_solution()