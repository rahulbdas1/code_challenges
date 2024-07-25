import requests
import pandas as df

def url_redirect_detector(csv_path, outgoing_csv_path, threads=10):
        csv_df = df.read_csv(csv_path)
        #rename df columns dynamically
        csv_df.rename(columns={csv_df.columns[0]: "original_url"}, inplace=True)
        csv_df['redirect_url'] = csv_df['original_url'].apply(checks_redirect_url)
        csv_df.drop(csv_df[csv_df.redirect_url == ""].index, inplace = True)
        csv_df.to_csv(outgoing_csv_path + 'redirect_urls.csv', index=False)
        #print(csv_df)

'''This function wll retry urls as well as return non-empty values if redirect urls are diff than og URL'''
def checks_redirect_url(url,tries=5):
    for i in range(tries):
        try:
            url_response = requests.get(url,allow_redirects=True)
            if url_response.history:
                redirect_url = url_response.url
            else:
                redirect_url = ""
            #If redirect url is same as the og url, than no need to persist the og url 2x
            if redirect_url != url:
                return redirect_url
            else:
                return ""
        except KeyError as e:
            if i < tries- 1: # i is zero indexed
                continue
            else:
                raise
        break     

if __name__ == "__main__":
    # using the urls.csv file with smaller url data
    url_redirector = url_redirect_detector("src/resources/data/urls.csv","src/resources/outgoing_data/",10)



    
    
