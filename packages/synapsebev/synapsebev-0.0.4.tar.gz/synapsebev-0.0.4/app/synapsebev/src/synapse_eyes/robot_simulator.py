
class Robot_Simulator:
    
    def __init__(self, robot_id, start_pos_x, start_pos_y, start_vel_x, start_vel_y, config, speed=1, perc_range=3):
        """
        :param start_dir: 0 right; 1 up; 2 left; 3 down. 
            if obstruction is struck --> First turns 90 degree anti-clockwise. Then takes a step.
        (0,0) is top-right of the grid.
        """
        self.robot_id = robot_id
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y
        self.vel_x = start_vel_x
        self.vel_y = start_vel_y
        # self.speed = speed
        self.perc_range = perc_range
        
        self.config = config
        self.max_rows = config["cost_map"]["max_rows"]-1
        self.max_cols = config["cost_map"]["max_cols"]-1
        self.max_straight_line = 4
        self.curr_straight_line = 0
    
    def _reverse_vel(self, vel_value):
        return vel_value * -1
    
    def _update_pos_x(self, val):
        self.pos_x = self.pos_x + val
    
    def _update_pos_y(self, val):
        self.pos_y = self.pos_y + val
    
    @property
    def _self_validate_position(self):
        assert self.pos_y <= self.max_cols
        assert self.pos_y <= self.max_rows
        assert self.pos_y >= 0
        assert self.pos_y >= 0
    
    
    @property
    def step_x(self):
        if self.vel_x != 0: 
            if self.vel_x > 0: 
                if self.pos_x == self.max_rows:
                    self.vel_x = self._reverse_vel(self.vel_x)
                    self.step_x
                else: 
                    self._update_pos_x(self.vel_x)
            elif self.vel_x <0:
                if self.pos_x == 0:
                    self.vel_x = self._reverse_vel(self.vel_x)
                    self.step_x
                else: 
                    self._update_pos_x(self.vel_x)
    
    @property
    def step_y(self):
        if self.vel_y != 0:
            if self.vel_y > 0: 
                if self.pos_y == self.max_cols:
                    self.vel_y = self._reverse_vel(self.vel_y)
                    self.step_y
                else: 
                    self._update_pos_y(self.vel_y)
            elif self.vel_y <0:
                if self.pos_y == 0:       
                    self.vel_y = self._reverse_vel(self.vel_y)
                    self.step_y
                else: 
                    self._update_pos_y(self.vel_y)
        
    
    @property
    def step(self):

        self._self_validate_position
        
        self.step_x
        self.step_y
        
        self.do_perception()
        
        
    def do_perception(self):
        
        self.visible_cells = []
        for r in range(self.pos_x -2, self.pos_x + 3):
            for c in range(self.pos_y -2, self.pos_y + 3):
                if r >= 0 and r <= self.max_rows and c >= 0 and c <= self.max_cols:
                    self.visible_cells.append((r, c))
        
        self.visible_cells