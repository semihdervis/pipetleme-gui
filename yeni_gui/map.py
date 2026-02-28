import numpy as np
import os

def build_reagent_array(top, bottom, count=9):
    """
    Build a linear array of coordinates for reagent wells.
    
    Args:
        top: (x, y) coordinates of the topmost well
        bottom: (x, y) coordinates of the bottommost well
        count: Total number of wells (default: 9)
    
    Returns:
        numpy array of shape (count, 2) containing (x, y) coordinates
    """
    top, bottom = np.array(top, float), np.array(bottom, float)
    coords = np.zeros((count, 2), float)
    for i in range(count):
        # Interpolate between top and bottom positions
        t = i / (count - 1)  # t ranges from 0 to 1
        coords[i] = top + t * (bottom - top)
    return coords

def build_sample_array(top, bottom, count=16):
    """
    Build a linear array of coordinates for sample wells.
    
    Args:
        top: (x, y) coordinates of the topmost well
        bottom: (x, y) coordinates of the bottommost well
        count: Total number of wells (default: 16)
    
    Returns:
        numpy array of shape (count, 2) containing (x, y) coordinates
    """
    top, bottom = np.array(top, float), np.array(bottom, float)
    coords = np.zeros((count, 2), float)
    for i in range(count):
        # Interpolate between top and bottom positions
        t = i / (count - 1)  # t ranges from 0 to 1
        coords[i] = top + t * (bottom - top)
    return coords

def build_dilute_map(tl, tr, bl, rows=12, cols=8):
    """
    Build a 2D grid of coordinates for a dilution plate.
    
    Args:
        tl: (x, y) coordinates of top-left corner
        tr: (x, y) coordinates of top-right corner
        bl: (x, y) coordinates of bottom-left corner
        rows: Number of rows (default: 12)
        cols: Number of columns (default: 8)
    
    Returns:
        numpy array of shape (rows, cols, 2) containing (x, y) coordinates
    """
    tl, tr, bl = map(lambda p: np.array(p, float), (tl, tr, bl))
    # Calculate step sizes for horizontal and vertical directions
    step_x = (tr - tl) / (cols - 1)  # Horizontal step size
    step_y = (bl - tl) / (rows - 1)  # Vertical step size
    grid = np.zeros((rows, cols, 2), float)
    for i in range(rows):
        for j in range(cols):
            grid[i, j] = tl + j * step_x + i * step_y
    return grid

def build_card_map(tl, tr, bl,
                   rows_per_side=6,
                   wells_per_row=8,
                   gap_ratio=1/3):
    """
    Build coordinates for a card with two side-by-side blocks of wells.
    
    Args:
        tl: (x, y) coordinates of top-left corner of left block
        tr: (x, y) coordinates of top-right corner (defines total width)
        bl: (x, y) coordinates of bottom-left corner of left block
        rows_per_side: Number of rows per block (default: 6)
        wells_per_row: Number of wells per row (default: 8)
        gap_ratio: Ratio of gap width to block width (default: 1/3)
    
    Returns:
        numpy array of shape (total_rows, wells_per_row, 2) where:
        - Rows 0 to (rows_per_side-1): left block
        - Rows rows_per_side to (2*rows_per_side-1): right block
    """
    tl, tr, bl = map(lambda p: np.array(p, float), (tl, tr, bl))
    # Calculate main vectors
    X, Y = tr - tl, bl - tl  # X: total width, Y: block height
    step_row = Y / (rows_per_side - 1)  # Vertical step between rows
    # Split horizontal space: X = block + gap + block
    block_vec = X / (2 + gap_ratio)  # Width of one block
    gap_vec = block_vec * gap_ratio  # Width of gap between blocks
    step_well = block_vec / (wells_per_row - 1)  # Horizontal step between wells
    total_rows = rows_per_side * 2
    coords = np.zeros((total_rows, wells_per_row, 2), float)
    for i in range(rows_per_side):
        # Left block: calculate origin for this row
        row_origin_left = tl + i * step_row
        for j in range(wells_per_row):
            coords[i, j] = row_origin_left + j * step_well
        # Right block: same row, shifted to the right
        row_origin_right = row_origin_left + block_vec + gap_vec
        right_row_idx = i + rows_per_side
        for j in range(wells_per_row):
            coords[right_row_idx, j] = row_origin_right + j * step_well
    return coords

