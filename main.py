import asyncio
from pydantic import BaseModel
import mistralai.agents as agents

class AnalyseVideoInput(BaseModel):
    video_url: str
    confirmation: bool = False

@agents.tool(
    name="analyser_video",
    description="Analyse une vidéo de formation",
    input_schema=AnalyseVideoInput,
)
async def analyser_video(args: AnalyseVideoInput) -> dict:
    if not args.confirmation:
        return {"erreur": "Confirmation explicite requise"}
    return {
        "resume": "Analyse terminée",
        "piliers": ["Attention", "Engagement actif", "Retour sur erreur", "Consolidation"],
        "conseils": ["Utilisez des accroches émotionnelles", "Intégrez des exercices pratiques"]
    }

agent = agents.Agent(
    model="mistral-large-latest",
    name="agent-formateur-neuropedagogie",
    instructions="Tu es un expert en neuropédagogie. Analyse les vidéos de formation et propose des améliorations basées sur les 4 piliers de l'apprentissage.",
    tools=[analyser_video],
)

async def main() -> None:
    async with agent.create_session() as session:
        while True:
            user_input = input("Vous: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            async for chunk in session.run_turn(user_input):
                print(chunk.text, end="", flush=True)
            print()

if __name__ == "__main__":
    asyncio.run(main())