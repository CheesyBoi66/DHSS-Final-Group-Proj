import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # To load and display the logo image
import csv

# Global variable for rect
rect = None

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

rect = None

def load_movie_data(filename):
    # Load movie data with different rating sources
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        movies = []
        for row in reader:
            movies.append({
                "name": row['name'],
                "year": int(row['year']),
                "RT_C": float(row['RT_C']),
                "RT_A": float(row['RT_A']),
                "MC_C": float(row['MC_C']),
                "MC_A": float(row['MC_A']),
                "DB": row['DB'],
                "gross": row['gross'],
                "AV_C": float(row['AV_C']),
                "AV_A": float(row['AV_A']),
                "AV_DIFF": row['AV_DIFF'],
                "AV_OVR": row['AV_OVR'],
            })
        return movies
def display_movie_list(movie_list, selected_rating_source):
    # Create Treeview with Scrollbars
    tree_frame = tk.Frame(mainWin, bg="slategray")
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Add vertical scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical")
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # Add horizontal scrollbar
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

    tree.column("name", width=300, anchor="w")
    tree.column("rating", width=80, anchor="center")

    # Clear the Treeview before inserting new data
    for item in tree.get_children():
        tree.delete(item)

    # Sort movies by year
    movie_list.sort(key=lambda x: x['year'])

    current_year = None
    for movie in movie_list:
        if movie['year'] != current_year:
            current_year = movie['year']
            # Insert year as a bold separator
            tree.insert("", "end", values=(f"--- {current_year} ---", ""), tags=("year",))
        # Insert movie details based on the selected rating source
        rating = movie[selected_rating_source]
        tree.insert("", "end", values=(movie['name'], rating))

    # Add styling for year separators
    tree.tag_configure("year", font=("Arial", 10, "bold"), foreground="blue")

def update_movie_list(event):
    # Get the selected display name from the combobox
    selected_display_name = rating_source_combobox.get()

    # Map the display name to the actual column name
    selected_rating_source = rating_sources[selected_display_name]

    # Now, you can update the movie list based on selected_rating_source (the internal column name)
    display_movie_list(movie_list, selected_rating_source)

def makeMainWin():
    global mainWin, mainCanv, rect, rating_source_combobox  # Declare rect and other variables as global here
    mainWin = tk.Tk()
    mainWin.minsize(480, 270)  # Setting up program basics and startup options
    mainWin.title("Multi-Era Media Comparison")
    mainWin.state("zoomed")  # Starts the program maximized
    mainWin.config(bg="slategray")
    mainWin.grid_columnconfigure(0, weight=1)
    mainWin.grid_rowconfigure(2, weight=1)

    # Create the canvas for the top orange bar
    mainCanv = tk.Canvas(mainWin, highlightthickness=0, height=50)
    mainCanv.grid(row=0, column=0, sticky="ew")
    
    # Create the orange bar rectangle
    rect = mainCanv.create_rectangle(0, 0, 50, 50, fill="goldenrod")
    
    mainCanv.bind("<Configure>", rectUp)  # Connects the resizing function for header when window is resized

    # Create the rating source combobox
    rating_source_combobox = ttk.Combobox(mainWin, values=list(rating_sources.keys()), state="readonly")
    rating_source_combobox.set("Rotten Tomatoes Critics")  # Default selection
    rating_source_combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    rating_source_combobox.bind("<<ComboboxSelected>>", update_movie_list)

def rectUp(thing):  # Called to update the width of top bar when window is resized
    canvas_width = thing.width
    mainCanv.coords(rect, 0, 0, canvas_width, 50)  # Now rect is defined globally, so it can be used here

def mainMake():
    global movie_list
    makeMainWin()
    movie_list = load_movie_data('movies.csv')  # Adjust path to your CSV file
    display_movie_list(movie_list, "RT_C")  # Default to Rotten Tomatoes Critics rating
    mainWin.mainloop()

if __name__ == "__main__":
    mainMake()
