from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

from typing import Optional

from .color_codes import EGO_ROBOT_CELL, ROBOT_CELL, VISIBILITY_0, VISIBILITY_100, VISIBILITY_20, VISIBILITY_40, VISIBILITY_60, VISIBILITY_80
from .metrics_calculator import calculate_metrics


cmap = colors.ListedColormap(["red", "blue", (0.0, 0.0, 0.0),(0.2, 0.2, 0.2), (0.4, 0.4, 0.4), (0.6, 0.6, 0.6), (0.8, 0.8, 0.8), (1.0, 1.0, 1.0)])
bounds = [EGO_ROBOT_CELL, ROBOT_CELL, VISIBILITY_0, VISIBILITY_20, VISIBILITY_40, VISIBILITY_60, VISIBILITY_80, VISIBILITY_100]
norm = colors.BoundaryNorm(bounds, cmap.N)


def visualize(cost_map_synapse, cost_map_single, synapse_score, single_score, hurdles, save_dir: str, counter: int, robot_position: dict, visualize_ego_only: bool):
    
    if hurdles:
        for hurdle in hurdles:
            cost_map_synapse[hurdle["row_idx"]][hurdle["col_idx"]] = EGO_ROBOT_CELL


    fig, ax = plt.subplots(ncols=2)
    
    
    ax[0].imshow(cost_map_single, cmap=cmap, norm=norm)
    ax[0].grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    ax[0].set_xticks(np.arange(0.5, cost_map_single.shape[0], 1))
    ax[0].set_yticks(np.arange(0.5, cost_map_single.shape[1], 1))
    ax[0].axis("off")
    ax[0].title.set_text(f'Current Approach\n\nPerception score: {int(single_score)}')
    
    ax[1].imshow(cost_map_synapse, cmap=cmap, norm=norm)
    ax[1].grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    ax[1].set_xticks(np.arange(0.5, cost_map_synapse.shape[0], 1))
    ax[1].set_yticks(np.arange(0.5, cost_map_synapse.shape[1], 1))
    ax[1].title.set_text(f'With Synapse\n\nPerception score: {int(synapse_score)}')
    ax[1].axis("off")
    
    fig.set_size_inches((8.5, 11), forward=False)
        
    if save_dir:
        plt.savefig(save_dir + "cost_map_" f"_{counter}" + ".png", dpi=500)
    else: 
        plt.show()
    

def store_map(cost_map_synapse, 
              cost_map_single,
              warehouse_db,
              save_dir: Optional[str] = None, 
              hurdles = [], 
              counter = None, 
              robot_position=None, 
              visualize_ego_only=False):

    
    for key, cost_val in warehouse_db.db.items():
        cost_map_synapse[key[0]][key[1]] = cost_val
    
    for key, cost_val in warehouse_db.single_db.items():
        cost_map_single[key[0]][key[1]] = cost_val


    # visualize
    single_score = calculate_metrics(cost_map_single, robot_position["1"], det_range=5)
    synapse_score = calculate_metrics(cost_map_synapse, robot_position["1"], det_range=5)    
    
    visualize(cost_map_synapse, cost_map_single, synapse_score, single_score, hurdles, save_dir, counter, robot_position=robot_position, visualize_ego_only=visualize_ego_only)
    

def main_generate(config, 
         save_dir, 
         warehouse_db,
         counter: Optional[int] = None, 
         robot_position: Optional[dict] = None, 
         visualize_ego_only=False):

    num_rows = config["cost_map"]["max_rows"]
    num_cols = config["cost_map"]["max_cols"]
    
    hurdles = config["hurdles"]
    
    # initialize init cost_map
    cost_map_synapse = np.zeros(num_rows * num_cols).reshape(num_rows, num_cols)
    cost_map_single = np.zeros(num_rows * num_cols).reshape(num_rows, num_cols)

    store_map(cost_map_synapse, cost_map_single, hurdles=hurdles, save_dir=save_dir, counter=counter, robot_position=robot_position, visualize_ego_only=visualize_ego_only, warehouse_db=warehouse_db)
    
