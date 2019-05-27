#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets.
# ***
# 
# This project involves data analysis for a company that builds Android and iOS mobile apps. The company makes its apps available on Google Play and the App Store.
# 
# They only build apps that are free to download and install, and their main source of revenue consists of in-app ads. This means their revenue for any given app is mostly influenced by the number of users who use their app — the more users that see and engage with the ads, the better. 
# My goal for this project is to analyze data to help the company's developers understand what type of apps are likely to attract more users.
# 
# ## In this project, we will:
# - use Python data analysis tools to analyze apps on Google Playstore and AppleStore.
# -  collect and analyze data about mobile apps available on Google Play and the App Store.
# - Use relevant existing data from [link](https://www.kaggle.com/lava18/google-play-store-apps/home) that contains data about Android apps from Google Play, and [link](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home) which contains data about Apple store apps.
# - Use this data to help developers understand what type of apps are likely to attract more users
# 

# Open the data sets to make them easier to explore. The function `explore_data()` can be used repeatedly to print ros in a readable way.

# In[1]:


from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android_apps_data = list(read_file)
android_header = android_apps_data[0]
android_data = android_apps_data[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
apple_apps_data = list(read_file)
apple_header = apple_apps_data[0]
apple_data = apple_apps_data [1:]


# In[2]:


def explore_data(apps_data, start, end, rows_and_columns=False):
    dataset_slice = apps_data[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(apps_data))
        print('Number of columns:', len(apps_data[0]))
        print()


# In[3]:


print("Google play store explored data are \n ")
explore_data(android_apps_data, 0, 5, True)
print("Apple store explored data are : \n ")
explore_data(apple_apps_data, 0, 5, True)
print()
print()
print("Column names are: \n")
print("Google play store columns: \n")
print(android_header)
print()
print()
print("Apple store columns: \n")
print(apple_header)



# 
# We see that the Google Play data set has 10841 apps and 13 columns. At a quick glance, the columns that might be useful for the purpose of our analysis are 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genres'.
# 
# We have 7197 iOS apps in this data set, and the columns that seem interesting are: 'track_name', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'. Not all column names are self-explanatory in this case, but details about each column can be found in the data set [column details](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)
# 

# # Cleaning the Data
# ***
# The Google Play data set has a dedicated [discussion section](https://www.kaggle.com/lava18/google-play-store-apps/discussion), and we can see that [one of the discussions](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) outlines an error for row 10472. Let's print this row and compare it against the header and another row that is correct.

# In[4]:


print("Android erroneous row. \n")
print(android_data[10472])
print()
print("The row 10472 corresponds to the app Life"
      "Made WI-Fi Touchscreen Photo Frame,"
      "and we can see that the rating is 19."
      "This is clearly off because the maximum "
      "rating for a Google Play app is 5. "
      "As a consequence, we'll delete this row.\n")
print()
print(android_header)


# In[5]:


print(len(android_data))
del android_data[10472]
print()
print(len(android_data))


# ## 1. Removing duplicate data
# ***
# ## Part one
# If we explore the Google Play data set long enough, we'll find that some apps have more than one entry. For instance, the application Instagram has four entries:

# In[6]:


for app in android_data:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In total, there are 1,181 cases where an app occurs more than once:

# In[7]:


duplicates =[]
unique_apps = []

for app in android_data:
    name = app[0]
    if name in unique_apps:
        duplicates.append(name)
    unique_apps.append(name)

print("The number of duplicate apps is :", len(duplicates))
print()
print("Examples of duplicate apps is such as ", duplicates[:10])


# We don't want to count certain apps more than once when we analyze data, so we need to remove the duplicate entries and keep only one entry per app. One thing we could do is remove the duplicate rows randomly, but we could probably find a better way.
# 
# If you examine the rows we printed two cells above for the Instagram app, the main difference happens on the fourth position of each row, which corresponds to the number of reviews. The different numbers show that the data was collected at different times. We can use this to build a criterion for keeping rows. We won't remove rows randomly, but rather we'll keep the rows that have the highest number of reviews because the higher the number of reviews, the more reliable the ratings.
# 
# To do that, we will:
# 
# - Create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app
# - Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)
# 

# ## Part two
# Lets start by building the dictionary

# In[8]:


reviews_max = {}

for app in android_data:
    name = app[0]
    no_reviews = float(app[3])
        
    if name in reviews_max and reviews_max[name] < no_reviews:
        reviews_max[name] = no_reviews
    
    elif name not in reviews_max:
        reviews_max[name] = no_reviews

print("Expected length : \n", len(android_data)-1181)
print("Actual length : \n", len(reviews_max))


# We are going to use the dictionary above to remove the duplicate rows. 
# - Start by creating two empty lists: `android_clean` (which will store our new cleaned data set) and `already_added` (which will just store app names).
# - Loop through the Google Play data set, without including the header row, and for each iteration:
# 1. assign the app name to a variable named name
# 2. convert the number of reviews to `float`, and assign it to a variable named `n_reviews`
# - If n_reviews is the same as the number of maximum reviews of the app name (the number can be found in the reviews_max dictionary) and name is not already in the list already_added, then:
# 1. append the entire row to the `android_clean` list
# 2. append the `name` to the `already_added` list.
# - The `android_clean` data set should have 9,659 rows.

# In[9]:


android_clean = []
already_added = []

for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    
    for name in reviews_max:
        if (n_reviews == reviews_max[name]) and (name not in already_added):
            android_clean.append(app)
            already_added.append(name)
            


# Now, lets explore the `android_clean` data, which is cleaned data, to ensure that there are only 9,659 rows.

# In[20]:


explore_data(android_clean, 0, 3, True)


# ## 2. Removing non English apps
# ***
# 
# Remember that the company develops their applications in English, but the data sets both have apps with names that suggest they are not directed toward an English-speaking audience.
# 

# In[11]:


print(apple_data[813][1])
print(apple_data[6731][1])

print(android_clean[4412][0])
print(android_clean[7940][0])


# To remove non-English apps, we are going to remove apps that have names containing a symbol that is not commonly used in English text. 
# NB: English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;), and other symbols (+, *, /).
# 
# All these characters that are specific to English texts are encoded using the ASCII standard. Each ASCII character has a corresponding number between 0 and 127 associated with it, and we can take advantage of that to build a function that checks an app name and tells us whether it contains non-ASCII characters.
# 
# We built this function below, and we use the built-in ord() function to find out the corresponding encoding number of each character.
# 
# The function seems to work fine, but some English app names use emojis or other symbols (™, — (em dash), – (en dash), etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form. 
# Therefore, we'll only remove an app if its name has more than three characters with corresponding numbers falling outside the ASCII range. This means all English apps with up to three emoji or other special characters will still be labeled as English.
# 

# In[12]:


def is_english(name):
    non_ascii = 0
    
    for character in name:
        if ord(character) > 127:
            non_ascii += 1
            
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Instachat 😜'))
    
        


# The function is still not perfect, and very few non-English apps might get past our filter, but this seems good enough at this point in our analysis
# We shouldn't spend too much time on optimization at this point.
# 
# Below, we use the is_english() function to filter out the non-English apps for both data sets:
# 

# In[13]:


android_english = []
apple_english = []

for app in android_clean:
    if is_english(app[0]):
        android_english.append(app)
        
for app in apple_data:
    if is_english(app[1]):
        apple_english.append(app)
        
explore_data(android_english, 0, 3, True)
print()
explore_data(apple_english, 0, 3, True)


# ## 3. Isolating Free Apps
# ***
# So far, we have removed:
# - inaccurate data
# - duplicate data entries
# - non-english apps
# 
# The company only builds apps that are free to download and install. The data sets contain both free and non-free apps.
# Isolating the free apps will be our last step in the data cleaning.

# In[14]:


android_final = []
apple_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in apple_english:
    price = app[4]
    if price == '0.0':
        apple_final.append(app)
        
explore_data(android_final, 0, 3, True)
explore_data(apple_final, 0, 3, True)
        


# # Data Analysis
# ***
# So far, we have managed to clean the data and are now ready to start our anlysis. The aim of this analysis is to determine the kinds of apps that are likely to attract more users because the company's revenue is highly influenced by the number of people using their apps.
# 
# To minimize risks and overhead, the company's validation strategy for an app idea is comprised of three steps:
# - Build a minimal Android version of the app, and add it to Google Play.
# - If the app has a good response from users, we develop it further.
# - If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because the end game is to build apps that can be added on both Google Play Store and App Store, we need to find app profiles that are successful on both markets. 

# ## Most Common Apps by genre
# Let's begin the analysis by getting a sense of the most common genres for each market. For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.
# 
# ## Part one
# 
# We'll build two functions we can use to analyze the frequency tables:
# - One function to generate frequency tables that show percentages
# - Another function that we can use to display the percentages in a descending order using the built-in function `sorted()`. (This function doesn't work well with dictioanries as it inspects the keys, but we want to inspect the values. Threfore, we convert our dictionary into a list of tuple, with each tuple containing a dictionary key and its corresponding frequency. The sorted function will take the list of tuples and return a list of its elements in ascending or descending order).
# 

# In[15]:


# function for generating a frequency table

def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages

# function for sorting a dictionary

def display_table(dataset, index): # dataset is a list of lists
    table = freq_table(dataset, index)  # generate a frequency table using the freq_table function
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)  # a tuple containing value key pairs
        table_display.append(key_val_as_tuple)  # a list of tuple
        
    table_sorted = sorted(table_display, reverse=True)  # returns table sorted in descending order
    for entry in table_sorted:
        print(entry[1], ':', entry[0])  # print the key value pairs inside the sorted table


