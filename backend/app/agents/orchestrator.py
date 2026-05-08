from app.agents.intent_classifier import IntentClassifier
from app.agents.reply_generator import ReplyGenerator
from app.agents.entity_extractor import EntityExtractor
from app.agents.lead_scorer import LeadScorer
from app.agents.handoff_decider import HandoffDecider


class Orchestrator:

    def __init__(self):

        self.intent_agent = IntentClassifier()

        self.reply_agent = ReplyGenerator()

        self.entity_agent = EntityExtractor()

        self.lead_agent = LeadScorer()

        self.handoff_agent = HandoffDecider()

    async def process_message(

        self,
        message,
        conversation_history=None,
        business_context=None

    ):

        if conversation_history is None:
            conversation_history = []

        if business_context is None:
            business_context = {}

        try:

            # STEP 1 — INTENT CLASSIFICATION

            intent_result = await self.intent_agent.classify(
                message
            )

            intent = intent_result.get("intent")

            # STEP 2 — REPLY GENERATION

            reply_result = await self.reply_agent.generate_reply(

                message=message,

                intent=intent,

                conversation_history=conversation_history,

                business_context=business_context

            )

            # STEP 3 — ENTITY EXTRACTION

            entities = await self.entity_agent.extract_entities(

                message=message,

                conversation_history=conversation_history

            )

            # STEP 4 — LEAD SCORING

            lead_result = self.lead_agent.score_lead(

                intent=intent,

                entities=entities,

                message=message

            )

            # STEP 5 — HANDOFF DECISION

            handoff_result = self.handoff_agent.decide_handoff(

                intent=intent,

                lead_score=lead_result["lead_score"],

                entities=entities,

                message=message

            )

            # FINAL RESPONSE

            return {

                "intent": intent_result,

                "reply": reply_result,

                "entities": entities,

                "lead_analysis": lead_result,

                "handoff": handoff_result

            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }