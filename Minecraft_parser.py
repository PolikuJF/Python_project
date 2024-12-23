import requests
from bs4 import BeautifulSoup
import sqlite3

def get_serverss(sort_by="", order="asc", search=""):
    connection = sqlite3.connect("my_serverss.db")
    query = "SELECT * FROM Serverss"
    filters = []
    params = []
    if search:
        filters.append("server LIKE ?")
        params.append(f"%{search}%")
    if filters:
        query += " WHERE " + filters[0]
        for filter in filters[1:]:
            query += " AND " + filter
    if sort_by:
        query += " ORDER BY " + sort_by + (" ASC" if order == "asc" else " DESC")
    stmt = connection.cursor()
    stmt.execute(query, params)
    serverss = []
    for row in stmt.fetchall():
        serverss.append(list(row))
    stmt.close()
    connection.close()
    return serverss


def update_date():
  connection = sqlite3.connect('my_serverss.db')
  cursor = connection.cursor()
  cursor.execute('''
  DROP TABLE IF EXISTS Serverss
  ''')
  cursor.execute('''
  CREATE TABLE Serverss (
  server TEXT NOT NULL,
  players INTEGER,
  likes INTEGER,
  points INTEGER,
  link TEXT NOT NULL
  )
  ''')
  connection.commit()

  for page_number in range(1, 8):
    response = requests.get(f'https://minecraftrating.ru/page/{page_number}/')
    soup = BeautifulSoup(response.text, 'html.parser')
    serverss = []
    for player in soup.find_all('em',itemprop="playersOnline"):
      player = player.text
      player = int(player)
      serverss.append({
              "players": player
           })
    for i, server_name in enumerate(soup.find_all('div',itemprop="name")):
      serverss[i]["name"]=server_name.text
    for i, server_likes in enumerate(soup.find_all('div',class_="block-i tooltip")):
      server_likes = server_likes.text
      if len(server_likes) != len(server_likes.split('г', 1)[0]):
        server_likes = server_likes.split('г', 1)[0]
        server_likes = int(server_likes)
        serverss[i//2]["likes"]=server_likes
      else:
        server_likes = server_likes.split('б', 1)[0]
        server_likes = int(server_likes)
        serverss[i//2]["points"]=server_likes
    for i, server_link in enumerate(soup.find_all('a', itemprop = "url")):
      server_link='https://minecraftrating.ru'+server_link.get('href')
      serverss[i]["links"]=(server_link)   
    for server in serverss:
      cursor.execute(
            'INSERT INTO Serverss (server, players, likes, points, link) VALUES (?, ?, ?, ?, ?)',
            (f'{server["name"]}', f'{server["players"]}', f'{server["likes"]}', f'{server["points"]}', f'{server["links"]}'))  

  connection.commit()
  serverss = cursor.fetchall()
  connection.close()
  return serverss