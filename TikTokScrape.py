from TikTokApi import TikTokApi
import pandas as pd

api = TikTokApi.get_instance()

def cleanData(data):
    nested_values = ['video', 'author', 'music', 'stats', 'authorStats']

    # Creates a dictionary for our df to be stored in
    flattened_data = {}

    for id, value in enumerate(data):
        flattened_data[id] = {}
        # Loop through each element
        for prop_id, prop_value in value.items():
            # Check if nested
            if prop_id in nested_values:
                for nested_id, nested_value in prop_value.items():
                    flattened_data[id][prop_id + '_' + nested_id] = nested_value
            # If it's not nested, add it back to the flattened dictionary
            else:
                flattened_data[id][prop_id] = prop_value

    return pd.DataFrame.from_dict(flattened_data, orient='index')


def getUserVideos(userDefID, secDefUID):
    cursorValue = 0
    hasMore = True
    df = pd.DataFrame()

    while hasMore:
        TikTokList = api.user_page(userID=userDefID,
                                   secUID=secDefUID,
                                   cursor=cursorValue)

        data = cleanData(TikTokList['itemList'])
        df = df.append(data)

        cursorValue = int(TikTokList['cursor'])
        hasMore = TikTokList['hasMore']
    else:
        print("No more data")
        df.to_csv('analytics.csv')

def inputUserID():
    userName = input("Enter Username: ")
    userInfo = api.get_user(userName)
    userID = userInfo['id']
    secUID = userInfo['secUid']

    return userID, secUID

userInfo = inputUserID()

getUserVideos(userInfo[0], userInfo[1])
