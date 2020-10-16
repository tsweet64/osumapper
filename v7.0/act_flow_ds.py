'use strict'; # In case of future updates if Python wanted to mimic JS

#
# Part 4 Save Flow Dataset
#

import numpy as np;
import os;

root = "mapdata/";

divisor = 4;

def step3_set_params(note_group_size=10, step_size=5):
    return note_group_size, step_size;

def read_map_npz_flow(file_path):
    with np.load(file_path) as data:
        flow_data = data["flow"];
    return flow_data;

# TICK, TIME, TYPE, X, Y, IN_DX, IN_DY, OUT_DX, OUT_DY
def step3_read_maps_flow(params):
    chunk_size, step_size = params;

    max_x = 512;
    max_y = 384;

    result = [];
    for file in os.listdir(root):
        if file.endswith(".npz"):
            #print(os.path.join(root, file));
            flow_data = read_map_npz_flow(os.path.join(root, file));
            for i in range(0, (flow_data.shape[0] - chunk_size) // step_size):
                chunk = flow_data[i * step_size:i * step_size + chunk_size];
                result.append(chunk);

    # normalize the TICK col and remove TIME col
    result = np.array(result)
    result[:, :, 0] %= divisor;
    result[:, :, 3] /= max_x;
    result[:, :, 4] /= max_y;
    result[:, :, 9] /= max_x;
    result[:, :, 10] /= max_y;

    # TICK, TIME, TYPE, X, Y, IN_DX, IN_DY, OUT_DX, OUT_DY, END_X, END_Y
    # only use X,Y,OUT_DX,OUT_DY,END_X,END_Y
    used_indices = [3, 4, 7, 8, 9, 10]#np.concatenate([, range(11, 11 + divisor + 1)])
    result = np.array(result)[:, :, used_indices];
    return result;

def step3_save_flow_dataset(maps_flow):
    np.savez_compressed("flow_dataset", maps = maps_flow);