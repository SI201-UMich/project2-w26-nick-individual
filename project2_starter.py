# SI 201 HW4 (Library Checkout System)
# Your name: Nicholas Graden
# Your student id: 0189 8219
# Your email: ngraden@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Gemini
# If you worked with generative AI also add a statement for how you used it.

# It helped me with overall code structure, but it gave me deep understanding of my get_listing_details function.
# I struggled to write that one correctly, but Gemini helped with pulling my Policy Number and Location Rating

# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# Yes, I didn't ask it directly for code (but got deep clarification for what I mentioned earlier), so I think it aligns.
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    new_list = []
    fout = open(html_path, encoding="utf-8-sig")
    lst = BeautifulSoup(fout, 'html.parser')
    fout.close()
    listing_divs = lst.find_all('div', class_='t1jojoys dir dir-ltr')

    for tags in listing_divs:
        new_list.append((tags.text, tags['id'].replace("title_", "")))
    return new_list
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HEREs
    # ==============================
    results = {}
    file_path = "html_files/listing_" + listing_id + ".html"
    fout = open(file_path, encoding="utf-8-sig")
    lst = BeautifulSoup(fout, 'html.parser')
    fout.close()



    policy_number = "Pending"

    #Host Name + Room Type
    subtitle_tag = lst.find('h2', class_='_14i3z6h')
    
    if subtitle_tag:
        subtitle_text = subtitle_tag.text
        if "by" in subtitle_text.lower():
            host = subtitle_text.lower().split("by")[1].strip().title()
        else:
            host = "Unknown"
    else:
        subtitle_text = ""
        host = "Unknown"

    if "Private" in subtitle_text:
        room_type = "Private Room"
    elif "Shared" in subtitle_text:
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    #Location Rating
    rating = 0.0
    #Gemini helped with this
    for div in lst.find_all('div'):
        if 'Location' in div.text and len(div.text) < 30:
            span = div.find('span', class_=['_4oybiu', '_17p6nbba'])
            if span:
                try:
                    rating = round(float(span.text.split()[0]), 1)
                    if rating > 0.0:
                        break
                except:
                    pass
    
    #Host Type
    host_type_tag = lst.find('span', class_='_1mhorg9')
    if host_type_tag and "Superhost" in host_type_tag.text:
        host_type = "Superhost"
    else:
        host_type = "regular"

    #Policy Number
    policy_number = "Pending"


    results[listing_id] = {
        "policy_number": policy_number,
        "host_type": host_type,
        "host_name": host,
        "room_type": room_type,
        "location_rating": rating
    }

    return results


    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    basic_listings = load_listing_results(html_path)
    detailed_data = []
    
    for item in basic_listings:        
        title = item[0]
        listing_id = item[1]
        
        details_dict = get_listing_details(listing_id)
        
        inner_dict = details_dict[listing_id]
        
        policy = inner_dict["policy_number"]
        host_type = inner_dict["host_type"]
        host_name = inner_dict["host_name"]
        room_type = inner_dict["room_type"]
        rating = inner_dict["location_rating"]
        
        full_tuple = (title, listing_id, policy, host_type, host_name, room_type, rating)
        
        detailed_data.append(full_tuple)

    return detailed_data
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    outfile = open(filename, "w", encoding="utf-8-sig", newline='')
    writer = csv.writer(outfile)
    writer.writerow(["Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"])

    for row in sorted_data:
        writer.writerow(row)

    outfile.close()
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings_dict = {}

    for row in data:
        room_type = row[5]
        rating = row[6]

        if rating > 0.0:
            
            if room_type not in ratings_dict:
                ratings_dict[room_type] = []
            
            ratings_dict[room_type].append(rating)

    averages = {}

    for room_type, rating_list in ratings_dict.items():
        calculated_avg = sum(rating_list) / len(rating_list)
        averages[room_type] = round(calculated_avg, 1) 

    return averages
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_ids = []

    for row in data:
        listing_id = row[1]
        policy = row[2]

        if policy == "Pending" or policy == "Exempt":
            continue 

        is_valid = False

        if len(policy) == 14 and policy[0:2] == "20" and policy[4:7] == "-00" and policy[-3:] == "STR":
            first_nums = policy[2:4]
            second_nums = policy[7:11]
            
            if first_nums.isdigit() and second_nums.isdigit():
                is_valid = True

        elif len(policy) == 11 and policy[0:7] == "STR-000":
            last_nums = policy[-4:] 
            
            if last_nums.isdigit():
                is_valid = True

        if not is_valid:
            invalid_ids.append(listing_id)

    return invalid_ids
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_url = "https://scholar.google.com/scholar?q="
    full_url = base_url + query
    
    #Gemini said to add this in, said it acts as a 'bouncer' so Google doesn't block it
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_tags = soup.find_all('h3', class_='gs_rt')
    
    titles = []
    for tag in title_tags:
        titles.append(tag.text)
        
    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        details_list = []
        for listing_id in html_list:
            details_list.append(get_listing_details(listing_id))

        self.assertEqual(details_list[0]["467507"]["policy_number"], "STR-0005349")
        
        self.assertEqual(details_list[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(details_list[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(details_list[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        for listing in self.detailed_data:
            self.assertEqual(len(listing), 7)

        self.assertEqual(
            self.detailed_data[-1], 
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        )

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        output_csv(self.detailed_data, out_path)

        fout = open(out_path, "r", encoding="utf-8-sig")
        reader = csv.reader(fout)
        rows = list(reader)
        fout.close()

        self.assertEqual(
            rows[1], 
            ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        )

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)
        # TODO: Check that the average for "Private Room" is 4.9.
        self.assertEqual(avg_ratings["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        self.assertEqual(invalid_listings, ["16204265"])


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)