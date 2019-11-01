
# coding: utf-8

# # Exploring Hacker News Posts
# 
# This project will compare posts in Hacker News based on certain criteria and determine what factors might cause posts to receive more comments on average

# In[10]:


from csv import reader
with open("hacker_news.csv", encoding="utf8") as file_read:
    data_read = reader(file_read)
    hn = list(data_read)

for row in hn[:5]:
    print(row)
    
print("Total number of rows in list is ", len(hn))
    


# The first list in the inner lists contains the column headers, and the lists after contain the data for one row. In order to analyze our data, we need to first remove the row containing the column headers.

# In[11]:


headers = hn[0]
hn = hn[1:]
print(headers)
for row in hn[:5]:
    print(row)


# Since we're only concerned with post titles beginning with Ask HN or Show HN, we'll create new lists of lists containing just the data for those titles.

# In[12]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    # Convert to lower case to make comparison simpler
    title = title.lower()
    if title.startswith('ask hn'):
        ask_posts.append(row)
    elif title.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

# Print out number of items sorted through the lists
print(len(ask_posts), len(show_posts), len(other_posts))

# Print out first five rows of ask and show posts just to check
for row in ask_posts[:5]:
    print(row)
    
for row in show_posts[:5]:
    print(row)


# In[13]:


# Determine if ask posts or show posts get more comments on average
total_ask_comments = 0
for row in ask_posts:
    # Get the number of comments for the current ask hn post
    num_comments = row[4]
    # Convert string to number
    num_comments = int(num_comments)
    # add number of comments to running counter
    total_ask_comments += num_comments

# Compute average for ask hn comments
avg_ask_comments = total_ask_comments/len(ask_posts)

total_show_comments = 0
for row in show_posts:
    # Get the number of comments for the current ask hn post
    num_comments = row[4]
    # Convert string to number
    num_comments = int(num_comments)
    # add number of comments to running counter
    total_show_comments += num_comments

# Compute average for ask hn comments
avg_show_comments = total_show_comments/len(show_posts)

print("Average Number of Ask HN Comments is {0:.2f} per post".format(avg_ask_comments))

print("Average Number of Show HN Comments is {0:.2f} per post".format(avg_show_comments))


# On average, ask posts receive almost 40% more comments than show posts on Hacker News. Since ask posts are more likely to receive comments, we'll focus our remaining analysis just on these posts. Let's determine if ask posts created at a certain time are more likely to attract comments.

# In[14]:


import datetime as dt
result_list = []

for row in ask_posts:
    # Get the string date/time the post was created
    created_at = row[6]
    # Get the number of comments for the current ask hn post
    num_comments = row[4]
    # Convert string to number
    num_comments = int(num_comments)
    # Append data to result_list
    result_list.append([created_at, num_comments])

counts_by_hour = {}
comments_by_hour = {}
    
for row in result_list:
    created_at_dt = dt.datetime.strptime(row[0],"%m/%d/%Y %H:%M")
    hour = created_at_dt.strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = row[1]
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += row[1]

#for row in counts_by_hour:
#    print(row, counts_by_hour[row], comments_by_hour[row])

# Create a list containing the hours during which posts were created 
# and the average number of comments those posts received.

avg_by_hour = []
for row in counts_by_hour:
    avg_var = comments_by_hour[row]/counts_by_hour[row]
    avg_var = round(avg_var, 3)
    avg_by_hour.append([row, avg_var])
    #print(row, avg_var)
    
swap_avg_by_hour = []
for row in sorted(avg_by_hour):
    swap_avg_by_hour.append([row[1], row[0]])

# print(swap_avg_by_hour)

sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print("Top 5 Hours for Ask Posts Comments")
for item in sorted_swap[:5]:
    hour_dt = dt.datetime.strptime(item[1], "%H")
    hour_str = hour_dt.strftime("%H:%M:") 
    print(hour_str, "{:.2f}".format(item[0]), "comments per post.")


# Ask Posts started between 3PM to 4PM have the most number of average comments, followed by posts started at 1PM, closely followed by 12PM. Early afternoon (12PM to 3PM) seems like a good time, in general to start these types of posts.
