

def calculate_metrics(cost_map, robot_pos, det_range):
    
    max_rows = cost_map.shape[0]
    max_cols = cost_map.shape[1]
    
    score = 0
    for r in range(robot_pos[0] - det_range, robot_pos[0] + det_range + 1):
        for c in range(robot_pos[1] - det_range, robot_pos[1] + det_range + 1):
            if r >= 0 and r < max_rows and c >= 0 and c < max_cols:
                if cost_map[r][c] < 0: 
                    score += 1
                else: 
                    score += cost_map[r][c]
    return score
