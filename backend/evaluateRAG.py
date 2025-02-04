
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import SingleTurnSample
import os
from ragas.metrics import Faithfulness,LLMContextPrecisionWithoutReference,ResponseRelevancy


async def evalute_rag_ragas(Rag_Data,llm,embeddings):
    
    evaluator_llm = LangchainLLMWrapper(llm)
    evaluator_embeddings=LangchainEmbeddingsWrapper(embeddings)
    sample = SingleTurnSample(
        user_input=Rag_Data["query"],
        response=Rag_Data["response"],
        retrieved_contexts=[
            Rag_Data["relevant_docs"]
        ]
    )

    scorer = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
    relevancy=await scorer.single_turn_ascore(sample)
    print(relevancy)
 
    
    print(Rag_Data)
    dataset=[{
            "user_input":Rag_Data["query"],
            "retrieved_contexts":[Rag_Data["relevant_docs"]],
            "response":Rag_Data["response"]
           
        }]
    print(dataset)
    evaluation_dataset = EvaluationDataset.from_list(dataset)
    result = evaluate(dataset=evaluation_dataset,metrics=[Faithfulness(),LLMContextPrecisionWithoutReference()],llm=evaluator_llm)
    print(result)
    eval_result={
        "relevancy":relevancy,
        "Faithfulness":result["faithfulness"],
        "LLM Context Precision":result["llm_context_precision_without_reference"]
    }
    return eval_result