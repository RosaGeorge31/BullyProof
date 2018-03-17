import urllib2
import json
import datetime
import csv
import time

#app_id = "<FILL IN>"
#app_secret = "<FILL IN>" # DO NOT SHARE WITH ANYONE!
page_id = raw_input("Please Paste Post status_id:")

#access_token = app_id + "|" + app_secret

access_token = raw_input("Please Paste Your Access Token:")

# Needed to write tricky unicode correctly to csv
def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 
                            0x201D:0x22, 0xa0:0x20 }).encode('utf-8')

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())
            print "Retrying."

    return response.read()

def getFacebookPageFeedData(page_id, access_token):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
  
    base = "https://graph.facebook.com"
    node = "/%s/likes?limit=2000" % page_id 

    parameters = "&access_token=%s" % (access_token)
    url = base + node + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data

def scrapeFacebookPageFeedStatus(page_id, access_token):
  

        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)

        statuses = getFacebookPageFeedData(page_id, access_token)

        file = open('%s_likes.csv' % page_id, 'wb')                                                                                      
        w = csv.writer(file)
        w.writerow(["user_id", "user_name"])
 
        while has_next_page:
            for status in statuses['data']:
              
                # Ensure it is a status with the expected metadata
                if status!= {}:
                    w.writerow([unicode_normalize(status["id"]),unicode_normalize(status["name"])])
                else:
                    has_next_page = False
                    
                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print "%s Likes Processed: %s" % \
                        (num_processed, datetime.datetime.now())

            # if there is no next page, we're done.
            
            try:
               if 'paging' in statuses.keys():
                
                statuses = json.loads(request_until_succeed(
                                        statuses['paging']['next']))
               
            except KeyError:
                has_next_page = False


        print "\nDone!\n%s Statuses Processed in %s" % \
                (num_processed, datetime.datetime.now() - scrape_starttime)


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token)


# The CSV can be opened in all major statistical programs. Have fun! :)
