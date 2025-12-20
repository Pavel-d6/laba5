import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src_bugs'))
from simulation import run_simulation


def main():
    run_simulation(steps=20, seed=43)

if __name__ == "__main__":
    main()