
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


BREAKFAST_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Role:
            You are a knowledgeable nutrition and meal-planning assistant.

            Task:
            Generate exactly five healthy breakfast ideas based on the
            user's dietary preference, cuisine, and health priority.

            Context:
            - Prefer balanced meals with nutritious ingredients.
            - Include whole grains, vegetables, and suitable protein sources.
            - Prefer simple, practical recipes.
            - Avoid excessive added sugar and deep-fried foods.
            - Respect the user's selected dietary preference.
            - Do not claim that a meal treats or cures a disease.

            Few-shot format examples:
            1. Vegetable oats upma — Oats, vegetables, and peanuts
               provide fiber and plant-based protein.
            2. Idli with sambar — A traditional breakfast combining
               steamed rice cakes with lentil-based soup.
            3. Vegetable pesarattu — A green gram dosa with vegetables.
            4. Ragi dosa with sambar — A millet-based breakfast served
               with lentil soup.
            5. Vegetable poha — Flattened rice cooked with vegetables
               and roasted peanuts.

            Response format:
            Return exactly five numbered ideas.
            Each idea must have a short title and a concise description.
            Use this format:
            1. **Breakfast title** — Short description.
            Do not include an introduction or conclusion.
            Generate ideas appropriate to the user's preferences rather
            than automatically copying the examples.
            """
        ),
        (
            "human",
            """
            Dietary preference: {diet}
            Cuisine: {cuisine}
            Health priority: {priority}

            Generate exactly five suitable breakfast ideas.
            """
        ),
    ]
)

def stream_breakfast_ideas(
    api_key: str,
    diet: str,
    cuisine: str,
    priority: str,
):
    """Stream breakfast ideas from OpenAI through LangChain."""

    if not api_key or not api_key.strip():
        raise ValueError("Please provide your OpenAI API key.")

    if not diet or not cuisine or not priority:
        raise ValueError("Please select all breakfast preferences.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key.strip(),
        temperature=0.7,
        streaming=True,
    )

    chain = BREAKFAST_PROMPT | llm

    for chunk in chain.stream(
        {
            "diet": diet,
            "cuisine": cuisine,
            "priority": priority,
        }
    ):
        if isinstance(chunk.content, str) and chunk.content:
            yield chunk.content

