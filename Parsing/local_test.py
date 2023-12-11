import pandas as pd
import re

data = {
    "Engine_capacity": ["3.0 AT (286 л.с.)", "2.5 MT (180 л.с.)", "4.4 AT (450 л.с.)"]
}
df = pd.DataFrame(data)
df["Engine_capacity"] = df["Engine_capacity"].apply(lambda x: re.findall(r"\d+", x)[-1])

print(df)
