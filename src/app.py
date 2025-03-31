import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://companies-market-cap-copy.vercel.app/index.html'
response = requests.get(url)
print("Código de respuesta: " , response.status_code)
print(response.text)
soup = BeautifulSoup(response.text,"html.parser")
table = soup.find("table")
table

rows = table.find_all("tr")

data = []
for row in rows[1:]:
    cols = row.find_all("td")
    year = cols[0].text.strip()
    income = cols[1].text.strip()
    data.append([year,income])

df = pd.DataFrame(data,columns=["Year","Income"])

df["Income"]=df["Income"].str.replace("$","")
df["Income"]=df["Income"].str.replace("B","")
print(df)
 
connection = sqlite3.connect("tesla.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS incomess_tesla (
   year CHAR(4), 
   income REAL
)""")

for i, row in df.iterrows():
    cursor.execute("INSERT INTO incomess_tesla (year, income) VALUES (?, ?)", (int(row["Year"]), float(row["Income"])))
connection.commit()
connection.close()

plt.subplot(1, 3, 1)
plt.plot(df["Year"], df["Income"], marker="o", linestyle="-", color="b")
plt.title("Ingresos por Año (Línea)")
plt.xlabel("Año")
plt.ylabel("Ingresos")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.bar(df["Year"], df["Income"], color="g")
plt.title("Ingresos por Año (Barras)")
plt.xlabel("Año")
plt.ylabel("Ingresos")

plt.subplot(1, 3, 3)
plt.scatter(df["Year"], df["Income"], color="r")
plt.title("Ingresos por Año (Dispersión)")
plt.xlabel("Año")
plt.ylabel("Ingresos")

# Mostrar los gráficos
plt.tight_layout()
plt.show()