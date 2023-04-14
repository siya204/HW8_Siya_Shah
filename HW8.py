# Your name: Siya Shah
# Your student id: 58776189
# Your email: siya@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    dict = {}

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name, category_id, building_id, rating FROM restaurants")
    conn.commit()
    for restaurant in cur.fetchall():
        name = restaurant[0]        
        cur.execute("SELECT category FROM categories WHERE id = (?)", (restaurant[1],))
        category = cur.fetchall()[0]
        cur.execute("SELECT building FROM buildings WHERE id = (?)", (restaurant[2],))
        building = cur.fetchall()[0]
        rating = restaurant[3]

        dict[name] = {}
        dict[name]["category"] = category[0]
        dict[name]["building"] = building[0]
        dict[name]["rating"] = rating

    return dict

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    dict = {}
    cur.execute("SELECT * FROM categories")
    category_ids = cur.fetchall()
    for id in category_ids:
        cur.execute("SELECT COUNT(name) FROM restaurants WHERE category_id = (?)", (id[0],))
        total = cur.fetchall()[0]

        dict[id[1]] = total[0]   
    conn.commit()

    x = list(dict.keys())
    y = list(dict.values())
    plt.barh(x, y)
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Total Amount of Resteraunts per Category on South U St")
    plt.tight_layout()
    plt.show()

    return dict    

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT restaurants.name FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = (?) ORDER BY rating DESC", (building_num,))
    conn.commit()

    dict = []
    for name in cur.fetchall():
        dict.append(name[0])

    return dict
    


#EXTRA CREDIT
#def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.
    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    #def test_get_highest_rating(self):
        #highest_rating = get_highest_rating('South_U_Restaurants.db')
        #self.assertEqual(highest_rating, self.highest_rating)


if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
