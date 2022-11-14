import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents new healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🐔 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🥣 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect('pick some fruits',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
          fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
          fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
          return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about ?')
  if not fruit_choice:
      streamlit.error("Please enter the fruit to get information.")
  else:
      backend_func = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(backend_func)
  
except URLError as e:
  streamlit.error()

#Dont run anything past here while we troubleshoot


def get_fruit_load_list():
          with  my_cnx.cursor() as my_cur:
                    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
          return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
          my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          my_data_rows = get_fruit_load_list()
          streamlit.dataframe(my_data_rows)

streamlit.stop()

fruit_add=streamlit.text_input('Which fruit would you like to add ?')
streamlit.write('Thanks for adding ',fruit_add)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

