from openai import OpenAI
import pprint

from langchain_community.utilities import SearxSearchWrapper

base_url = "https://api.aimlapi.com/v1"
api_key = "842b61037d4049a3b3f824ffdba905b3"
system_prompt = "You are a travel agent. Be descriptive and helpful."
user_prompt = "Tell me about San Francisco"

client = OpenAI(api_key=api_key, base_url=base_url)
search = SearxSearchWrapper(searx_host="http://127.0.0.1:8888")
search.run("What is the capital of France")
# prompt = """
# Instructions:
# - Given the React component below, change it so that nonfiction books have red
#   text.
# - Return only the code in your reply
# - Do not include any additional formatting, such as markdown code blocks
# - For formatting, use four space tabs, and do not allow any lines of code to
#   exceed 80 columns

# const books = [
#   { title: 'Dune', category: 'fiction', id: 1 },
#   { title: 'Frankenstein', category: 'fiction', id: 2 },
#   { title: 'Moneyball', category: 'nonfiction', id: 3 },
# ];

# export default function BookList() {
#   const listItems = books.map(book =>
#     <li>
#       {book.title}
#     </li>
#   );

#   return (
#     <ul>{listItems}</ul>
#   );
# }
# """

# response = client.chat.completions.create(
#     model="o1-mini",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": prompt
#                 },
#             ],
#         }
#     ]
# )

# print(response.choices[0].message.content)
