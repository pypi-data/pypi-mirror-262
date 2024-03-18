import yaml
import numpy as np
import os
import logging
import cv2
import os

from .color_codes import EGO_ROBOT_CELL, ROBOT_CELL, VISIBILITY_100
from .generate_cost_map import main_generate
from .robot_simulator import Robot_Simulator
from .warehouse_occ_grid_db import WarehouseOccGridDB


class Warehouse:
    
    def __init__(self, config, save_dir, visualize_ego_only):
        logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger()
        self.config = config
        self.robots = self.spawn_robots()
        self.counter = 0 
        self.save_dir = save_dir
        self.visualize_ego_only = visualize_ego_only
        self.warehouse_occ_grid_db = WarehouseOccGridDB()
    
    def spawn_robots(self):
        robots = []
        for robot_config in self.config["robot_batch"]:
            robot = Robot_Simulator(
                robot_id = robot_config["robot_id"],
                start_pos_x=robot_config["start_pos_x"], 
                start_pos_y=robot_config["start_pos_y"], 
                start_vel_x=robot_config["start_vel_x"], 
                start_vel_y=robot_config["start_vel_y"], 
                perc_range=robot_config["perc_range"],
                config=self.config)
            robots.append(robot)
            
        return robots
        
        
    def generate_zeros_occupancy_grid(self):
        num_rows = self.config["cost_map"]["max_rows"]
        num_cols = self.config["cost_map"]["max_cols"]
        return np.zeros(num_rows * num_cols).reshape(num_rows, num_cols) 
    
    @property
    def step(self):
        robot_pos_cache = {}
        for robot in self.robots:
            curr_occ_grid = self.generate_zeros_occupancy_grid()
            robot.step
            
            robot_pos_cache[robot.robot_id] = (robot.pos_x, robot.pos_y)
            
            for visible_cell in robot.visible_cells:
                curr_occ_grid[visible_cell[0]][visible_cell[1]] = VISIBILITY_100

            
            for r in range(curr_occ_grid.shape[0]):
                for c in range(curr_occ_grid.shape[1]):
                    if curr_occ_grid[r][c] != 0:
                        self.warehouse_occ_grid_db.add_cell_data(
                            {
                                "key": (r, c),
                                "cost_val": curr_occ_grid[r][c]
                            }
                        )
            if robot.robot_id == "1":
                for r in range(curr_occ_grid.shape[0]):
                    for c in range(curr_occ_grid.shape[1]):
                        if curr_occ_grid[r][c] != 0:
                            self.warehouse_occ_grid_db.add_cell_data_single(
                                {
                                    "key": (r, c),
                                    "cost_val": curr_occ_grid[r][c]
                                }
                            )
                
                    
            
        # publish robot positions
        for robot_id, robot_pos in robot_pos_cache.items():
            if robot_id == "1":
                self.warehouse_occ_grid_db.add_cell_data(
                    {
                        "key": (robot_pos[0], robot_pos[1]), 
                        "cost_val": ROBOT_CELL
                    }
                )
                self.warehouse_occ_grid_db.add_cell_data_single(
                    {
                        "key": (robot_pos[0], robot_pos[1]), 
                        "cost_val": ROBOT_CELL
                    }
                )
            else: 
                self.warehouse_occ_grid_db.add_cell_data(
                    {
                        "key": (robot_pos[0], robot_pos[1]), 
                        "cost_val": EGO_ROBOT_CELL
                    }
                )
        
        # generate cost map
        main_generate(self.config, 
                      counter=self.counter, 
                      robot_position=robot_pos_cache, 
                      save_dir=self.save_dir, 
                      visualize_ego_only=self.visualize_ego_only, 
                      warehouse_db=self.warehouse_occ_grid_db)
        
        # decay
        self.warehouse_occ_grid_db.decay_occ_grid
                
        self.counter += 1
        self.logger.info(f"Launch Robot Simulator ==> Completed iteration: {self.counter}")
        


def setup_configs_env_vars(config_path: str, save_dir: str):
    stream = open(config_path, 'r')
    config = yaml.load(stream, Loader=yaml.FullLoader)
    os.makedirs(save_dir, exist_ok=True)
    
    return config
    

def main_synapse_eyes(config_path: str = "/Users/apoorvsingh/repo_synapse/app/synapsebev/src/synapse_eyes/config.yml", 
              video_out_path: str = "video.avi"
              ):
    save_dir = "data/"
    config = setup_configs_env_vars(config_path=config_path, save_dir=save_dir)
    warehouse = Warehouse(config, save_dir=save_dir, visualize_ego_only=True)
    
    counter = 0
    
    while counter<40: 
        warehouse.step
        counter += 1
    

    images = [img for img in os.listdir(save_dir) if img.endswith(".png")]
    
    images = sorted(images)
    
    frame = cv2.imread(os.path.join(save_dir, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_out_path, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(save_dir, image)))

    cv2.destroyAllWindows()
    video.release()
    
    
# if __name__ == "__main__":
#     main_synapse_eyes()