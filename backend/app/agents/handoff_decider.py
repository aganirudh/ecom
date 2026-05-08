class HandoffDecider:

    def decide_handoff(

        self,
        intent,
        lead_score,
        entities,
        message

    ):

        reasons = []

        handoff = False

        message = message.lower()

        # HIGH LEAD SCORE

        if lead_score >= 7:

            handoff = True
            reasons.append("High-value lead detected")

        # NEGOTIATION

        if intent == "negotiation":

            handoff = True
            reasons.append("Customer negotiating price")

        # COMPLAINTS

        if intent == "complaint":

            handoff = True
            reasons.append("Customer complaint detected")

        # HIGH URGENCY

        if entities.get("urgency") == "high":

            handoff = True
            reasons.append("Urgent delivery/request")

        # PAYMENT DISCUSSION

        if entities.get("payment_done"):

            handoff = True
            reasons.append("Payment-related conversation")

        # CUSTOM REQUESTS

        custom_keywords = [

            "custom",
            "special",
            "personalized",
            "bulk order",
            "wholesale"

        ]

        for word in custom_keywords:

            if word in message:

                handoff = True
                reasons.append("Custom order request")
                break

        # ANGRY CUSTOMER SIGNALS

        angry_keywords = [

            "refund",
            "bad",
            "worst",
            "angry",
            "late",
            "complaint"

        ]

        for word in angry_keywords:

            if word in message:

                handoff = True
                reasons.append("Negative customer sentiment")
                break

        return {

            "handoff": handoff,
            "reasons": reasons

        }