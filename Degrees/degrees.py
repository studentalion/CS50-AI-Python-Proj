import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Load row by row
            # row["id"] means the top of column is "id" and read
            # that column "id" in this row
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            
            # add in set
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
                # dont know whats this
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    # Default:large dataset
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Input source and target(in string)
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find path
    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        # Using formatted string
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        # Turn ids into names and formatted print out
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    Using BFS in order to find the shortest path

    Noticeably,source and target are ids.
    """
    visited = set()

    frontier = QueueFrontier()
    # Source is already id-format
    start = Node(state=source,parent=None,action=None)

    frontier.add(start)
    """
    BFS:
    Declare a queue and insert the starting vertex.
    Initialize a visited array and mark the starting vertex as visited.
    Follow the below process till the queue becomes empty:
    Remove the first vertex of the queue.
    Mark that vertex as visited.
    Insert all the unvisited neighbours of the vertex into the queue.
    """
    while 1:
        if frontier.empty():
            return None
        
        node = frontier.remove()
        visited.add(node.state)
        neighbors = neighbors_for_person(node.state)
        for movie,person in neighbors:
            # Not in frontier and not visited
            if person not in visited and not frontier.contains_state(person):
                child = Node(state=person,parent=node,action=movie)
                if child.state == target:
                    path = []
                    node = child
                    # Create path from end to top
                    while node.parent is not None:
                       path.append((node.action,node.state))
                       node = node.parent
                    # Return path
                    path.reverse()
                    return path
                frontier.add(child)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.4
    """
    # get Method:if not find in dict then return a empty set
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    # If more than one then choose one
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    # 2D dict
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

# If run this file directly then run main()
if __name__ == "__main__":
    main()