# In[16]:


display_table(apple_final, -5)


# On examining the App Store apps, we can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.

# In[17]:


# examining the Genres and Category columns of the Google Play data set 
display_table(android_final, 1) # Category


# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# Even so, practical apps seem to have a better representation on Google Play compared to App Store. This picture is also confirmed by the frequency table we see for the Genres column:
# 

# In[18]:


display_table(android_final, -4) # genre


# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# ## 1. Most Popular Apps by Genre on the App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# We will start by calculating the average number of user ratings per app genre on the App Store. To do that, we'll need to:
# - Isolate the apps of each genre.
# - Sum up the user ratings for the apps of that genre.
# - Divide the sum by the number of apps belonging to that genre (not by the total number of apps).
# 

# In[22]:


# calculate the average number of user ratings per app genre on the App Store
genre_apple = freq_table(apple_final, -5)  # dictionary of genres and frequencies as values

for genre in genre_apple:
    total = 0  # stores the sum of user ratings (the number of ratings, not the actual ratings) specific to each genre.
    len_genre = 0  # stores the number of apps specific to each genre.
    for row in apple_final:
        genre_app = row[-5]
        if genre == genre_app:
            n_rating = float(row[5])
            total += n_rating
            len_genre += 1
    average_rating = total / len_genre
    print(genre, ':', average_rating)
        


