#imports
############################################################
import string, numpy, time, math, csv
import tkinter as tk
from PIL import ImageTk, Image
############################################################
#windows
mainWin = tk.Tk()
mainCanv = tk.Canvas(mainWin,highlightthickness=0,height=50)
mainCanv.grid(row=0,column=0, sticky="ew")
rect = mainCanv.create_rectangle(0,0,50,50,fill="goldenrod")
############################################################
#vars

class listInfo:
    def __init__(self, name, RT_C, RT_A, MC_C, MC_A, DB, gross, AV_C, AV_A, AV_DIFF, year):
        self.name = name
        self.year = year
        self.stats = {
            "RottenTomatoes_Critic": RT_C,
            "RottenTomatoes_Audience": RT_A,
            "Metacritic_Critic": MC_C,
            "Metacritic_Audience": MC_A,
            "IMDB": DB,
            "Gross_Profit": gross,
            "Average_Critic": AV_C,
            "Average_Audience": AV_A,
            "Average_Difference": AV_DIFF,
        }

    @classmethod
    def from_csv(cls, row):
        return cls(
            name=row["name"],
            RT_C=int(row["RT_C"]),
            RT_A=int(row["RT_A"]),
            MC_C=int(row["MC_C"]),
            MC_A=float(row["MC_A"]),
            DB=float(row["DB"]),
            gross=int(row["gross"]),
            AV_C=float(row["AV_C"]),
            AV_A=float(row["AV_A"]),
            AV_DIFF=float(row["AV_DIFF"]),
            year=int(row["year"])
        )

def rectUp(thing):  # Called to update the width of top bar when window is resized
    canvas_width = thing.width
    mainCanv.coords(rect, 0, 0, canvas_width, 50)

def load_movie_data(filepath):
    movie_list = []
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_list.append(listInfo.from_csv(row))
    return movie_list

def display_movie_details(movie):
    details = (
        f"Name: {movie.name}\n"
        f"Year: {movie.year}\n"
        f"Rotten Tomatoes Critic: {movie.stats['RottenTomatoes_Critic']}\n"
        f"Rotten Tomatoes Audience: {movie.stats['RottenTomatoes_Audience']}\n"
        f"Metacritic Critic: {movie.stats['Metacritic_Critic']}\n"
        f"Metacritic Audience: {movie.stats['Metacritic_Audience']}\n"
        f"IMDB Critic: {movie.stats['IMDB_Critic']}\n"
        f"IMDB Audience: {movie.stats['IMDB_Audience']}\n"
        f"Gross: ${movie.stats['Gross_Profit']}\n"
        f"Average Critic: {movie.stats['Average_Critic']}\n"
        f"Average Audience: {movie.stats['Average_Audience']}\n"
        f"Average Difference: {movie.stats['Average_Difference']}\n"
    )

    details_label.config(text=details)

def create_movie_listbox(movies):
    frame = tk.Frame(mainWin, bg="slategray")
    frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    scrollbar = tk.Scrollbar(frame, orient="vertical")
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, bg="lightgray", font=("Arial", 14))
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    # Populate listbox with movie names
    for movie in movies:
        listbox.insert("end", f"{movie.name} ({movie.year})")

    # Handle movie selection
    def on_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            movie = movies[selected_index[0]]
            display_movie_details(movie)

    listbox.bind("<<ListboxSelect>>", on_select)

def makeMainWin():
    mainWin.minsize(480, 270)  # setting up program basics and startup options
    mainWin.title("Multi-Era Media Comparison")
    mainWin.state("zoomed")  # Starts the program maximized
    mainWin.config(bg="slategray")
    mainWin.grid_columnconfigure(0, weight=1)

    mainCanv.bind("<Configure>", rectUp)  # Connects the resizing function for header when window is resized

    # Load movie data from CSV
    movie_filepath = "movies.csv"  # Update this path to your CSV file
    movies = load_movie_data(movie_filepath)

    # Create the movie listbox
    create_movie_listbox(movies)

    # Label to display movie details
    global details_label
    details_label = tk.Label(mainWin, text="Select a movie to see details.", font=("Arial", 12), justify="left")
    details_label.grid(row=2, column=0, pady=20)

def main():
    makeMainWin()
    mainWin.mainloop()

main()
