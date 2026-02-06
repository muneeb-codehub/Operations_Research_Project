"""
CloudOptima - Simplex Method Solver
Linear Programming for VM Instance Optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime


class SimplexSolver:
    """Simplex tableau solver with sensitivity analysis"""
    
    def __init__(self, c, A, b, var_names, constraint_names):
        self.c = c  # Objective coefficients
        self.A = A  # Constraint matrix
        self.b = b  # RHS values
        self.var_names = var_names
        self.constraint_names = constraint_names
        self.num_vars = len(c)
        self.num_constraints = len(b)
        self.iterations = []
        self.tableau = None
        
    def initialize_tableau(self):
        """Initialize simplex tableau with slack variables"""
        self.tableau = []
        
        # Add constraint rows with slack variables
        for i in range(self.num_constraints):
            row = list(self.A[i])
            # Add slack variables (identity matrix)
            for j in range(self.num_constraints):
                row.append(1 if i == j else 0)
            row.append(self.b[i])  # RHS
            self.tableau.append(row)
        
        # Add objective row (for maximization: -c)
        z_row = [-ci for ci in self.c]
        # Slack variables have 0 coefficient in objective
        for _ in range(self.num_constraints):
            z_row.append(0)
        z_row.append(0)  # Z value starts at 0
        
        self.tableau.insert(0, z_row)
        
        # Track basic variables
        self.basic_vars = [f"s{i+1}" for i in range(self.num_constraints)]
        self.all_vars = self.var_names + [f"s{i+1}" for i in range(self.num_constraints)]
    
    def get_tableau_string(self, iteration, entering=None, leaving=None):
        """Format tableau for display"""
        lines = []
        
        lines.append(f"\n{'='*90}")
        lines.append(f"ITERATION {iteration}")
        lines.append(f"{'='*90}")
        
        if iteration == 0:
            lines.append("Initial Tableau (Standard Form)")
        else:
            lines.append(f"After pivot operation")
        
        lines.append(f"\n{'Basic Var':<15} | {'Value (RHS)':>12} | Status")
        lines.append("-" * 90)
        
        # Z row
        z_value = self.tableau[0][-1]
        lines.append(f"{'Z (Profit)':<15} | ${z_value:>11,.2f} | {'Objective'}")
        
        # Constraint rows
        for i in range(1, len(self.tableau)):
            basic_var = self.basic_vars[i-1]
            value = self.tableau[i][-1]
            
            # Mark entering/leaving
            status = ""
            if leaving and leaving == basic_var:
                status = "← Leaving"
            elif entering is not None and self.all_vars[entering] == basic_var:
                status = "→ Entering"
            
            lines.append(f"{basic_var:<15} | {value:>12.2f} | {status}")
        
        if entering is not None:
            lines.append(f"\n➤ Entering variable: {self.all_vars[entering]}")
            lines.append(f"   (Most negative coefficient in Z row)")
        
        if leaving is not None:
            lines.append(f"➤ Leaving variable: {leaving}")
            lines.append(f"   (Minimum ratio test)")
        
        return "\n".join(lines)
    
    def solve(self):
        """Solve using Simplex method"""
        self.initialize_tableau()
        iteration = 0
        
        # Store initial tableau
        self.iterations.append(self.get_tableau_string(iteration))
        
        max_iterations = 50
        
        while iteration < max_iterations:
            # Step 1: Check optimality (all coefficients in Z row ≥ 0?)
            optimal = True
            entering_col = -1
            most_negative = 0
            
            # Check decision variables only (not slack variables)
            for j in range(self.num_vars):
                if self.tableau[0][j] < -1e-6:  # Negative coefficient
                    optimal = False
                    if self.tableau[0][j] < most_negative:
                        most_negative = self.tableau[0][j]
                        entering_col = j
            
            if optimal:
                self.iterations.append("\n✅ OPTIMAL SOLUTION REACHED!")
                self.iterations.append("All coefficients in objective row are non-negative.")
                break
            
            if entering_col == -1:
                break
            
            # Step 2: Minimum ratio test to find leaving variable
            min_ratio = float('inf')
            leaving_row = -1
            
            for i in range(1, len(self.tableau)):
                pivot_col_value = self.tableau[i][entering_col]
                if pivot_col_value > 1e-6:  # Positive values only
                    ratio = self.tableau[i][-1] / pivot_col_value
                    if ratio >= 0 and ratio < min_ratio:
                        min_ratio = ratio
                        leaving_row = i
            
            if leaving_row == -1:
                self.iterations.append("\n⚠️ Problem is UNBOUNDED")
                return None, "Unbounded", None
            
            iteration += 1
            leaving_var = self.basic_vars[leaving_row - 1]
            
            # Step 3: Pivot operation
            pivot_element = self.tableau[leaving_row][entering_col]
            
            # Normalize pivot row
            for j in range(len(self.tableau[leaving_row])):
                self.tableau[leaving_row][j] /= pivot_element
            
            # Eliminate entering variable from other rows
            for i in range(len(self.tableau)):
                if i != leaving_row:
                    multiplier = self.tableau[i][entering_col]
                    for j in range(len(self.tableau[i])):
                        self.tableau[i][j] -= multiplier * self.tableau[leaving_row][j]
            
            # Update basic variables
            self.basic_vars[leaving_row - 1] = self.all_vars[entering_col]
            
            # Store iteration
            self.iterations.append(self.get_tableau_string(
                iteration, entering_col, leaving_var
            ))
        
        if iteration >= max_iterations:
            self.iterations.append("\n⚠️ Maximum iterations reached")
        
        # Extract solution
        solution = {var: 0 for var in self.all_vars}
        
        for i in range(1, len(self.tableau)):
            var_name = self.basic_vars[i - 1]
            solution[var_name] = self.tableau[i][-1]
        
        z_value = self.tableau[0][-1]
        
        return solution, z_value, iteration
    
    def sensitivity_analysis(self, solution, z_value):
        """Perform sensitivity analysis on optimal solution"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("📊 SENSITIVITY ANALYSIS")
        lines.append("="*90)
        
        # Shadow Prices (dual values from slack variables in final tableau)
        lines.append("\n🔍 SHADOW PRICES (Marginal Value of Resources):")
        lines.append("-" * 70)
        lines.append(f"{'Constraint':<25} | {'Shadow Price':>15} | {'Interpretation'}")
        lines.append("-" * 70)
        
        for i in range(self.num_constraints):
            slack_col = self.num_vars + i
            shadow_price = -self.tableau[0][slack_col]  # Negative of Z-row coefficient
            
            constraint_name = self.constraint_names[i]
            
            interpretation = ""
            if abs(shadow_price) < 1e-6:
                interpretation = "Non-binding (surplus exists)"
            else:
                interpretation = f"${shadow_price:.2f} per unit increase"
            
            lines.append(f"{constraint_name:<25} | ${shadow_price:>14.2f} | {interpretation}")
        
        # Reduced Costs (for non-basic variables)
        lines.append("\n🔍 REDUCED COSTS (Cost to make non-basic variable profitable):")
        lines.append("-" * 70)
        lines.append(f"{'Variable':<20} | {'Reduced Cost':>15} | {'Status'}")
        lines.append("-" * 70)
        
        for j in range(self.num_vars):
            var_name = self.var_names[j]
            reduced_cost = self.tableau[0][j]
            
            status = "Basic (in solution)" if var_name in self.basic_vars else "Non-basic"
            
            lines.append(f"{var_name:<20} | ${reduced_cost:>14.2f} | {status}")
        
        # Resource Utilization
        lines.append("\n📊 RESOURCE UTILIZATION:")
        lines.append("-" * 70)
        lines.append(f"{'Resource':<25} | {'Used':>12} | {'Available':>12} | {'Slack':>12} | {'%Used':>8}")
        lines.append("-" * 70)
        
        for i in range(self.num_constraints):
            constraint_name = self.constraint_names[i]
            available = self.b[i]
            
            # Calculate used resources
            used = 0
            for j in range(self.num_vars):
                var_name = self.var_names[j]
                if var_name in self.basic_vars:
                    idx = self.basic_vars.index(var_name)
                    quantity = self.tableau[idx + 1][-1]
                    used += self.A[i][j] * quantity
            
            slack = available - used
            pct_used = (used / available * 100) if available > 0 else 0
            
            lines.append(f"{constraint_name:<25} | {used:>12.1f} | {available:>12.1f} | {slack:>12.1f} | {pct_used:>7.1f}%")
        
        return "\n".join(lines)