def compute_all_maps():
    """
    Compute coordinate maps for all lab equipment components.
    
    Returns:
        Dictionary containing coordinate arrays for:
        - r1, r2: reagent arrays (9 wells each)
        - s1, s2, s3: sample arrays (16 wells each)
        - liss, bromelin: single position reagents (above dilute plate)
        - d1, d2: dilution plates (12x8 grids, top and bottom)
        - c1, c2, c3, c4: card maps (4 cards, each with 12 rows x 8 wells)
    """
    maps = {}

    # Reagent arrays (vertical, 9 wells each) from main_screen coordinates
    maps["r1"] = build_reagent_array((25, 210), (25, 594), 9)
    maps["r2"] = build_reagent_array((80, 208), (80, 592), 9)

    # Sample arrays (vertical, 16 wells each) from main_screen coordinates
    maps["s1"] = build_sample_array((140, 32), (141, 592), 16)
    maps["s2"] = build_sample_array((180, 34), (181, 592), 16)
    maps["s3"] = build_sample_array((226, 38), (226, 589), 16)

    # Single position reagents above dilute plate
    maps["liss"] = np.array([309, 69], float)
    maps["bromelin"] = np.array([409, 69], float)
    maps["wash"] = np.array([300, -65], float)

    # Dilution plates (top and bottom) from main_screen coordinates
    maps["d1"] = build_dilute_map((282, 153), (405, 153), (282, 345))
    maps["d2"] = build_dilute_map((283, 414), (405, 414), (282, 610))

    # Card maps (4 cards) from main_screen coordinates
    maps["c1"] = build_card_map((520, -18), (820, -19), (520, 121))
    maps["c2"] = build_card_map((520, 181), (820, 181), (520, 320))
    maps["c3"] = build_card_map((520, 381), (820, 381), (520, 520))
    maps["c4"] = build_card_map((520, 581), (820, 581), (520, 720))

    return maps

SAVE_PATH = "coords.npz"

def save_maps(path, maps: dict):
    """
    Save coordinate maps to a compressed numpy file.
    
    Args:
        path: File path to save the maps
        maps: Dictionary of coordinate arrays to save
    """
    # np.savez saves each array separately in the compressed file
    np.savez(path, **maps)

def load_maps(path):
    """
    Load coordinate maps from a compressed numpy file.
    
    Args:
        path: File path to load the maps from
    
    Returns:
        Dictionary of coordinate arrays
    """
    data = np.load(path)
    # np.load returns an NpzFile object that can be used like a dict
    # Convert it to a regular dictionary for easier use
    return {k: data[k] for k in data.files}

def load_or_compute(path=SAVE_PATH):
    """
    Load maps from file if it exists, otherwise compute and save them.
    
    Args:
        path: File path to load from or save to (default: SAVE_PATH)
    
    Returns:
        Dictionary of coordinate arrays
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_PATH)
    if os.path.exists(path):
        return load_maps(path)
    else:
        maps = compute_all_maps()
        save_maps(path, maps)
        return maps

if __name__ == "__main__":
    # Load existing maps (or use load_or_compute() to generate if missing)
    maps = load_or_compute()

    # Example: Access 5th well (index 4) of 2nd reagent array
    print(maps["r2"][4])

    # Example: Access row 3, column 2 (indices 2, 1) of first dilution plate
    print(maps["d1"][2, 1])

    # Example: Access right block, row 7, well 3 (indices 7, 2) of card 2
    print(maps["c2"][7, 2])

    
    print(maps["liss"])
    print(maps["bromelin"])

    # ==================== Example Pipette Process ===================
    def move():
        """Placeholder for pipette movement function."""
        pass

    maps["c1"]



