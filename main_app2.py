"""
CloudOptima v1.0 - Alternative Modern GUI
Interactive Real-Time Solver with Live Visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import threading
import time


class ModernCloudOptimaApp:
    """Alternative modern GUI with different functionality approach"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CloudOptima v1.0 - Interactive OR Suite")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0a0e27')
        
        # Modern styling
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_card': '#1a1f3a',
            'accent_blue': '#00d4ff',
            'accent_purple': '#b24bf3',
            'accent_green': '#00ff88',
            'accent_orange': '#ff9500',
            'text_primary': '#ffffff',
            'text_secondary': '#8b92b8',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }
        
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()
        self.create_modern_ui()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = 1600
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askokcancel("Exit", "Exit CloudOptima v1.0?"):
            self.root.destroy()
    
    def create_modern_ui(self):
        """Create alternative modern UI layout"""
        
        # Top Navigation Bar
        self.create_top_navbar()
        
        # Main Container with Sidebar
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True)
        
        # Left Sidebar - Problem Selector
        self.create_sidebar(main_container)
        
        # Right Content Area
        self.content_area = tk.Frame(main_container, bg=self.colors['bg_dark'])
        self.content_area.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Bottom Status Bar (create before showing dashboard)
        self.create_status_bar()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_top_navbar(self):
        """Create modern top navigation bar"""
        navbar = tk.Frame(self.root, bg='#13172e', height=70)
        navbar.pack(fill='x', side='top')
        navbar.pack_propagate(False)
        
        # Logo Section
        logo_frame = tk.Frame(navbar, bg='#13172e')
        logo_frame.pack(side='left', padx=30, pady=15)
        
        tk.Label(logo_frame, text="⚡", font=('Segoe UI Emoji', 28), 
                bg='#13172e', fg=self.colors['accent_blue']).pack(side='left')
        
        tk.Label(logo_frame, text="CLOUDOPTIMA", font=('Arial Black', 16, 'bold'),
                bg='#13172e', fg='white').pack(side='left', padx=10)
        
        tk.Label(logo_frame, text="v2.0", font=('Arial', 10),
                bg='#13172e', fg=self.colors['text_secondary']).pack(side='left')
        
        # Action Buttons
        btn_frame = tk.Frame(navbar, bg='#13172e')
        btn_frame.pack(side='right', padx=30)
        
        # Quick Action Buttons
        actions = [
            ("📊 Run All", self.run_all_solvers, self.colors['accent_green']),
            ("💾 Export Results", self.export_results, self.colors['accent_purple']),
            ("⚙️ Settings", self.show_settings, self.colors['text_secondary'])
        ]
        
        for text, command, color in actions:
            btn = tk.Button(btn_frame, text=text, command=command,
                          bg=color, fg='white', font=('Arial', 9, 'bold'),
                          relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
            btn.pack(side='left', padx=5)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg=self.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
    
    def create_sidebar(self, parent):
        """Create left sidebar with problem selector"""
        sidebar = tk.Frame(parent, bg=self.colors['bg_card'], width=280)
        sidebar.pack(side='left', fill='y', padx=(20,0), pady=20)
        sidebar.pack_propagate(False)
        
        # Sidebar Header
        tk.Label(sidebar, text="PROBLEMS", font=('Arial', 12, 'bold'),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=(20,10), padx=20, anchor='w')
        
        # Problem Menu Items
        self.menu_items = [
            ("🏠", "Dashboard", "Overview", self.show_dashboard, self.colors['accent_blue']),
            ("📈", "Linear Programming", "Simplex Method", self.show_lp_solver, self.colors['accent_green']),
            ("🔀", "Assignment Problem", "Hungarian Algorithm", self.show_assignment_solver, self.colors['accent_purple']),
            ("🚛", "Transportation", "Transportation Methods", self.show_transportation_solver, self.colors['accent_orange']),
            ("📊", "Compare Results", "Side by Side", self.show_comparison, self.colors['accent_blue']),
            ("📁", "Data Manager", "Import/Export", self.show_data_manager, self.colors['text_secondary'])
        ]
        
        for icon, title, subtitle, command, color in self.menu_items:
            self.create_menu_item(sidebar, icon, title, subtitle, command, color)
    
    def create_menu_item(self, parent, icon, title, subtitle, command, color):
        """Create animated menu item"""
        item_frame = tk.Frame(parent, bg=self.colors['bg_card'], cursor='hand2')
        item_frame.pack(fill='x', padx=10, pady=5)
        
        # Content frame
        content = tk.Frame(item_frame, bg=self.colors['bg_card'])
        content.pack(fill='both', expand=True, padx=15, pady=12)
        
        # Icon
        tk.Label(content, text=icon, font=('Segoe UI Emoji', 20),
                bg=self.colors['bg_card'], fg=color).pack(side='left', padx=(0,10))
        
        # Text container
        text_frame = tk.Frame(content, bg=self.colors['bg_card'])
        text_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(text_frame, text=title, font=('Arial', 10, 'bold'),
                bg=self.colors['bg_card'], fg='white', anchor='w').pack(fill='x')
        
        tk.Label(text_frame, text=subtitle, font=('Arial', 8),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary'], anchor='w').pack(fill='x')
        
        # Hover effects
        def on_enter(e):
            item_frame.configure(bg=self.colors['bg_dark'])
            content.configure(bg=self.colors['bg_dark'])
            text_frame.configure(bg=self.colors['bg_dark'])
            for child in text_frame.winfo_children():
                child.configure(bg=self.colors['bg_dark'])
            for child in content.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=self.colors['bg_dark'])
        
        def on_leave(e):
            item_frame.configure(bg=self.colors['bg_card'])
            content.configure(bg=self.colors['bg_card'])
            text_frame.configure(bg=self.colors['bg_card'])
            for child in text_frame.winfo_children():
                child.configure(bg=self.colors['bg_card'])
            for child in content.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=self.colors['bg_card'])
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        item_frame.bind("<Button-1>", lambda e: command())
        
        for widget in [content, text_frame] + list(content.winfo_children()) + list(text_frame.winfo_children()):
            widget.bind("<Button-1>", lambda e: command())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def create_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.root, bg='#13172e', height=40)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="● Ready",
                                     font=('Consolas', 9), bg='#13172e',
                                     fg=self.colors['accent_green'], anchor='w')
        self.status_label.pack(side='left', padx=20, fill='both', expand=True)
        
        # Time
        self.time_label = tk.Label(status_frame, text="",
                                   font=('Consolas', 9), bg='#13172e',
                                   fg=self.colors['text_secondary'])
        self.time_label.pack(side='right', padx=20)
        self.update_clock()
    
    def update_clock(self):
        """Update clock in status bar"""
        current_time = datetime.now().strftime('%I:%M:%S %p | %B %d, %Y')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show interactive dashboard"""
        self.clear_content()
        self.update_status("Dashboard", self.colors['accent_blue'])
        
        # Welcome Section
        welcome = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        welcome.pack(fill='x', pady=(0,20))
        
        tk.Label(welcome, text="🎯 Welcome to CloudOptima v1.0",
                font=('Arial', 24, 'bold'), bg=self.colors['bg_card'],
                fg='white').pack(padx=30, pady=(30,10), anchor='w')
        
        tk.Label(welcome, text="Interactive Operations Research Suite for Cloud Infrastructure Optimization",
                font=('Arial', 11), bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(padx=30, pady=(0,30), anchor='w')
        
        # Stats Cards
        stats_container = tk.Frame(self.content_area, bg=self.colors['bg_dark'])
        stats_container.pack(fill='both', expand=True)
        
        stats = [
            ("📈", "Linear Programming", "Simplex Algorithm", self.colors['accent_green']),
            ("🔀", "Assignment Problem", "Hungarian Method", self.colors['accent_purple']),
            ("🚛", "Transportation", "Transportation Methods", self.colors['accent_orange'])
        ]
        
        for i, (icon, title, method, color) in enumerate(stats):
            row = i // 3
            col = i % 3
            
            card = tk.Frame(stats_container, bg=self.colors['bg_card'])
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Configure grid weights
            stats_container.grid_rowconfigure(row, weight=1)
            stats_container.grid_columnconfigure(col, weight=1)
            
            # Icon header
            header = tk.Frame(card, bg=color, height=80)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(header, text=icon, font=('Segoe UI Emoji', 40),
                    bg=color).pack(expand=True)
            
            # Content
            content = tk.Frame(card, bg=self.colors['bg_card'])
            content.pack(fill='both', expand=True, padx=20, pady=20)
            
            tk.Label(content, text=title, font=('Arial', 14, 'bold'),
                    bg=self.colors['bg_card'], fg='white').pack(anchor='w')
            
            tk.Label(content, text=method, font=('Arial', 9),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(5,15))
    
    def show_lp_solver(self):
        """Show Linear Programming solver with interactive controls"""
        self.clear_content()
        self.update_status("Linear Programming Solver", self.colors['accent_green'])
        
        # Header
        header = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        header.pack(fill='x', pady=(0,20))
        
        tk.Label(header, text="📈 Linear Programming Solver",
                font=('Arial', 20, 'bold'), bg=self.colors['bg_card'],
                fg='white').pack(padx=30, pady=(20,5), anchor='w')
        
        tk.Label(header, text="Simplex Algorithm | Maximize VM Instance Profit",
                font=('Arial', 10), bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(padx=30, pady=(0,20), anchor='w')
        
        # Control Panel
        control_panel = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        control_panel.pack(fill='x', pady=(0,20))
        
        controls = tk.Frame(control_panel, bg=self.colors['bg_card'])
        controls.pack(padx=30, pady=20)
        
        # Objective selector
        tk.Label(controls, text="Objective:", font=('Arial', 10, 'bold'),
                bg=self.colors['bg_card'], fg='white').grid(row=0, column=0, padx=(0,10), pady=10, sticky='w')
        
        self.lp_objective = tk.StringVar(value="maximize")
        tk.Radiobutton(controls, text="Maximize Profit", variable=self.lp_objective, value="maximize",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=1, padx=5)
        
        tk.Radiobutton(controls, text="Minimize Cost", variable=self.lp_objective, value="minimize",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=2, padx=5)
        
        # Run button with loading animation
        tk.Button(controls, text="🚀 RUN SIMPLEX ALGORITHM", command=self.run_lp_solver,
                 bg=self.colors['accent_green'], fg='white', font=('Arial', 11, 'bold'),
                 padx=30, pady=12, relief=tk.FLAT, cursor='hand2').grid(row=0, column=3, padx=20)
        
        # Results Area with tabs
        results_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        results_frame.pack(fill='both', expand=True)
        
        # Create notebook for results
        style = ttk.Style()
        style.configure('Modern.TNotebook', background=self.colors['bg_card'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab', background=self.colors['bg_dark'], 
                       foreground='white', padding=[20, 10], font=('Arial', 9, 'bold'))
        style.map('Modern.TNotebook.Tab', background=[('selected', self.colors['accent_green'])],
                 foreground=[('selected', 'white')])
        
        notebook = ttk.Notebook(results_frame, style='Modern.TNotebook')
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Output tab
        output_tab = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(output_tab, text='📊 Solution Output')
        
        self.lp_output = tk.Text(output_tab, wrap=tk.WORD, font=('Consolas', 9),
                                bg='#0d1117', fg='#c9d1d9', relief=tk.FLAT,
                                padx=20, pady=20)
        self.lp_output.pack(fill='both', expand=True, padx=10, pady=10)
        self.lp_output.insert('1.0', "Click 'RUN SIMPLEX ALGORITHM' to solve the Linear Programming problem...\n\n")
        
        # Visualization tab
        viz_tab = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(viz_tab, text='📈 Visualization')
        
        tk.Label(viz_tab, text="🎨 Graphical visualization coming soon...",
                font=('Arial', 12), bg=self.colors['bg_dark'],
                fg=self.colors['text_secondary']).pack(expand=True)
    
    def show_assignment_solver(self):
        """Show Assignment Problem solver"""
        self.clear_content()
        self.update_status("Assignment Problem Solver", self.colors['accent_purple'])
        
        # Header
        header = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        header.pack(fill='x', pady=(0,20))
        
        tk.Label(header, text="🔀 Assignment Problem Solver",
                font=('Arial', 20, 'bold'), bg=self.colors['bg_card'],
                fg='white').pack(padx=30, pady=(20,5), anchor='w')
        
        tk.Label(header, text="Hungarian Algorithm | Optimal Job-to-Node Matching",
                font=('Arial', 10), bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(padx=30, pady=(0,20), anchor='w')
        
        # Control Panel
        control_panel = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        control_panel.pack(fill='x', pady=(0,20))
        
        controls = tk.Frame(control_panel, bg=self.colors['bg_card'])
        controls.pack(padx=30, pady=20)
        
        tk.Label(controls, text="Problem Type:", font=('Arial', 10, 'bold'),
                bg=self.colors['bg_card'], fg='white').grid(row=0, column=0, padx=(0,10), pady=10, sticky='w')
        
        self.assign_type = tk.StringVar(value="minimize")
        tk.Radiobutton(controls, text="Minimize Time", variable=self.assign_type, value="minimize",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=1, padx=5)
        
        tk.Radiobutton(controls, text="Maximize Efficiency", variable=self.assign_type, value="maximize",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=2, padx=5)
        
        tk.Button(controls, text="🚀 RUN HUNGARIAN ALGORITHM", command=self.run_assignment_solver,
                 bg=self.colors['accent_purple'], fg='white', font=('Arial', 11, 'bold'),
                 padx=30, pady=12, relief=tk.FLAT, cursor='hand2').grid(row=0, column=3, padx=20)
        
        # Results Area
        results_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        results_frame.pack(fill='both', expand=True)
        
        self.assignment_output = tk.Text(results_frame, wrap=tk.WORD, font=('Consolas', 9),
                                        bg='#0d1117', fg='#c9d1d9', relief=tk.FLAT,
                                        padx=20, pady=20)
        self.assignment_output.pack(fill='both', expand=True, padx=20, pady=20)
        self.assignment_output.insert('1.0', "Click 'RUN HUNGARIAN ALGORITHM' to solve the Assignment problem...\n\n")
    
    def show_transportation_solver(self):
        """Show Transportation Problem solver"""
        self.clear_content()
        self.update_status("Transportation Problem Solver", self.colors['accent_orange'])
        
        # Header
        header = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        header.pack(fill='x', pady=(0,20))
        
        tk.Label(header, text="🚛 Transportation Problem Solver",
                font=('Arial', 20, 'bold'), bg=self.colors['bg_card'],
                fg='white').pack(padx=30, pady=(20,5), anchor='w')
        
        tk.Label(header, text="Transportation Methods | Minimize Shipping Cost",
                font=('Arial', 10), bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(padx=30, pady=(0,20), anchor='w')
        
        # Control Panel with method selection
        control_panel = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        control_panel.pack(fill='x', pady=(0,20))
        
        controls = tk.Frame(control_panel, bg=self.colors['bg_card'])
        controls.pack(padx=30, pady=20)
        
        tk.Label(controls, text="Initial Method:", font=('Arial', 10, 'bold'),
                bg=self.colors['bg_card'], fg='white').grid(row=0, column=0, padx=(0,10), pady=10, sticky='w')
        
        self.transport_method = tk.StringVar(value="all")
        tk.Radiobutton(controls, text="Northwest Corner", variable=self.transport_method, value="northwest",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=1, padx=5)
        
        tk.Radiobutton(controls, text="Least Cost", variable=self.transport_method, value="leastcost",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=2, padx=5)
        
        tk.Radiobutton(controls, text="VAM", variable=self.transport_method, value="vam",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=3, padx=5)
        
        tk.Radiobutton(controls, text="Compare All", variable=self.transport_method, value="all",
                      bg=self.colors['bg_card'], fg='white', selectcolor=self.colors['bg_dark'],
                      font=('Arial', 9), activebackground=self.colors['bg_card']).grid(row=0, column=4, padx=5)
        
        tk.Button(controls, text="🚀 SOLVE TRANSPORTATION", command=self.run_transportation_solver,
                 bg=self.colors['accent_orange'], fg='white', font=('Arial', 11, 'bold'),
                 padx=30, pady=12, relief=tk.FLAT, cursor='hand2').grid(row=0, column=5, padx=20)
        
        # Results Area
        results_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        results_frame.pack(fill='both', expand=True)
        
        self.transport_output = tk.Text(results_frame, wrap=tk.WORD, font=('Consolas', 9),
                                       bg='#0d1117', fg='#c9d1d9', relief=tk.FLAT,
                                       padx=20, pady=20)
        self.transport_output.pack(fill='both', expand=True, padx=20, pady=20)
        self.transport_output.insert('1.0', "Click 'SOLVE TRANSPORTATION' to find optimal routing...\n\n")
    
    def show_comparison(self):
        """Show side-by-side comparison of all methods"""
        self.clear_content()
        self.update_status("Results Comparison", self.colors['accent_blue'])
        
        tk.Label(self.content_area, text="📊 Compare All Results Side-by-Side",
                font=('Arial', 20, 'bold'), bg=self.colors['bg_dark'],
                fg='white').pack(pady=30)
        
        tk.Label(self.content_area, text="Run all solvers first to enable comparison",
                font=('Arial', 12), bg=self.colors['bg_dark'],
                fg=self.colors['text_secondary']).pack()
        
        tk.Button(self.content_area, text="🚀 RUN ALL SOLVERS NOW",
                 command=self.run_all_solvers,
                 bg=self.colors['accent_green'], fg='white',
                 font=('Arial', 12, 'bold'), padx=40, pady=15,
                 relief=tk.FLAT, cursor='hand2').pack(pady=30)
    
    def show_data_manager(self):
        """Show data import/export manager"""
        self.clear_content()
        self.update_status("Data Manager", self.colors['text_secondary'])
        
        tk.Label(self.content_area, text="📁 Data Manager",
                font=('Arial', 20, 'bold'), bg=self.colors['bg_dark'],
                fg='white').pack(pady=30)
        
        actions = tk.Frame(self.content_area, bg=self.colors['bg_dark'])
        actions.pack(pady=20)
        
        tk.Button(actions, text="📥 Import Data (Excel)",
                 command=self.import_data,
                 bg=self.colors['accent_blue'], fg='white',
                 font=('Arial', 11, 'bold'), padx=30, pady=15,
                 relief=tk.FLAT, cursor='hand2').pack(pady=10)
        
        tk.Button(actions, text="💾 Export Results (Excel)",
                 command=self.export_results,
                 bg=self.colors['accent_purple'], fg='white',
                 font=('Arial', 11, 'bold'), padx=30, pady=15,
                 relief=tk.FLAT, cursor='hand2').pack(pady=10)
        
        tk.Button(actions, text="📄 Generate PDF Report",
                 command=self.generate_pdf,
                 bg=self.colors['accent_orange'], fg='white',
                 font=('Arial', 11, 'bold'), padx=30, pady=15,
                 relief=tk.FLAT, cursor='hand2').pack(pady=10)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("500x600")
        settings_window.configure(bg=self.colors['bg_card'])
        
        # Center window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - 250
        y = (settings_window.winfo_screenheight() // 2) - 300
        settings_window.geometry(f'500x600+{x}+{y}')
        
        tk.Label(settings_window, text="⚙️ Application Settings",
                font=('Arial', 16, 'bold'), bg=self.colors['bg_card'],
                fg='white').pack(pady=20)
        
        # Settings options
        settings_frame = tk.Frame(settings_window, bg=self.colors['bg_card'])
        settings_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        options = [
            "🎨 Theme: Dark Mode",
            "🔢 Decimal Precision: 2",
            "⚡ Solver Speed: Fast",
            "📊 Show Visualizations: Enabled",
            "💾 Auto-save Results: Enabled",
            "🔔 Notifications: Enabled"
        ]
        
        for option in options:
            tk.Label(settings_frame, text=option, font=('Arial', 11),
                    bg=self.colors['bg_card'], fg='white',
                    anchor='w').pack(fill='x', pady=10)
    
    def run_lp_solver(self):
        """Run LP solver in background thread"""
        self.update_status("Running Linear Programming...", self.colors['warning'])
        
        def solver_thread():
            try:
                self.lp_output.delete('1.0', tk.END)
                self.lp_output.insert('1.0', "⏳ Executing Simplex Algorithm...\n\n")
                self.root.update()
                
                import simplex_method
                result = simplex_method.run_simplex_method(self.lp_objective.get()[:3])
                
                self.lp_output.delete('1.0', tk.END)
                self.lp_output.insert('1.0', result)
                
                self.update_status("Linear Programming completed ✓", self.colors['success'])
                messagebox.showinfo("Success", "Linear Programming solved successfully!")
                
            except Exception as e:
                self.lp_output.insert(tk.END, f"\n\n❌ ERROR: {str(e)}")
                self.update_status(f"Error: {str(e)}", self.colors['error'])
                messagebox.showerror("Error", f"Solver failed:\n{str(e)}")
        
        threading.Thread(target=solver_thread, daemon=True).start()
    
    def run_assignment_solver(self):
        """Run Assignment solver"""
        self.update_status("Running Assignment Problem...", self.colors['warning'])
        
        def solver_thread():
            try:
                self.assignment_output.delete('1.0', tk.END)
                self.assignment_output.insert('1.0', "⏳ Executing Hungarian Algorithm...\n\n")
                self.root.update()
                
                import assignment_problem
                result = assignment_problem.run_assignment_problem(minimize=(self.assign_type.get()=="minimize"))
                
                self.assignment_output.delete('1.0', tk.END)
                self.assignment_output.insert('1.0', result)
                
                self.update_status("Assignment Problem completed ✓", self.colors['success'])
                messagebox.showinfo("Success", "Assignment Problem solved successfully!")
                
            except Exception as e:
                self.assignment_output.insert(tk.END, f"\n\n❌ ERROR: {str(e)}")
                self.update_status(f"Error: {str(e)}", self.colors['error'])
                messagebox.showerror("Error", f"Solver failed:\n{str(e)}")
        
        threading.Thread(target=solver_thread, daemon=True).start()
    
    def run_transportation_solver(self):
        """Run Transportation solver"""
        self.update_status("Running Transportation Problem...", self.colors['warning'])
        
        def solver_thread():
            try:
                self.transport_output.delete('1.0', tk.END)
                self.transport_output.insert('1.0', "⏳ Executing Transportation Methods...\n\n")
                self.root.update()
                
                import transportation_problem
                result = transportation_problem.run_transportation_problem()
                
                self.transport_output.delete('1.0', tk.END)
                self.transport_output.insert('1.0', result)
                
                self.update_status("Transportation Problem completed ✓", self.colors['success'])
                messagebox.showinfo("Success", "Transportation Problem solved successfully!")
                
            except Exception as e:
                self.transport_output.insert(tk.END, f"\n\n❌ ERROR: {str(e)}")
                self.update_status(f"Error: {str(e)}", self.colors['error'])
                messagebox.showerror("Error", f"Solver failed:\n{str(e)}")
        
        threading.Thread(target=solver_thread, daemon=True).start()
    
    def run_all_solvers(self):
        """Run all three solvers sequentially"""
        self.update_status("Running all solvers...", self.colors['warning'])
        
        def run_all():
            try:
                # Show LP tab and run
                self.show_lp_solver()
                time.sleep(0.5)
                self.run_lp_solver()
                time.sleep(3)
                
                # Show Assignment tab and run
                self.show_assignment_solver()
                time.sleep(0.5)
                self.run_assignment_solver()
                time.sleep(3)
                
                # Show Transportation tab and run
                self.show_transportation_solver()
                time.sleep(0.5)
                self.run_transportation_solver()
                
                self.update_status("All solvers completed ✓", self.colors['success'])
                messagebox.showinfo("Complete", "All optimization problems solved successfully!")
                
            except Exception as e:
                self.update_status(f"Error in batch run: {str(e)}", self.colors['error'])
                messagebox.showerror("Error", f"Batch execution failed:\n{str(e)}")
        
        threading.Thread(target=run_all, daemon=True).start()
    
    def import_data(self):
        """Import data from Excel"""
        filename = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            messagebox.showinfo("Import", f"Data would be imported from:\n{filename}")
            self.update_status(f"Imported: {filename}", self.colors['success'])
    
    def export_results(self):
        """Export results to Excel"""
        filename = filedialog.asksaveasfilename(
            title="Save results as",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            messagebox.showinfo("Export", f"Results would be exported to:\n{filename}")
            self.update_status(f"Exported: {filename}", self.colors['success'])
    
    def generate_pdf(self):
        """Generate PDF report"""
        filename = filedialog.asksaveasfilename(
            title="Save PDF report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            messagebox.showinfo("PDF", f"PDF report would be generated:\n{filename}")
            self.update_status(f"PDF generated: {filename}", self.colors['success'])
    
    def update_status(self, message, color=None):
        """Update status bar"""
        if color is None:
            color = self.colors['accent_blue']
        self.status_label.config(text=f"● {message}", fg=color)
        self.root.update()
    
    def darken_color(self, hex_color):
        """Darken a hex color by 20%"""
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.7)) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernCloudOptimaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
