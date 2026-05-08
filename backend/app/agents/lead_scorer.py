class LeadScorer:

    def score_lead(

        self,
        intent,
        entities,
        message

    ):

        score = 0

        reasons = []

        message = message.lower()

        # INTENT-BASED SCORING

        if intent == "negotiation":

            score += 3
            reasons.append("Negotiating price")

        elif intent == "payment_query":

            score += 4
            reasons.append("Payment discussion")

        elif intent == "product_inquiry":

            score += 2
            reasons.append("Interested in product")

        elif intent == "delivery_query":

            score += 2
            reasons.append("Asked delivery timeline")

        # ENTITY-BASED SCORING

        if entities.get("advance_amount"):

            score += 4
            reasons.append("Advance payment mentioned")

        if entities.get("negotiated_price"):

            score += 3
            reasons.append("Negotiated pricing")

        if entities.get("urgency") == "high":

            score += 2
            reasons.append("Urgent requirement")

        if entities.get("payment_done"):

            score += 5
            reasons.append("Payment completed")

        # MESSAGE SIGNALS

        strong_buying_words = [

            "final",
            "confirm",
            "book",
            "available",
            "urgent",
            "delivery",
            "pay",
            "advance"

        ]

        for word in strong_buying_words:

            if word in message:

                score += 1

        # PRIORITY LEVEL

        if score >= 10:

            priority = "very_high"

        elif score >= 7:

            priority = "high"

        elif score >= 4:

            priority = "medium"

        else:

            priority = "low"

        return {

            "lead_score": score,
            "priority": priority,
            "reasons": reasons

        }