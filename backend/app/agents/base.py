from openai import OpenAI

from app.core.config import GROQ_API_KEY


class BaseAgent:

    def __init__(self):

        self.client = OpenAI(

            api_key=GROQ_API_KEY,

            base_url="https://api.groq.com/openai/v1"

        )

    async def call_llm(

        self,
        system_prompt,
        user_prompt

    ):

        try:

            completion = self.client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ]

            )

            return completion.choices[0].message.content

        except Exception as e:

            return str(e)