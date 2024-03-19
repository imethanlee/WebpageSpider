import numpy as np
import pandas as pd
import requests

if __name__ == "__main__":
    try:
        r = requests.get("https://openphish.com/feed.txt")
    except Exception as e:
        print(f"Access OpenPhish fails. [{e}]")

    urls = r.text.split('\n')[:-1]
    urls = np.array(urls)
    np.random.shuffle(urls)
    urls = urls[:500]
    df_urls = pd.DataFrame(data={"url": urls})
    df_urls.to_csv("./input/example_phishing_urls.csv", index=False)
