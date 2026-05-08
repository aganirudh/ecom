import json
import re

from app.agents.base import BaseAgent


class IntentClassifier(BaseAgent):

    async def classify(self, message):

        system_prompt = f"""
        Classify the Instagram customer message into ONE intent.

        INTENTS:
        - negotiation
        - delivery_query
        - payment_query
        - complaint
        - product_inquiry
        - order_status
        - genuine_lead
        - spam
        - general

        RULES:

        - negotiation = asking for discount, final price, bargaining
        - delivery_query = asking about shipping or delivery timing
        - payment_query = discussing payment or advance
        - complaint = unhappy or angry customer
        - product_inquiry = asking product details
        - genuine_lead = serious buyer intent
        - spam = irrelevant/scam messages
        - If pricing negotiation is mentioned, prioritize negotiation intent
        - If customer asks for final price, cheaper rate, discount, or bargaining, ALWAYS classify as negotiation even if delivery is also mentioned

        NEGOTIATION EXAMPLES:
        - "1500 final?"
        - "Best price?"
        - "Can you reduce price?"
        - "Too expensive"
        - "Any discount?"
        - "Can you do cheaper?"
        - "2500 last price?"
        - "Give better rate"
        - "Wholesale price?"
        - "Can you do final 2000?"

        DELIVERY QUERY EXAMPLES:
        - "Can you deliver tomorrow?"
        - "Need urgent delivery"
        - "How many days delivery?"
        - "Can I get it tonight?"
        - "Fast shipping possible?"
        - "Delivery by morning?"

        PAYMENT QUERY EXAMPLES:
        - "I paid already"
        - "Advance sent"
        - "Payment done"
        - "Transferred amount"
        - "Check payment please"
        - "Sent 1000 advance"

        COMPLAINT EXAMPLES:
        - "Very bad service"
        - "Order still not received"
        - "You are not replying"
        - "Product damaged"
        - "Late delivery again"
        - "Really disappointed"

        PRODUCT INQUIRY EXAMPLES:
        - "Do you have black bags?"
        - "Available in stock?"
        - "What colors available?"
        - "Show wallet options"
        - "Price for leather bag?"

        GENUINE LEAD EXAMPLES:
        - "I want to order today"
        - "Need bulk quantity"
        - "Can buy immediately"
        - "Need 50 pieces"
        - "Interested in wholesale"

        SPAM EXAMPLES:
        - "Earn money fast"
        - "Click this link"
        - "Free crypto"
        - "Make millions now"

        IMPORTANT:
        - If customer says things like:
        "1500 final",
        "best price",
        "discount",
        "cheaper",
        "better price",
        classify as negotiation

        - Return ONLY valid JSON
        - No markdown
        - No explanation

        FORMAT:
        {{
            "intent": "negotiation",
            "confidence": 0.95
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

            match = re.search(r'\{.*\}', response, re.DOTALL)

            if match:

                clean_json = match.group()

                return json.loads(clean_json)

            else:

                raise ValueError("No valid JSON found")

        except Exception as e:

            return {

                "intent": "general",
                "confidence": 0.5,
                "error": str(e)

            }