# In[24]:


for app in apple_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# After analyzing the results above, I would recommend `Navigation` as an app profile for the App Store seeing it has the most user ratings, ` 86090.33333333333`.
# However, this figure is heavily influenced by `Waze` and `Google Maps`, which have close to half a million user reviews together:
# 
# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.

# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[25]:


for app in apple_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# 
# 
# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# - Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# - Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# - Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 

# ## 2. Most Popular Apps by Genre on Google Play
# Lets analyze the Google Play market a bit.

# In[23]:


display_table(android_final, 5)


# In the cell above, we have displayed the data for the install columns of the Google Play store. The install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.).
# For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to find out which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on.
# To perform computations, however, we'll need to convert each install number from string to float. This means we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error.
# Let's calculate the average number of installs per app genre for the Google Play data set.

# In[26]:


android_categories = freq_table(android_final, 1)

for category in android_categories:
    total = 0  # stores the sum of installs specific to each genre
    len_category = 0  # stores the number of apps specific to each genre
    
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace('+', '')
            n_installs = n_installs.replace(',', '')
            n_installs = float(n_installs)
            total += n_installs
            len_category += 1
            
    average_no_installs = total / len_category
    print(category, ':', average_no_installs)
    


# On average, communication apps have the most installs: 63426839. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[29]:


# analsis of the communication category
for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])
        


# If we removed all the communication apps that have over 50 million installs, the average would be reduced roughly ten times:
# 

# In[42]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 50000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# In[43]:


for app in android_final:
    if app[1] == 'VIDEO_PLAYERS':
          print(app[0], ':', app[5])


# We see the same pattern for the video players category, which is the second runner-up with 30212769 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 4768215. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[44]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[46]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                           or app[5] == '500,000,000+'
                                           or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[50]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                           or app[5] == '50,000,000+'
                                           or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# # Conclusions
# ***
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
