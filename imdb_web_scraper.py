from bs4 import BeautifulSoup
import requests
import csv

# URL in which CSV will be based off of (Please change for different results)
URL = "https://www.imdb.com/list/ls009668579/"
# Name of output CSV file (change to what you want your file to be named)
CSV_NAME = 'imdb_scrape.csv'

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'lxml')
g_data = soup.find_all("div", {"class": "lister-item-content"})

# create final list for all movie data
movie_list = list()


# ----------------Functions---------------
# function that returns movie title
def get_movie_title(movie):
    movie_title = movie.find("a").text
    return movie_title


# function that returns movie year
def get_movie_year(movie):
    movie_year = movie.find("span", {"class": "lister-item-year text-muted unbold"}).text
    movie_year = movie_year.replace("I", "")
    movie_year = movie_year.replace("(", "")
    movie_year = movie_year.replace(")", "")
    return movie_year.strip()


# function that returns movie rating, i.e. PG, R, PG-13
def get_movie_rating(movie):
    return movie.find("span", {"class": "certificate"}).text


# function that returns runtime of movie
def get_movie_runtime(movie):
    return movie.find("span", {"class": "runtime"}).text


# function that returns genre of movie
def get_movie_genre(movie):
    movie_genre = movie.find("span", {"class": "genre"}).text
    return movie_genre.replace("\n", '').strip()


# function that returns score out of 10 for movie
def get_movie_score(movie):
    movie_score = movie.find("div", {"class": "ipl-rating-star"}).text
    return movie_score.replace("\n", '') + "/10"


# function that returns summary description of movie
def get_movie_sum(movie):
    movie_sum_list = movie.find("p", {"class": ""})
    # start = movie_sum_list[1].text.find("Metascore") + 6
    # end = movie_sum_list[1].text.find("Director")
    return movie_sum_list.text.strip()


# function that returns link to IMDb movie page
def get_movie_link(movie):
    for link in movie.find_all("a"):
        movie_link = link.get("href")
        if(movie_link.startswith("/title")):
            break
    return "https://www.imdb.com" + movie_link


# ------------------Implementation------------------
# parse through all the movies on the IMDb web page
for movie in g_data:
    current_movie = list()
    try:
        # add movie title
        current_movie.append(get_movie_title(movie))
    except Exception:
        print("Error getting movie title")
        pass
    try:
        # add movie Year
        current_movie.append(get_movie_year(movie))
    except Exception:
        print("Error getting movie year")
        pass
    try:
        # add movie title
        current_movie.append(get_movie_rating(movie))
    except Exception:
        print("Error getting movie rating")
        pass
    try:
        # add runtime
        current_movie.append(get_movie_runtime(movie))
    except Exception:
        print("Error getting movie runtime")
        pass
    try:
        # add genres
        current_movie.append(get_movie_genre(movie))
    except Exception:
        print("Error getting movie genre")
        pass
    try:
        # add socre
        current_movie.append(get_movie_score(movie))
    except Exception:
        print("Error getting movie score")
        pass
    try:
        # add movie summary
        current_movie.append(get_movie_sum(movie))
    except Exception:
        print("Error getting movie summary")
        pass
    try:
        # add movie link
        current_movie.append(get_movie_link(movie))
    except Exception:
        print("Error getting movie link")
        pass
    # add the entire row of movie data to the list
    movie_list.append(current_movie)

# creating the csv file to write to
csv_file = open(CSV_NAME, 'w')

# create csv file and write out first row
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Year', 'Rating', 'Duration', 'Genre', 'Score', 'Summary', 'Link'])

for movie in movie_list:
    csv_writer.writerow(movie)

# prints out a list version of the csv sheet to double check
print(movie_list)

# close the file
csv_file.close()
