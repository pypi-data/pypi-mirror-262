from knowt.llm import RAG
from transformers.pipelines import TextGenerationPipeline


def test_rag():
    rag = RAG(self_hosted=True)
    assert rag.db.num_dim == 384
    assert rag.db.embeddings.shape == (41531, 384)
    assert isinstance(rag.pipe, TextGenerationPipeline)
