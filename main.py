"""
Agent Formateur en Neuropédagogie
Un agent expert pour aider les formateurs à analyser leurs vidéos de formation
et améliorer leurs sessions basées sur les 4 piliers de l'apprentissage et les neurosciences.
"""

import asyncio
import mistralai.agents as agents


@agents.tool(
    name="analyser_video_formation",
    description="Analyse une vidéo de formation pour extraire les points clés, les piliers de l'apprentissage abordés, et identifier les moments d'hésitation ou de manque de clarté.",
    input_schema={
        "type": "object",
        "properties": {
            "video_url": {"type": "string", "description": "URL de la vidéo YouTube ou autre plateforme à analyser"},
            "confirmation": {"type": "boolean", "description": "Confirmation explicite du formateur pour analyser la vidéo"},
        },
        "required": ["video_url", "confirmation"],
    },
)
async def analyser_video_formation(args: dict) -> dict:
    video_url = args["video_url"]
    confirmation = args["confirmation"]
    if not confirmation:
        return {
            "erreur": "Confirmation explicite requise pour analyser la vidéo",
            "message": "Veuillez confirmer explicitement que je peux analyser cette vidéo.",
        }
    return {
        "video_url": video_url,
        "resume": "Analyse en cours... (simulation)",
        "piliers_abordes": [],
        "points_cles": [],
        "questions_apprenants": [],
        "moments_hesitation": [],
        "outils_utilises": [],
        "recommandations": [],
    }


@agents.tool(
    name="creer_quiz_memoire",
    description="Crée un quiz de 5-10 questions sur la mémoire et les neurosciences.",
    input_schema={
        "type": "object",
        "properties": {
            "theme": {"type": "string", "description": "Thème du quiz", "default": "mémoire"},
            "niveau": {"type": "string", "enum": ["debutant", "intermediaire", "avance"], "description": "Niveau de difficulté", "default": "intermediaire"},
            "nombre_questions": {"type": "integer", "minimum": 5, "maximum": 10, "description": "Nombre de questions", "default": 5},
        },
    },
)
async def creer_quiz_memoire(args: dict) -> dict:
    theme = args.get("theme", "mémoire")
    niveau = args.get("niveau", "intermediaire")
    nombre_questions = args.get("nombre_questions", 5)

    questions = []
    if theme == "mémoire":
        questions = [
            {
                "question": "Quels sont les 3 principaux types de mémoire selon les neurosciences ?",
                "reponse": "Mémoire sensorielle, mémoire à court terme, mémoire à long terme",
                "explication": "La mémoire sensorielle stocke brièvement les informations sensorielles, la mémoire à court terme les maintient temporairement, et la mémoire à long terme les stocke durablement.",
            },
            {
                "question": "Quelle zone cérébrale est principalement impliquée dans la formation de la mémoire à long terme ?",
                "reponse": "L'hippocampe",
                "explication": "L'hippocampe joue un rôle crucial dans la consolidation de l'information.",
            },
            {
                "question": "Citez 2 méthodes efficaces pour consolider la mémoire selon les neurosciences.",
                "reponse": "Répétition espacée, sommeil, pratique active, enseignement aux autres",
                "explication": "La répétition espacée et le sommeil favorisent la consolidation synaptique.",
            },
        ]
    return {
        "quiz": questions[:nombre_questions],
        "theme": theme,
        "niveau": niveau,
        "conseil": "D'après les neurosciences, variez les types de questions pour stimuler différents réseaux neuronaux.",
    }


@agents.tool(
    name="evaluer_piliers_apprentissage",
    description="Évalue quels piliers de l'apprentissage ont été abordés dans une session.",
    input_schema={
        "type": "object",
        "properties": {
            "description_session": {"type": "string", "description": "Description de la session"},
            "duree": {"type": "integer", "description": "Durée en minutes", "default": 60},
        },
        "required": ["description_session"],
    },
)
async def evaluer_piliers_apprentissage(args: dict) -> dict:
    description_session = args["description_session"]
    duree = args.get("duree", 60)

    piliers = {
        "Attention": {"present": False, "niveau": 0, "suggestions": []},
        "Engagement actif": {"present": False, "niveau": 0, "suggestions": []},
        "Retour sur erreur": {"present": False, "niveau": 0, "suggestions": []},
        "Consolidation": {"present": False, "niveau": 0, "suggestions": []},
    }
    description_lower = description_session.lower()

    if any(mot in description_lower for mot in ["accroche", "attention", "captiver"]):
        piliers["Attention"]["present"] = True
        piliers["Attention"]["niveau"] = 3
    else:
        piliers["Attention"]["suggestions"] = ["Commencez par une question interactive", "Utilisez des visuels percutants"]

    if any(mot in description_lower for mot in ["exercice", "pratique", "interactif"]):
        piliers["Engagement actif"]["present"] = True
        piliers["Engagement actif"]["niveau"] = 3
    else:
        piliers["Engagement actif"]["suggestions"] = ["Intégrez des exercices toutes les 15-20 minutes", "Utilisez Jamboard ou Mentimeter"]

    if any(mot in description_lower for mot in ["feedback", "correction", "erreur"]):
        piliers["Retour sur erreur"]["present"] = True
        piliers["Retour sur erreur"]["niveau"] = 3
    else:
        piliers["Retour sur erreur"]["suggestions"] = ["Prévoyez des moments de feedback", "Encouragez l'auto-correction"]

    if any(mot in description_lower for mot in ["resume", "synthese", "consolidation"]):
        piliers["Consolidation"]["present"] = True
        piliers["Consolidation"]["niveau"] = 3
    else:
        piliers["Consolidation"]["suggestions"] = ["Terminez par un résumé", "Envoyez un support de synthèse"]

    score = sum(1 for pilier in piliers.values() if pilier["present"])
    return {
        "piliers": piliers,
        "score": f"{score}/4",
        "recommandation": "Pour une session optimale, assurez-vous d'aborder les 4 piliers.",
    }


