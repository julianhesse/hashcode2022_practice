from util import prep_dir
import itertools
import numpy as np
import pandas as pd


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

        score_prev = self.overall_score()
        for ing in removed:
            self.ingredients.append(ing)
            score_new = self.overall_score()
            if score_new < score_prev:
                self.ingredients.pop()
            else:
                score_prev = score_new

        removed = list(set(removed))

        for i in range(4):

            for ing in self.ingredients:
                self.ingredients.remove(ing)
                score_new = self.overall_score()
                if score_new < score_prev:
                    self.ingredients.append(ing)
                else:
                    score_prev = score_new
                    removed.append(ing)

            self.ingredients = list(set(self.ingredients))

            for ing in removed:
                self.ingredients.append(ing)
                score_new = self.overall_score()
                if score_new < score_prev:
                    self.ingredients.pop()
                else:
                    score_prev = score_new

            removed = list(set(removed))

        self.ingredients = list(set(self.ingredients))

    def random_solution(self):
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

        score_prev = self.overall_score()
        random_selection = np.random.choice(removed, len(removed)*2)
        for ing in random_selection:
            self.ingredients.append(ing)
            score_new = self.overall_score()
            if score_new < score_prev:
                self.ingredients.pop()
                score_prev = score_new

    
    def pandas_solution(self):
        liked_counts = self.count_ing_list(self.ing_liked)
        disliked_counts = self.count_ing_list(self.ing_disliked)
        self.ingredients = list(liked_counts.keys())

        df = pd.DataFrame({'liked': list(self.ing_liked), 'disliked': list(self.ing_disliked)})

        like_scores = []
        dislike_scores = []
        for ing_liked, ing_disliked in zip(self.ing_liked, self.ing_disliked):
            # calc a score for liked ingredients by how frequent the ingredients are
            like_score = sum([liked_counts[ing] for ing in ing_liked])
            like_scores.append(like_score)

            # calc a score for disliked ingredients by how frequent the ingredients are
            dislike_score = sum([disliked_counts[ing] for ing in ing_disliked])
            dislike_scores.append(dislike_score)

        df['like score'] = like_scores
        df['avg like score'] = list(map(lambda x, y: (x/len(y)) if x else 0, df['like score'], df['liked']))
        df['dislike score'] = dislike_scores
        df['avg dislike score'] = list(map(lambda x, y: (x/len(y)) if x else 0, df['dislike score'], df['disliked']))

        print(df)

        # df = df.sort_values(by=['like score', 'dislike score'], ascending=[False, True])
        df = df.sort_values(by=['avg like score', 'avg dislike score'], ascending=[False, True])
        # df = df.sort_values(by=['dislike score', 'like score'], ascending=[True, False])
        # df = df.sort_values(by=['avg dislike score', 'avg like score'], ascending=[True, False])
        print(df)

        prev_score = self.overall_score()
        for i in df.index:
            ingredients = set(self.ingredients) # optimization
            # find out if removing disliked ingredients is increasing the score
            disliked_ing = []
            for ing in df.iloc[i]['disliked']:
                if ing in ingredients:
                    disliked_ing.append(ing)

            for ing in disliked_ing:
                self.ingredients.remove(ing)

            new_score = self.overall_score()
            if prev_score > new_score:
                self.ingredients.extend(disliked_ing)
            else:
                prev_score = new_score

        # prev_score = self.overall_score()
        # for i in df.index:
        #     ingredients = set(self.ingredients) # optimization
        #     # find out if adding disliked ingredients are increasing the score
        #     disliked_ing = []
        #     for ing in df.iloc[i]['disliked']:
        #         if ing not in ingredients:
        #             disliked_ing.append(ing)

        #     self.ingredients.extend(ing)

        #     new_score = self.overall_score()
        #     if prev_score > new_score:
        #         for ing in disliked_ing:
        #             self.ingredients.pop()
        #     else:
        #         prev_score = new_score

        for i in range(2):
            removed = set(list(liked_counts.keys())).difference(set(self.ingredients))
            score_prev = self.overall_score()
            for ing in removed:
                self.ingredients.append(ing)
                score_new = self.overall_score()
                if score_new < score_prev:
                    self.ingredients.pop()
                else:
                    score_prev = score_new

            # self.ingredients = list(set(self.ingredients))

            for ing in self.ingredients:
                self.ingredients.remove(ing)
                score_new = self.overall_score()
                if score_new < score_prev:
                    self.ingredients.append(ing)
                else:
                    score_prev = score_new

            self.ingredients = list(set(self.ingredients))

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

        ings = set(self.ingredients)
        for ing_liked, ing_disliked in zip(self.ing_liked, self.ing_disliked):
            pizza_liked = sum([ing in ings for ing in ing_liked]) == len (ing_liked)
            pizza_disliked = sum([ing in ings for ing in ing_disliked]) > 0
            if pizza_liked and not pizza_disliked:
                score += 1

        return score


if __name__ == '__main__':
    files = ["a_an_example.in", "b_basic.in", "c_coarse.in", "d_difficult.in", "e_elaborate.in"]
    test = Solver_Base(files[3])
    # print(test.count_ing_list(test.ing_disliked))
    # print(test.count_ing_list(test.ing_liked))
    print(len(test.count_ing_list(test.ing_disliked)))
    print(len(test.count_ing_list(test.ing_liked)))
    print(test.num_clients)
    # print(test.ing_liked)
    # print(test.ing_disliked)
    test.pandas_solution()
    print(test.overall_score())
    test.save_solution()