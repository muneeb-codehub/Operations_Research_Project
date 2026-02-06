"""
CloudOptima Data Generator
Generates realistic cloud computing optimization data
"""

import pandas as pd
import numpy as np

def generate_linear_programming_data():
    """Generate LP data for 10 VM types with 10 constraints"""
    
    # 10 VM Types
    vm_types = [
        'Basic VM',
        'Micro VM', 
        'Small VM',
        'Medium VM',
        'Large VM',
        'Memory VM',
        'Compute VM',
        'Storage VM',
        'GPU VM',
        'Metal VM'
    ]
    
    # Realistic profit per hour for each VM type
    profits = [5, 12, 25, 50, 95, 180, 350, 420, 850, 1200]
    
    # Maximum instances based on resource constraints
    max_instances = [500, 400, 300, 200, 150, 80, 50, 30, 20, 10]
    
    # Resource consumption per instance (for 10 constraints)
    # CPU cores, RAM (GB), SSD (TB), HDD (TB), Power (W), Cooling (BTU), 
    # Network (Gbps), Rack Units, Licenses, IP addresses
    
    resource_matrix = np.array([
        [1, 0.5, 10, 50, 50, 170, 0.1, 1, 0, 1],      # Nano
        [2, 1, 20, 100, 100, 340, 0.2, 1, 0, 1],       # Micro
        [4, 4, 50, 200, 250, 850, 0.5, 2, 0, 1],       # Small
        [8, 8, 100, 400, 500, 1700, 1.0, 3, 1, 1],     # Medium
        [16, 16, 200, 800, 1000, 3400, 2.0, 4, 1, 1],  # Large
        [16, 64, 250, 1000, 1200, 4100, 2.5, 5, 1, 1], # XL Memory
        [32, 32, 300, 1200, 2000, 6800, 4.0, 6, 1, 2], # 2XL Compute
        [32, 64, 2000, 5000, 2500, 8500, 5.0, 8, 1, 2],# 4XL Storage
        [64, 128, 500, 2000, 5000, 17000, 10.0, 10, 2, 4], # GPU
        [96, 256, 1000, 10000, 8000, 27200, 20.0, 20, 4, 8] # Bare Metal
    ])
    
    # Total available resources (constraints)
    total_resources = [
        50000,   # Total CPU cores
        100000,  # Total RAM (GB)
        150000,  # Total SSD (TB)
        500000,  # Total HDD (TB)
        1000000, # Total Power (W)
        3000000, # Total Cooling (BTU)
        5000,    # Total Network (Gbps)
        25000,   # Total Rack Units
        5000,    # Total Windows Licenses
        10000    # Total IP addresses
    ]
    
    constraint_names = [
        'CPU Limit',
        'RAM Limit',
        'SSD Limit',
        'HDD Limit',
        'Power Limit',
        'Cooling Limit',
        'Bandwidth Limit',
        'Rack Space Limit',
        'License Limit',
        'IP Limit'
    ]
    
    # Create DataFrame
    df = pd.DataFrame({
        'VM_Type': vm_types,
        'Profit_per_Hour': profits,
        'Max_Instances': max_instances,
    })
    
    # Add resource consumption columns
    for i, constraint in enumerate(constraint_names):
        df[f'Consumes_{constraint}'] = resource_matrix[:, i]
    
    # Add constraint limits as separate rows at the bottom
    constraint_df = pd.DataFrame({
        'VM_Type': constraint_names,
        'Profit_per_Hour': [''] * 10,
        'Max_Instances': total_resources,
    })
    
    # Fill constraint resource columns with labels
    for i, constraint in enumerate(constraint_names):
        constraint_df[f'Consumes_{constraint}'] = ['LIMIT'] + [''] * 9 if i == 0 else ''
    
    return df, constraint_df