@agents.tool(
    name="conseiller_outils_interactifs",
    description="Recommande des outils interactifs pour une formation.",
    input_schema={
        "type": "object",
        "properties": {
            "type_formation": {"type": "string", "description": "Type de formation", "default": "en ligne"},
            "taille_groupe": {"type": "integer", "description": "Nombre de participants", "default": 10},
            "objectifs": {"type": "string", "description": "Objectifs pédagogiques", "default": ""},
        },
    },
)
async def conseiller_outils_interactifs(args: dict) -> dict:
    type_formation = args.get("type_formation", "en ligne")
    taille_groupe = args.get("taille_groupe", 10)
    objectifs = args.get("objectifs", "")

    outils = []
    if taille_groupe <= 20:
        outils.extend(
            [
                {"nom": "Jamboard", "utilisation": "Tableau blanc collaboratif", "avantages": "Intuitif, temps réel", "neurosciences": "Stimule la créativité"},
                {"nom": "Miro", "utilisation": "Tableau blanc avancé", "avantages": "Templates prêts", "neurosciences": "Favorise la visualisation"},
            ]
        )
    outils.extend(
        [
            {"nom": "MindMeister", "utilisation": "Cartes mentales", "avantages": "Structure visuelle", "neurosciences": "Active la mémoire associative"},
            {"nom": "Kahoot!", "utilisation": "Quiz interactifs", "avantages": "Ludique, engagement élevé", "neurosciences": "Renforce la mémoire"},
            {"nom": "Mentimeter", "utilisation": "Sondages en temps réel", "avantages": "Simple, visuel", "neurosciences": "Stimule la participation"},
        ]
    )
    if type_formation in ["en ligne", "hybride"]:
        outils.extend(
            [
                {"nom": "Zoom", "utilisation": "Breakout rooms", "avantages": "Interaction en petits groupes", "neurosciences": "Favorise l'apprentissage social"},
                {"nom": "Gather.town", "utilisation": "Espace virtuel", "avantages": "Expérience immersive", "neurosciences": "Environnement riche"},
            ]
        )
    outils.append({"nom": "OpenDoo", "utilisation": "Gestion de projet", "avantages": "Suivi des tâches", "neurosciences": "Renforce la consolidation"})
    return {"outils": outils, "recommandation": "Choisissez 2-3 outils maximum pour éviter la surcharge cognitive."}


harness = agents.Harness(
    tools=[analyser_video_formation, creer_quiz_memoire, evaluer_piliers_apprentissage, conseiller_outils_interactifs],
    name="agent-formateur-neuropedagogie",
    description="Agent expert en neuropédagogie",
)

INSTRUCTIONS = """
Tu es **Agent-Formateur-NeuroPedagogie**, un assistant expert en neuropédagogie.
**Ton rôle** : Aider les formateurs à analyser leurs vidéos et améliorer leurs sessions via les 4 piliers de l'apprentissage.
**Règles** : 1. NE JAMAIS analyser une vidéo sans confirmation EXPLICITE. 2. NE JAMAIS inventer. 3. TOUJOURS citer tes sources.
**Style** : Professionnel, pédagogique, engageant.
"""

agent = agents.Agent(
    name="agent-formateur-neuropedagogie",
    description="Agent expert en neuropédagogie pour analyser les vidéos de formation et améliorer les sessions.",
    instructions=INSTRUCTIONS,
    harness=harness,
    model="mistral-large-latest",
    loop_policy=agents.LoopPolicy.max_turns(10),
)


def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        print(f"Agent: {agent.name}")
        print(f"Description: {agent.description}")
        print(f"Model: {agent.model}")
        print(f"Tools: {[tool.name for tool in agent.harness.tools]}")
        return

    async def run():
        async with agent.create_session() as session:
            print("\n🧠 Agent Formateur en Neuropédagogie\n" + "=" * 60)
            print(
                "Bonjour ! Je peux analyser tes vidéos et améliorer tes sessions.\n"
                "Exemples:\n"
                "  - 'Analyse ma vidéo : [URL]'\n"
                "  - 'Crée un quiz sur la mémoire'\n"
                "  - 'Quels outils utiliser ?'"
            )
            while True:
                try:
                    user_input = input("\nToi: ")
                    if user_input.lower() in ["quit", "exit", "au revoir"]:
                        print("\nAu revoir ! 👋")
                        break
                    if not user_input.strip():
                        continue
                    print("\nAgent: ", end="", flush=True)
                    async for chunk in session.run_turn(user_input):
                        print(
                            (hasattr(chunk, "text") and chunk.text)
                            or (hasattr(chunk, "content") and chunk.content)
                            or "",
                            end="",
                            flush=True,
                        )
                    print()
                except (KeyboardInterrupt, EOFError):
                    break

    asyncio.run(run())


if __name__ == "__main__":
    main()
