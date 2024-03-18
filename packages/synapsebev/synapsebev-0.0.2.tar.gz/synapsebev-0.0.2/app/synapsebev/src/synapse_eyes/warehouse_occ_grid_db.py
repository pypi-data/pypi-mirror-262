class WarehouseOccGridDB:
    def __init__(self):
        self.db = {}
        self.single_db = {}
    
    def add_cell_data(self, item):
        self.db[item["key"]] = item["cost_val"]
    
    def add_cell_data_single(self, item):
        self.single_db[item["key"]] = item["cost_val"]

    @property
    def decay_occ_grid(self):
        keys_to_remove = []
        for key, cost_val in self.db.items():
            decayed_cost_val = cost_val -0.2
            self.db[key] = decayed_cost_val
            if decayed_cost_val <= 0.01:
                keys_to_remove.append(key)
        
        for key in keys_to_remove: 
            self.db.pop(key)
        
        # for single
        keys_to_remove = []
        for key, cost_val in self.single_db.items():
            decayed_cost_val = cost_val -0.2
            self.single_db[key] = decayed_cost_val
            if decayed_cost_val <= 0.01:
                keys_to_remove.append(key)
        
        for key in keys_to_remove: 
            self.single_db.pop(key)
            
                