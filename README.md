# ☁️ CloudOptima v1.0

**Interactive Operations Research Suite for Cloud Infrastructure Optimization**

CloudOptima is a comprehensive desktop application that solves three major Operations Research optimization problems with real-time visualization, sensitivity analysis, and step-by-step solutions for VM allocation, job scheduling, and data routing optimization.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Problem Types](#-problem-types)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Algorithms](#-algorithms)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 🎨 **Modern GUI Interface**
- Dark-themed, professional interface built with Tkinter
- Real-time solver execution with progress indicators
- Multi-threaded processing (non-blocking UI)
- Interactive dashboard with color-coded sections
- Live status updates and clock display

### 🔧 **Optimization Capabilities**
- **Linear Programming** - Simplex Method with sensitivity analysis
- **Assignment Problem** - Hungarian Algorithm implementation
- **Transportation Problem** - Multiple methods (Northwest Corner, Least Cost, VAM, MODI)
- Side-by-side method comparison
- Comprehensive sensitivity analysis

### 📊 **Data Management**
- Import/Export Excel data
- Generate PDF reports (planned)
- Pre-loaded realistic cloud computing datasets
- Custom data generation tools

### 🎓 **Educational Value**
- Step-by-step algorithm visualization
- Detailed iteration tracking
- Shadow prices and reduced costs
- Resource utilization analysis
- Binding constraint identification

---

## 🎯 Problem Types

### 1️⃣ **Linear Programming (Simplex Method)**
**Objective:** Maximize VM instance profit while respecting infrastructure constraints

**Problem Size:**
- 10 VM types (Basic, Micro, Small, Medium, Large, Memory, Compute, Storage, GPU, Metal)
- 10 resource constraints (CPU, RAM, SSD, HDD, Power, Cooling, Bandwidth, Rack Space, Licenses, IPs)

**Output:**
- Optimal VM allocation
- Maximum hourly profit
- Simplex tableau iterations
- Sensitivity analysis (shadow prices, reduced costs, resource utilization)

---

### 2️⃣ **Assignment Problem (Hungarian Algorithm)**
**Objective:** Optimal job-to-server node assignment

**Problem Size:**
- 10 jobs (DB, Video, ML, Logs, Crypto, Compile, Render, Traffic, Zip, Scan tasks)
- 10 server nodes (Node A through Node J)

**Output:**
- Optimal job assignments
- Minimum total processing time
- Step-by-step matrix reduction
- Algorithm iteration details

---

### 3️⃣ **Transportation Problem**
**Objective:** Minimize data transfer costs between data centers and storage vaults

**Problem Size:**
- 10 data centers (sources)
- 10 storage vaults (destinations)

**Methods:**
- Northwest Corner Method
- Least Cost Method
- Vogel's Approximation Method (VAM)
- MODI Method (optimality test)

**Output:**
- Allocation tables for each method
- Total transportation costs
- Method comparison
- Optimal routing strategy

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Libraries
```bash
pip install pandas numpy openpyxl
```

### Clone Repository
```bash
git clone https://github.com/muneeb-codehub/Operations_Research_Project.git
cd Operations_Research_Project
```

### Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Create requirements.txt with: pandas, numpy, openpyxl)*

---

## 💻 Usage

### Running the Application
```bash
python main_app2.py
```

### Quick Start Guide

1. **Launch Application**
   - Run `main_app2.py`
   - The GUI window will open with the dashboard

2. **Select Problem Type**
   - Click on any problem from the left sidebar:
     - 📈 Linear Programming
     - 🔀 Assignment Problem
     - 🚛 Transportation Problem

3. **Configure Options**
   - Choose objective (Maximize/Minimize)
   - Select method (for Transportation)

4. **Run Solver**
   - Click the "RUN" button
   - View real-time results in the output area

5. **Analyze Results**
   - Review optimal solutions
   - Check sensitivity analysis
   - Compare different methods

### Running Individual Modules
```bash
# Linear Programming
python simplex_method.py

# Assignment Problem
python assignment_problem.py

# Transportation Problem
python transportation_problem.py

# Sensitivity Analysis
python sensitivity_analysis.py

# Generate New Data
python generate_data.py
```

---

## 📁 Project Structure

```
Operations_Research_Project/
│
├── main_app2.py                    # Main GUI application
├── simplex_method.py                # Linear Programming solver
├── assignment_problem.py            # Assignment Problem solver
├── transportation_problem.py        # Transportation Problem solver
├── sensitivity_analysis.py          # Sensitivity analysis module
├── generate_data.py                 # Data generation utility
├── CloudOptima_OR_Data.xlsx         # Sample dataset
├── README.md                        # This file
│
├── .vscode/
│   └── settings.json                # VS Code settings
│
└── __pycache__/                     # Python cache files
```

---

## 🧮 Algorithms

### Simplex Method
- **Type:** Linear Programming
- **Complexity:** O(n³) worst case
- **Features:** Tableau method with pivot operations
- **Sensitivity:** Shadow prices, reduced costs, allowable ranges

### Hungarian Algorithm
- **Type:** Assignment Problem
- **Complexity:** O(n³)
- **Features:** Row/column reduction, optimal assignment finding
- **Fallback:** Greedy assignment if optimal not found

### Transportation Methods
- **Northwest Corner:** O(m+n) - Basic feasible solution
- **Least Cost:** O(mn) - Greedy cost-based allocation
- **VAM:** O(mn log(mn)) - Best initial solution
- **MODI:** O(mn) - Optimality verification

---

## 🔬 Technical Details

### Technologies Used
- **Language:** Python 3.8+
- **GUI Framework:** Tkinter
- **Data Processing:** Pandas, NumPy
- **Excel Integration:** OpenPyXL
- **Threading:** Python threading module

### Key Features Implementation
- **Multi-threading:** Prevents UI freezing during computation
- **Real-time Updates:** Dynamic status bar and progress indicators
- **Modular Design:** Separate solver modules for maintainability
- **Error Handling:** Comprehensive exception handling and user feedback

### Performance
- Handles 10x10 matrices efficiently
- Real-time solving (< 1 second for most problems)
- Scalable architecture for larger problems

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- [ ] Add more optimization algorithms
- [ ] Implement PDF report generation
- [ ] Add data visualization charts
- [ ] Expand to larger problem sizes
- [ ] Add unit tests
- [ ] Improve UI/UX

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Contact

**Muneeb Arif**

- GitHub: [@muneeb-codehub](https://github.com/muneeb-codehub)
- Email: muneebarif226@gmail.com

---

## Acknowledgments

- Operations Research course materials
- Cloud computing optimization research
- Python Tkinter community
- NumPy and Pandas documentation

---

## 📚 References

- Simplex Method: Dantzig, G. B. (1963)
- Hungarian Algorithm: Kuhn, H. W. (1955)
- Transportation Problem: Hitchcock, F. L. (1941)
- Vogel's Approximation Method: Reinfeld & Vogel (1958)

---

**⭐ If you find this project helpful, please consider giving it a star!**
