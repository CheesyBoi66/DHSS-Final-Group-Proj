import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import csv

# Global variables
burg = None
rect = None
boot = None
tree_frame = None
tree = None
movie_list = []
rating_sources = {
    "Rotten Tomatoes Critics": "RT_C",
    "Rotten Tomatoes Audience": "RT_A",
    "MetaCritics Critics": "MC_C",
    "MetaCritics Audience": "MC_A",
    "IMDb": "DB",
    "Gross Box Office": "gross",
    "Average Critic Score": "AV_C",
    "Average Audience Score": "AV_A",
    "Average Difference": "AV_DIFF",
    "Average Overall": "AV_OVR",
    "Year": "year"
}

# Global flags
menu_frame = None
is_menu_open = False
mainWin = None
mainCanv = None
rating_source_combobox = None

def load_movie_data(csv_file):
    """Load movie data from a CSV file into a list of dictionaries."""
    movie_list = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = {key: value for key, value in row.items()}
            movie_list.append(movie)
    return movie_list

def display_movie_list(movie_list, selected_rating_source):
    """Display the movie list in a Treeview."""
    global tree

    # Clear existing Treeview if it exists
    for item in tree.get_children():
        tree.delete(item)

    # Sort movies by year
    movie_list.sort(key=lambda x: x['year'])

    current_year = None
    for movie in movie_list:
        if movie['year'] != current_year:
            current_year = movie['year']
            tree.insert("", "end", values=(f"--- {current_year} ---", ""), tags=("year",))
        rating = movie.get(selected_rating_source, "N/A")
        tree.insert("", "end", values=(movie['name'], rating))

    # Add styling for year separators
    tree.tag_configure("year", font=("Impact", 14, "bold"), foreground="blue")

def update_padding(event=None):
    """Update padding for the Treeview frame dynamically based on window size."""
    if tree_frame:
        window_width = mainWin.winfo_width()
        padx_value = window_width // 10  # Adjust as needed
        tree_frame.grid_configure(padx=padx_value)

def update_movie_list(event):
    """Update the movie list based on the selected rating source."""
    selected_display_name = rating_source_combobox.get()
    selected_rating_source = rating_sources.get(selected_display_name)
    if selected_rating_source:
        display_movie_list(movie_list, selected_rating_source)

def toggle_menu():
    """Toggles the visibility of the side menu."""
    global menu_frame, is_menu_open

    if not is_menu_open:
        # Create the menu frame
        menu_frame = tk.Frame(mainWin, bg="gray", width=200)
        menu_frame.place(
            x=mainWin.winfo_width(),  # Start off-screen to the right
            y=50,  # Below the orange bar
            height=mainWin.winfo_height() - 50,  # Stretch dynamically excluding the orange bar
            width=200  # Fixed width for the menu
        )
        
        # Slide the menu into view
        slide_menu_in()
        is_menu_open = True
    else:
        slide_menu_out()
        is_menu_open = False

def slide_menu_in():
    """Animates the menu sliding in from the right."""
    current_x = menu_frame.winfo_x() + 200
    window_width = mainWin.winfo_width()
    
    # Slide the menu in if it is off-screen
    if current_x > window_width - 200:
        new_x = current_x - 20
        menu_frame.place(x=new_x, y=50)
        mainWin.after(10, slide_menu_in)

def slide_menu_out():
    """Animates the menu sliding out to the right."""
    current_x = menu_frame.winfo_x()
    window_width = mainWin.winfo_width()

    # Slide the menu out until it's off-screen
    if current_x < window_width:
        new_x = current_x + 20
        menu_frame.place(x=new_x, y=50)
        mainWin.after(10, slide_menu_out)

def update_menu_height(event=None):
    """Update the menu height dynamically when the window is resized."""
    if is_menu_open:
        menu_frame.place(
            x=menu_frame.winfo_x(),
            y=50,
            height=mainWin.winfo_height() - 50,  # Exclude orange bar
            width=200
        )

def makeMainWidg():
    """Create the hamburger button for the menu."""
    global burg
    # Load and resize the image using Pillow
    original_image = Image.open("burger.png")  # Open the image
    resized_image = original_image.resize((50, 50))  # Resize to 50x50 pixels

    # Convert the resized image to a PhotoImage
    burg = ImageTk.PhotoImage(resized_image)

    # Create a Button with the hamburger icon
    hamburger_button = tk.Button(
        mainCanv, 
        image=burg, 
        bg="slategray", 
        relief="flat", 
        command=toggle_menu  # Command to toggle the side menu
    )
    hamburger_button.image = burg  # Keep a reference to avoid garbage collection
    hamburger_button.pack(side="right", padx=10, pady=10, expand=False)

def makeMainWin():
    """Create the main window."""
    global mainWin, mainCanv, rect, tree_frame, tree, rating_source_combobox, menu_frame, is_menu_open

    # Create base window
    mainWin = tk.Tk()
    mainWin.minsize(480, 270)
    mainWin.title("Multi-Era Media Comparison")
    mainWin.state("zoomed")
    mainWin.config(bg="slategray")
    mainWin.grid_columnconfigure(0, weight=1)
    mainWin.grid_rowconfigure(2, weight=1)

    # Initialize variables
    is_menu_open = False  # Initialize is_menu_open to avoid referencing before assignment
    menu_frame = None

    # Create the canvas for the top bar
    mainCanv = tk.Canvas(mainWin, highlightthickness=0, height=50, bg="goldenrod")
    mainCanv.grid(row=0, column=0, sticky="ew")
    rect = mainCanv.create_rectangle(0, 0, 50, 50, fill="goldenrod")
    mainCanv.bind("<Configure>", lambda e: mainCanv.coords(rect, 0, 0, mainWin.winfo_width(), 50))

    # Rating source combobox
    rating_source_combobox = ttk.Combobox(mainWin, values=list(rating_sources.keys()), state="readonly")
    rating_source_combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    rating_source_combobox.set("Rotten Tomatoes Critics")  # Default selection
    rating_source_combobox.bind("<<ComboboxSelected>>", update_movie_list)

    # Create a frame for the Treeview
    tree_frame = tk.Frame(mainWin, bg="slategray")
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    mainWin.bind("<Configure>", update_padding)

    # Add Treeview with scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical")
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
    hsb.pack(side=tk.BOTTOM, fill=tk.X)

    tree = ttk.Treeview(
        tree_frame,
        columns=("name", "rating"),
        show="headings",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set,
        height=20
    )
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    # Define column headings
    tree.heading("name", text="Movie Name", anchor="w")
    tree.heading("rating", text="Rating", anchor="center")
    tree.column("name", width=2, anchor="w")
    tree.column("rating", width=2, anchor="center")

def mainMake():
    """Main function to start the program."""
    global movie_list
    makeMainWin()
    movie_list = load_movie_data('movies.csv')
    display_movie_list(movie_list, "RT_C")
    makeMainWidg()
    mainWin.bind("<Configure>", lambda event: update_padding())
    mainWin.mainloop()

if __name__ == "__main__":
    mainMake()