def run_simplex_method(problem_type="max"):
    """Main function to run simplex on CloudOptima LP problem"""
    output = []
    
    try:
        # Read Excel data
        df = pd.read_excel('CloudOptima_OR_Data.xlsx', sheet_name='Linear_Programming')
        
        output.append("="*90)
        output.append("☁️  CLOUDOPTIMA - LINEAR PROGRAMMING OPTIMIZATION")
        output.append("="*90)
        output.append(f"\n📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"🎯 Objective: MAXIMIZE Total Hourly Profit")
        output.append(f"📊 Problem Size: {len(df)} VM types, 10 infrastructure constraints")
        
        # Extract data (first 10 rows are VM types)
        vm_data = df.iloc[:10]
        
        output.append(f"\n📋 VM TYPES:")
        for idx, row in vm_data.iterrows():
            output.append(f"  • {row['VM_Type']}: ${row['Profit_per_Hour']}/hour (max {int(row['Max_Instances'])} instances)")
        
        # Objective coefficients (profit per hour)
        c = vm_data['Profit_per_Hour'].tolist()
        
        # Variable names
        var_names = vm_data['VM_Type'].tolist()
        
        # Constraint matrix (resource consumption)
        constraint_cols = [col for col in df.columns if col.startswith('Consumes_')]
        A = vm_data[constraint_cols].values.tolist()
        
        # RHS (resource limits from constraint rows)
        constraint_data = df.iloc[12:22]  # Rows after the gap
        b = constraint_data['Max_Instances'].tolist()
        
        # Constraint names
        constraint_names = [col.replace('Consumes_', '') for col in constraint_cols]
        
        output.append(f"\n🔧 CONSTRAINTS (Resource Limits):")
        for i, name in enumerate(constraint_names):
            output.append(f"  {i+1}. {name}: ≤ {b[i]:,.0f}")
        
        output.append(f"\n⏳ Running Simplex Algorithm...")
        output.append("="*90)
        
        # Create and solve
        solver = SimplexSolver(c, A, b, var_names, constraint_names)
        solution, z_value, iterations = solver.solve()
        
        if solution is None:
            output.append(f"❌ {z_value}")
            return "\n".join(output)
        
        # Show iterations (first 3 and last 2)
        output.append("\n📈 SIMPLEX ITERATIONS:")
        all_iterations = solver.iterations
        
        if len(all_iterations) <= 5:
            for iter_text in all_iterations:
                output.append(iter_text)
        else:
            # Show first 3
            for iter_text in all_iterations[:3]:
                output.append(iter_text)
            
            output.append(f"\n... {len(all_iterations) - 5} intermediate iterations omitted ...")
            
            # Show last 2
            for iter_text in all_iterations[-2:]:
                output.append(iter_text)
        
        output.append("\n" + "="*90)
        output.append("🎉 OPTIMAL SOLUTION FOUND!")
        output.append("="*90)
        
        output.append(f"\n💰 MAXIMUM HOURLY PROFIT: ${z_value:,.2f}")
        output.append(f"🔄 Total Iterations: {iterations}")
        
        # Display optimal allocation
        output.append(f"\n📊 OPTIMAL VM ALLOCATION:")
        output.append("-" * 70)
        output.append(f"{'VM Type':<20} | {'Instances':>12} | {'Profit/Hour':>12} | {'Total Profit':>15}")
        output.append("-" * 70)
        
        total_instances = 0
        total_profit = 0
        
        for i, vm_name in enumerate(var_names):
            instances = solution[vm_name]
            if instances > 0.01:  # Show only if allocated
                profit_per = c[i]
                vm_profit = instances * profit_per
                total_instances += instances
                total_profit += vm_profit
                
                output.append(f"{vm_name:<20} | {instances:>12.2f} | ${profit_per:>11.2f} | ${vm_profit:>14,.2f}")
        
        output.append("-" * 70)
        output.append(f"{'TOTAL':<20} | {total_instances:>12.2f} | {'':<12} | ${total_profit:>14,.2f}")
        
        # Sensitivity Analysis
        sensitivity_output = solver.sensitivity_analysis(solution, z_value)
        output.append(sensitivity_output)
        
        output.append(f"\n✅ Analysis Complete!")
        output.append("="*90)
        
    except Exception as e:
        import traceback
        output.append(f"\n❌ ERROR: {str(e)}")
        output.append(f"\nTraceback:\n{traceback.format_exc()}")
    
    return "\n".join(output)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(run_simplex_method("max"))
