import yaml
from copy import deepcopy

from .utils import HighLevelNode, Constraints
from .environment import Environment


class CBS:
    def __init__(self, environment):
        self.env = environment
        self.open_set = set() # set of Highlevel nodes; Nodes which are yet to visit. 
        self.closed_set = set() # set of Highlevel nodes; Nodes which are already visited.
    
    def search(self):
        start = HighLevelNode()
        # TODO: Initialize it in a better way
        start.constraint_dict = {}
        for agent in self.env.agent_dict.keys():
            start.constraint_dict[agent] = Constraints()
        start.solution = self.env.compute_solution()
        if not start.solution:
            return {}
        start.cost = self.env.compute_solution_cost(start.solution)

        self.open_set |= {start}

        while self.open_set:
            P = min(self.open_set)
            self.open_set -= {P}
            self.closed_set |= {P}

            self.env.constraint_dict = P.constraint_dict
            conflict_dict = self.env.get_first_conflict(P.solution)
            if not conflict_dict:
                print("solution found")

                return self.generate_plan(P.solution)

            constraint_dict = self.env.create_constraints_from_conflict(conflict_dict)

            for agent in constraint_dict.keys():
                new_node = deepcopy(P)
                new_node.constraint_dict[agent].add_constraint(constraint_dict[agent])

                self.env.constraint_dict = new_node.constraint_dict
                new_node.solution = self.env.compute_solution()
                if not new_node.solution:
                    continue
                new_node.cost = self.env.compute_solution_cost(new_node.solution)

                # TODO: ending condition
                if new_node not in self.closed_set:
                    self.open_set |= {new_node}

        return {}

    def generate_plan(self, solution):
        plan = {}
        for agent, path in solution.items():
            path_dict_list = [{'t':state.time, 'x':state.location.x, 'y':state.location.y} for state in path]
            plan[agent] = path_dict_list
        return plan


def main_synapse_plan(config_file: str = "/Users/apoorvsingh/repo_synapse/synapse_plan/configs/config.yml", 
         output_file: str = "/Users/apoorvsingh/repo_synapse/synapse_plan/configs/output.yml"):

    # Read from input file
    with open(config_file, 'r') as param_file:
        try:
            config = yaml.load(param_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    dimension = config["map"]["dimensions"]
    obstacles = config["map"]["obstacles"]
    agents = config['agents']

    env = Environment(dimension, agents, obstacles)

    # Searching
    cbs = CBS(env)
    solution = cbs.search()
    if not solution:
        print(" Solution not found" )
        return

    # Write to output file
    output = dict()
    output["schedule"] = solution
    output["cost"] = env.compute_solution_cost(solution)
    with open(output_file, 'w') as output_yaml:
        yaml.safe_dump(output, output_yaml)


if __name__ == "__main__":
    main_synapse_plan()