def generate_assignment_data():
    """Generate 10x10 assignment matrix: Jobs to Server Nodes"""
    
    jobs = [
        'DB Task',
        'Video Task',
        'ML Task',
        'Logs Task',
        'Crypto Task',
        'Compile Task',
        'Render Task',
        'Traffic Task',
        'Zip Task',
        'Scan Task'
    ]
    
    nodes = [f'Node {chr(65+i)}' for i in range(10)]  # Node A to Node J
    
    # Generate realistic processing times (minutes)
    # Different jobs perform differently on different hardware
    np.random.seed(42)
    
    # Base times for each job
    base_times = [45, 120, 180, 30, 90, 60, 150, 100, 40, 55]
    
    # Generate matrix with variations
    cost_matrix = []
    for base_time in base_times:
        # Add randomness: ±30% variation across nodes
        row = np.random.randint(
            int(base_time * 0.7), 
            int(base_time * 1.3), 
            size=10
        )
        cost_matrix.append(row)
    
    df = pd.DataFrame(cost_matrix, index=jobs, columns=nodes)
    
    return df


def generate_transportation_data():
    """Generate 10x10 transportation: Data Centers to Storage Vaults"""
    
    data_centers = [
        'Center 1',
        'Center 2',
        'Center 3',
        'Center 4',
        'Center 5',
        'Center 6',
        'Center 7',
        'Center 8',
        'Center 9',
        'Center 10'
    ]
    
    storage_vaults = [f'Vault {i+1}' for i in range(10)]
    
    # Supply (TB of data to backup from each DC)
    np.random.seed(42)
    supply = np.random.randint(500, 1500, size=10)
    
    # Demand (TB capacity at each vault)
    # Make sure total supply ≈ total demand for balanced problem
    demand = supply.copy()
    np.random.shuffle(demand)
    
    # Adjust to make exactly balanced
    total_supply = supply.sum()
    total_demand = demand.sum()
    if total_supply != total_demand:
        demand[-1] += (total_supply - total_demand)
    
    # Cost matrix ($ per TB transfer)
    # Based on distance, bandwidth costs, etc.
    cost_matrix = np.random.uniform(0.5, 15.0, size=(10, 10))
    
    # Make diagonal cheaper (same region transfers)
    for i in range(10):
        cost_matrix[i][i] = np.random.uniform(0.1, 1.0)
    
    # Round to 2 decimals
    cost_matrix = np.round(cost_matrix, 2)
    
    # Create DataFrame
    df = pd.DataFrame(cost_matrix, index=data_centers, columns=storage_vaults)
    
    # Add supply column
    df['Supply_TB'] = supply
    
    # Add demand row at bottom
    demand_row = pd.DataFrame([demand], columns=storage_vaults, index=['Demand_TB'])
    demand_row['Supply_TB'] = ''
    
    return df, demand_row


def create_excel_file():
    """Create complete Excel file with all three sheets"""
    
    filename = 'CloudOptima_OR_Data.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Sheet 1: Linear Programming
        lp_df, constraint_df = generate_linear_programming_data()
        lp_df.to_excel(writer, sheet_name='Linear_Programming', index=False)
        
        # Add constraint limits below the main data
        constraint_df.to_excel(writer, sheet_name='Linear_Programming', 
                              startrow=len(lp_df)+2, index=False)
        
        # Sheet 2: Assignment Problem
        assignment_df = generate_assignment_data()
        assignment_df.to_excel(writer, sheet_name='Assignment_Problem')
        
        # Sheet 3: Transportation Problem
        transport_df, demand_row = generate_transportation_data()
        transport_df.to_excel(writer, sheet_name='Transportation_Problem')
        
        # Add demand row
        demand_row.to_excel(writer, sheet_name='Transportation_Problem',
                           startrow=len(transport_df)+1)
    
    print(f"✅ Created {filename}")
    print(f"📊 Sheet 1: Linear_Programming (10 VM types, 10 constraints)")
    print(f"📊 Sheet 2: Assignment_Problem (10x10 jobs-to-nodes)")
    print(f"📊 Sheet 3: Transportation_Problem (10x10 DCs-to-vaults)")
    
    return filename


if __name__ == "__main__":
    create_excel_file()
    print("\n🎉 Data generation complete!")
