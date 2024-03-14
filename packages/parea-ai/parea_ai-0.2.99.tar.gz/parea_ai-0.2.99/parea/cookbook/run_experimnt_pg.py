import os
import uuid

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

from parea import Parea, trace
from parea.evals.general import answer_matches_target_llm_grader_factory
from parea.schemas import Completion, LLMInputs, Message, ModelParams, Role

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name='pg-essay')


def make_expr_name(name: str) -> str:
    # remove spaces, special characters, periods and make lowercase
    clean_name = name.replace(" ", "-").replace(".", "-").lower()
    return f"{clean_name}-{str(uuid.uuid4())[:2]}"


def call_llm(content: str, model: str) -> str:
    return p.completion(
        data=Completion(
            llm_configuration=LLMInputs(
                model=model,
                model_params=ModelParams(temp=0.0),
                messages=[Message(role=Role.user, content=content)],
            )
        )
    ).content


paul_graham_essay = SimpleDirectoryReader("data/pg-essay").load_data()
matches_target = answer_matches_target_llm_grader_factory(model="gpt-4-32k-0613")


def factory(model: str) -> callable:
    @trace(eval_funcs=[matches_target])
    def summarize_paul_graham_essay(context: str, question: str) -> str:
        content = f"""
        Review the following document:\n{context}
        \nAnswer the following question:{question}
        \n\nResponse:
        """
        return call_llm(content, model)

    return summarize_paul_graham_essay


def run():
    for model in ["gpt-4-32k-0613", "claude-2.1", "gemini-pro"]:
        p.experiment(
            data=[
                {
                    "context": paul_graham_essay[0].text,
                    "question": "What company did Paul leave after returning to painting",
                    "target": "Yahoo",
                }
            ],
            func=factory(model),
        ).run(name=make_expr_name(model))


if __name__ == "__main__":
    run()
