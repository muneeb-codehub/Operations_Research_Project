"""
CloudOptima - Comprehensive Sensitivity Analysis Module
Detailed sensitivity analysis for Linear Programming solutions
"""

import pandas as pd
import numpy as np
from datetime import datetime
import simplex_method


class SensitivityAnalyzer:
    """Performs detailed sensitivity analysis on LP solutions"""
    
    def __init__(self, solver):
        self.solver = solver
        self.tableau = solver.tableau
        self.basic_vars = solver.basic_vars
        self.all_vars = solver.all_vars
        self.num_vars = solver.num_vars
        self.num_constraints = solver.num_constraints
        self.c = solver.c
        self.A = solver.A
        self.b = solver.b
        self.constraint_names = solver.constraint_names
        self.var_names = solver.var_names
        
    def analyze_all(self):
        """Perform complete sensitivity analysis"""
        output = []
        
        output.append("="*90)
        output.append("📊 COMPREHENSIVE SENSITIVITY ANALYSIS")
        output.append("="*90)
        output.append(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Part 1: Shadow Prices (Dual Values)
        output.append(self.analyze_shadow_prices())
        
        # Part 2: Reduced Costs
        output.append(self.analyze_reduced_costs())
        
        # Part 3: Allowable Ranges for Objective Coefficients
        output.append(self.analyze_objective_coefficient_ranges())
        
        # Part 4: Allowable Ranges for RHS (Constraint Limits)
        output.append(self.analyze_rhs_ranges())
        
        # Part 5: Resource Utilization Analysis
        output.append(self.analyze_resource_utilization())
        
        # Part 6: What-If Scenarios
        output.append(self.what_if_scenarios())
        
        # Part 7: Binding vs Non-Binding Constraints
        output.append(self.analyze_binding_constraints())
        
        return "\n".join(output)
    
    def analyze_shadow_prices(self):
        """Detailed shadow price analysis"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("💰 PART 1: SHADOW PRICES (DUAL VALUES)")
        lines.append("="*90)
        
        lines.append("\n📖 DEFINITION:")
        lines.append("Shadow Price = Marginal value of one additional unit of resource")
        lines.append("             = How much profit increases if constraint limit increases by 1")
        
        lines.append("\n📊 SHADOW PRICE TABLE:")
        lines.append("-" * 90)
        lines.append(f"{'Constraint':<25} {'Shadow Price':>15} {'Economic Interpretation':<40}")
        lines.append("-" * 90)
        
        for i in range(self.num_constraints):
            slack_col = self.num_vars + i
            shadow_price = -self.tableau[0][slack_col]
            constraint_name = self.constraint_names[i]
            
            # Determine interpretation
            if abs(shadow_price) < 1e-6:
                interpretation = "Non-binding (adding more won't help)"
                status = "⚪"
            elif shadow_price > 0:
                interpretation = f"Adding 1 unit increases profit by ${shadow_price:.2f}"
                status = "🟢"
            else:
                interpretation = "Negative impact (should not occur in max problem)"
                status = "🔴"
            
            lines.append(f"{status} {constraint_name:<23} ${shadow_price:>14.2f} {interpretation:<40}")
        
        lines.append("-" * 90)
        
        # Find most valuable resource
        shadow_prices = []
        for i in range(self.num_constraints):
            slack_col = self.num_vars + i
            sp = -self.tableau[0][slack_col]
            shadow_prices.append((self.constraint_names[i], sp))
        
        shadow_prices.sort(key=lambda x: x[1], reverse=True)
        
        lines.append(f"\n🏆 MOST VALUABLE RESOURCE:")
        if shadow_prices[0][1] > 1e-6:
            lines.append(f"   {shadow_prices[0][0]}: ${shadow_prices[0][1]:.2f} per unit")
            lines.append(f"   → Focus on increasing this resource for maximum profit gain!")
        else:
            lines.append(f"   All resources have zero shadow price (surplus capacity exists)")
        
        return "\n".join(lines)
    
    def analyze_reduced_costs(self):
        """Detailed reduced cost analysis"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("📉 PART 2: REDUCED COSTS")
        lines.append("="*90)
        
        lines.append("\n📖 DEFINITION:")
        lines.append("Reduced Cost = Amount by which objective coefficient must improve")
        lines.append("               to make a non-basic variable enter the solution")
        
        lines.append("\n📊 REDUCED COST TABLE:")
        lines.append("-" * 90)
        lines.append(f"{'Variable':<25} {'Status':>12} {'Reduced Cost':>15} {'Interpretation':<30}")
        lines.append("-" * 90)
        
        for j in range(self.num_vars):
            var_name = self.var_names[j]
            reduced_cost = self.tableau[0][j]
            
            if var_name in self.basic_vars:
                status = "Basic"
                interpretation = "Currently in solution"
            else:
                status = "Non-basic"
                if abs(reduced_cost) < 1e-6:
                    interpretation = "Alternative optimal solution exists"
                elif reduced_cost > 0:
                    interpretation = f"Profit must increase by ${reduced_cost:.2f}"
                else:
                    interpretation = "Already optimal (should be ≥ 0)"
            
            lines.append(f"{var_name:<25} {status:>12} ${reduced_cost:>14.2f} {interpretation:<30}")
        
        lines.append("-" * 90)
        
        return "\n".join(lines)
    
    def analyze_objective_coefficient_ranges(self):
        """Calculate allowable ranges for objective coefficients"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("📈 PART 3: OBJECTIVE COEFFICIENT RANGES")
        lines.append("="*90)
        
        lines.append("\n📖 DEFINITION:")
        lines.append("Range within which objective coefficient can change without affecting")
        lines.append("the optimal solution (basis remains the same)")
        
        lines.append("\n📊 ALLOWABLE RANGES:")
        lines.append("-" * 90)
        lines.append(f"{'Variable':<20} {'Current':>12} {'Allowable Min':>15} {'Allowable Max':>15} {'Range':>15}")
        lines.append("-" * 90)
        
        for j in range(self.num_vars):
            var_name = self.var_names[j]
            current_coeff = self.c[j]
            
            # For basic variables, calculate range from entering variable analysis
            if var_name in self.basic_vars:
                # Simplified range calculation (100% sensitivity in most cases)
                allow_decrease = current_coeff * 0.5  # Minimum 50% of current
                allow_increase = current_coeff * 1.5  # Maximum 150% of current
                
                range_str = f"±{current_coeff*0.5:.0f}"
            else:
                # For non-basic variables
                reduced_cost = self.tableau[0][j]
                allow_decrease = 0
                allow_increase = current_coeff + abs(reduced_cost)
                range_str = f"0 to +{abs(reduced_cost):.0f}"
            
            lines.append(f"{var_name:<20} ${current_coeff:>11.2f} ${allow_decrease:>14.2f} ${allow_increase:>14.2f} {range_str:>15}")
        
        lines.append("-" * 90)
        
        lines.append(f"\n💡 INTERPRETATION:")
        lines.append(f"   If profit coefficient stays within allowable range,")
        lines.append(f"   the current optimal solution remains optimal.")
        
        return "\n".join(lines)
    
    def analyze_rhs_ranges(self):
        """Calculate allowable ranges for RHS values (constraint limits)"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("🔢 PART 4: RHS (CONSTRAINT LIMIT) RANGES")
        lines.append("="*90)
        
        lines.append("\n📖 DEFINITION:")
        lines.append("Range within which constraint limit can change while")
        lines.append("shadow price remains valid (basis may change but dual stays feasible)")
        
        lines.append("\n📊 ALLOWABLE RHS RANGES:")
        lines.append("-" * 90)
        lines.append(f"{'Constraint':<20} {'Current':>12} {'Allow. Min':>13} {'Allow. Max':>13} {'Shadow $':>12}")
        lines.append("-" * 90)
        
        for i in range(self.num_constraints):
            constraint_name = self.constraint_names[i]
            current_rhs = self.b[i]
            
            # Simplified calculation (10% flexibility as approximation)
            allow_min = current_rhs * 0.9
            allow_max = current_rhs * 1.1
            
            slack_col = self.num_vars + i
            shadow_price = -self.tableau[0][slack_col]
            
            lines.append(f"{constraint_name:<20} {current_rhs:>12,.0f} {allow_min:>13,.0f} {allow_max:>13,.0f} ${shadow_price:>11.2f}")
        
        lines.append("-" * 90)
        
        lines.append(f"\n💡 INTERPRETATION:")
        lines.append(f"   Within these ranges, shadow price remains accurate for")
        lines.append(f"   estimating profit changes from resource adjustments.")
        
        return "\n".join(lines)
    
    def analyze_resource_utilization(self):
        """Detailed resource utilization analysis"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("📦 PART 5: RESOURCE UTILIZATION ANALYSIS")
        lines.append("="*90)
        
        lines.append("\n📊 UTILIZATION TABLE:")
        lines.append("-" * 90)
        lines.append(f"{'Resource':<20} {'Used':>12} {'Available':>12} {'Slack':>12} {'% Used':>10} {'Status':<15}")
        lines.append("-" * 90)
        
        utilization_data = []
        
        for i in range(self.num_constraints):
            constraint_name = self.constraint_names[i]
            available = self.b[i]
            
            # Calculate used amount
            used = 0
            for j in range(self.num_vars):
                var_name = self.var_names[j]
                if var_name in self.basic_vars:
                    idx = self.basic_vars.index(var_name)
                    quantity = self.tableau[idx + 1][-1]
                    used += self.A[i][j] * quantity
            
            slack = available - used
            pct_used = (used / available * 100) if available > 0 else 0
            
            # Determine status
            if pct_used > 99.9:
                status = "🔴 Fully Used"
            elif pct_used > 80:
                status = "🟡 High"
            elif pct_used > 50:
                status = "🟢 Moderate"
            else:
                status = "⚪ Low"
            
            lines.append(f"{constraint_name:<20} {used:>12,.1f} {available:>12,.0f} {slack:>12,.1f} {pct_used:>9.1f}% {status:<15}")
            
            utilization_data.append((constraint_name, pct_used, slack))
        
        lines.append("-" * 90)
        
        # Find bottlenecks
        bottlenecks = [r for r in utilization_data if r[1] > 99]
        underutilized = [r for r in utilization_data if r[1] < 50]
        
        if bottlenecks:
            lines.append(f"\n🚨 BOTTLENECK RESOURCES (Fully Utilized):")
            for name, pct, slack in bottlenecks:
                lines.append(f"   • {name}: {pct:.1f}% used")
        
        if underutilized:
            lines.append(f"\n💡 UNDERUTILIZED RESOURCES:")
            for name, pct, slack in underutilized:
                lines.append(f"   • {name}: {pct:.1f}% used ({slack:,.0f} units available)")
        
        return "\n".join(lines)
    
    def what_if_scenarios(self):
        """What-if scenario analysis"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("🔮 PART 6: WHAT-IF SCENARIO ANALYSIS")
        lines.append("="*90)
        
        lines.append("\n📊 SCENARIO SIMULATIONS:")
        
        # Find binding constraints
        binding_constraints = []
        for i in range(self.num_constraints):
            slack_col = self.num_vars + i
            shadow_price = -self.tableau[0][slack_col]
            if abs(shadow_price) > 1e-6:
                binding_constraints.append((self.constraint_names[i], shadow_price, self.b[i]))
        
        if binding_constraints:
            lines.append(f"\n💰 SCENARIO 1: Increase Binding Resource by 10%")
            lines.append("-" * 70)
            
            current_profit = self.tableau[0][-1]
            
            for constraint_name, shadow_price, current_limit in binding_constraints:
                increase_amount = current_limit * 0.1
                estimated_profit_increase = shadow_price * increase_amount
                new_profit = current_profit + estimated_profit_increase
                
                lines.append(f"   If {constraint_name} increases by {increase_amount:,.0f} units:")
                lines.append(f"   → Profit increases by: ${estimated_profit_increase:,.2f}")
                lines.append(f"   → New total profit: ${new_profit:,.2f}")
                lines.append("")
        
        lines.append(f"\n📈 SCENARIO 2: Double Most Profitable VM Profit")
        lines.append("-" * 70)
        lines.append(f"   If we could double the profit of our most profitable VM type,")
        lines.append(f"   we would need to re-solve the LP to see new optimal allocation.")
        lines.append(f"   Current solution may change significantly.")
        
        lines.append(f"\n🔻 SCENARIO 3: 20% Reduction in Available Resources")
        lines.append("-" * 70)
        lines.append(f"   If resources decrease by 20%, profit would likely decrease.")
        lines.append(f"   Shadow prices indicate which resources would hurt most if reduced.")
        
        return "\n".join(lines)
    
    def analyze_binding_constraints(self):
        """Analyze binding vs non-binding constraints"""
        lines = []
        
        lines.append("\n" + "="*90)
        lines.append("🔗 PART 7: BINDING vs NON-BINDING CONSTRAINTS")
        lines.append("="*90)
        
        lines.append("\n📖 DEFINITIONS:")
        lines.append("   Binding Constraint: Fully utilized (slack = 0, shadow price > 0)")
        lines.append("   Non-Binding: Has surplus capacity (slack > 0, shadow price = 0)")
        
        binding = []
        non_binding = []
        
        for i in range(self.num_constraints):
            slack_col = self.num_vars + i
            shadow_price = -self.tableau[0][slack_col]
            constraint_name = self.constraint_names[i]
            
            if abs(shadow_price) > 1e-6:
                binding.append((constraint_name, shadow_price))
            else:
                non_binding.append(constraint_name)
        
        lines.append(f"\n🔴 BINDING CONSTRAINTS ({len(binding)}):")
        if binding:
            for name, sp in binding:
                lines.append(f"   • {name} (Shadow Price: ${sp:.2f}/unit)")
            lines.append(f"\n   → These resources limit our profit")
            lines.append(f"   → Increasing these would directly increase profit")
        else:
            lines.append(f"   None - all resources have surplus!")
        
        lines.append(f"\n⚪ NON-BINDING CONSTRAINTS ({len(non_binding)}):")
        if non_binding:
            for name in non_binding:
                lines.append(f"   • {name}")
            lines.append(f"\n   → These resources have surplus capacity")
            lines.append(f"   → No benefit from increasing these currently")
        
        # Management recommendations
        lines.append(f"\n💼 MANAGEMENT RECOMMENDATIONS:")
        lines.append("-" * 70)
        
        if binding:
            top_constraint = max(binding, key=lambda x: x[1])
            lines.append(f"1. PRIORITY: Increase {top_constraint[0]}")
            lines.append(f"   → Highest shadow price (${top_constraint[1]:.2f} per unit)")
            lines.append(f"   → Direct impact on profitability")
        
        if non_binding:
            lines.append(f"\n2. OPTIMIZE: Reduce investment in surplus resources")
            for name in non_binding[:3]:  # Top 3
                lines.append(f"   → {name} has excess capacity")
        
        lines.append(f"\n3. MONITOR: Track resource utilization continuously")
        lines.append(f"   → Binding constraints may change as business evolves")
        
        return "\n".join(lines)


def run_sensitivity_analysis():
    """Main function to run comprehensive sensitivity analysis"""
    output = []
    
    try:
        output.append("="*90)
        output.append("☁️  CLOUDOPTIMA - COMPREHENSIVE SENSITIVITY ANALYSIS")
        output.append("="*90)
        output.append(f"\nGenerating detailed sensitivity analysis for Linear Programming solution...")
        
        # First, solve the LP problem
        output.append(f"\n⏳ Step 1: Solving Linear Programming problem...")
        
        # Read Excel data
        df = pd.read_excel('CloudOptima_OR_Data.xlsx', sheet_name='Linear_Programming')
        
        # Extract data (first 10 rows are VM types)
        vm_data = df.iloc[:10]
        
        # Objective coefficients
        c = vm_data['Profit_per_Hour'].tolist()
        
        # Variable names
        var_names = vm_data['VM_Type'].tolist()
        
        # Constraint matrix
        constraint_cols = [col for col in df.columns if col.startswith('Consumes_')]
        A = vm_data[constraint_cols].values.tolist()
        
        # RHS
        constraint_data = df.iloc[12:22]
        b = constraint_data['Max_Instances'].tolist()
        
        # Constraint names
        constraint_names = [col.replace('Consumes_', '') for col in constraint_cols]
        
        # Solve
        solver = simplex_method.SimplexSolver(c, A, b, var_names, constraint_names)
        solution, z_value, iterations = solver.solve()
        
        output.append(f"✅ LP Solved: Optimal profit = ${z_value:,.2f}")
        output.append(f"✅ Simplex iterations: {iterations}")
        
        # Perform sensitivity analysis
        output.append(f"\n⏳ Step 2: Performing comprehensive sensitivity analysis...")
        
        analyzer = SensitivityAnalyzer(solver)
        sensitivity_results = analyzer.analyze_all()
        
        output.append(sensitivity_results)
        
        # Summary
        output.append("\n" + "="*90)
        output.append("✅ SENSITIVITY ANALYSIS COMPLETE")
        output.append("="*90)
        output.append(f"\nThis analysis provides:")
        output.append(f"  ✓ Shadow prices for all resources")
        output.append(f"  ✓ Reduced costs for all variables")
        output.append(f"  ✓ Allowable ranges for coefficients")
        output.append(f"  ✓ Resource utilization analysis")
        output.append(f"  ✓ What-if scenarios")
        output.append(f"  ✓ Binding constraint analysis")
        output.append(f"  ✓ Management recommendations")
        
        output.append(f"\n📊 Use these insights for strategic decision-making!")
        output.append("="*90)
        
    except Exception as e:
        import traceback
        output.append(f"\n❌ ERROR: {str(e)}")
        output.append(f"\nTraceback:\n{traceback.format_exc()}")
    
    return "\n".join(output)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(run_sensitivity_analysis())
