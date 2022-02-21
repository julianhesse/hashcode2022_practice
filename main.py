from solver_base import Solver_Base

def main():

    for fname in ["a_an_example.in", "b_basic.in", "c_coarse.in", "d_difficult", "e_elaborate.in"]:
        Solver_Base(name=fname).compute_solution()

if __name__ == "__main__":
    main()
