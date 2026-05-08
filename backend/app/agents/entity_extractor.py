import json
from app.agents.base import BaseAgent


class EntityExtractor(BaseAgent):

    async def extract_entities(

        self,
        message,
        conversation_history=None

    ):

        if conversation_history is None:
            conversation_history = []

        system_prompt = f"""
        You extract structured business information from Instagram customer chats.

        Your task is to extract important business entities.

        CONVERSATION HISTORY:
        {conversation_history}

        Extract the following fields if available:

        - customer_name
        - product_name
        - payment_done
        - advance_amount
        - total_amount
        - negotiated_price
        - delivery_date
        - requested_delivery_date
        - address
        - urgency
        - customer_sentiment

        RULES:
        - Use null if unavailable
        - payment_done must be true or false
        - urgency can only be:
            low
            medium
            high
        - If message contains pricing negotiation like "1500 final",
        store it in negotiated_price

        - If customer mentions phrases like:
        "1500 final",
        "best price",
        "discount",
        "cheaper",
        extract the amount into negotiated_price

        - NEVER treat numbers/prices as product names

        - If customer mentions:
        paid,
        payment done,
        advance paid,
        transfer completed,
        then set payment_done = true

        - Urgent phrases include:
        urgent,
        ASAP,
        tomorrow,
        tonight,
        immediately,
        fast delivery

        - If urgent phrases detected,
        urgency = high
        - customer_sentiment can only be:
            positive
            neutral
            negative

        IMPORTANT:
        - Return ONLY valid JSON
        - No markdown
        - No explanation

        Example:

        {{
            "customer_name": null,
            "product_name": "Leather Bag",
            "payment_done": true,
            "advance_amount": 500,
            "total_amount": 2000,
            "negotiated_price": 1500,
            "delivery_date": "tomorrow",
            "requested_delivery_date": "Friday",
            "address": null,
            "urgency": "high",
            "customer_sentiment": "positive"
        }}
        """

        try:

            response = await self.call_llm(
                system_prompt,
                message
            )

            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

            return json.loads(response)

        except Exception as e:

            return {
                "customer_name": None,
                "product_name": None,
                "payment_done": False,
                "advance_amount": None,
                "total_amount": None,
                "negotiated_price": None,
                "delivery_date": None,
                "requested_delivery_date": None,
                "address": None,
                "urgency": "medium",
                "customer_sentiment": "neutral",
                "error": str(e)
            }