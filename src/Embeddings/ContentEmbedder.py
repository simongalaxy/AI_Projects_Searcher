from typing import List, Dict, Any
from transformers import AutoTokenizer
from fastembed import TextEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.Utils.Logger import Logger
from src.Utils.Settings import Settings

class FastEmbedPipeline:
    def __init__(self, logger:Logger):
        self.logger = logger
        self.embedding_model = Settings.get("embedding_model", model_name)
        
        # 1. Initialize the Hugging Face AutoTokenizer for token counting
        # fastembed uses the same underlying Hugging Face repos for its vocabulary mapping
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # 2. Initialize the fastembed model for vector generation
        self.embed_model = TextEmbedding(model_name=self.embedding_model)
        
        # 3. Define the strict ceiling for the chosen embedding model
        self.max_token_limit = 512 

        # 4. Initialize the RecursiveCharacterTextSplitter for fallback chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=0,
            separators=["\n\n", "\n", " ", ""]
            )
        self.logger.info("DocumentGenerator initialized with RecursiveCharacterTextSplitter.")
    

    def count_tokens(self, text: str) -> int:
        """Returns the exact number of tokens for a given string."""
        inputs = self.tokenizer(text, add_special_tokens=False)
        return len(inputs["input_ids"])


    def recursive_token_splitter(self, text: str, max_tokens: int = 400, overlap_tokens: int = 50) -> List[str]:
        """
        A native token-aware character/word recursive splitter.
        Keeps chunks safely below the embedding model's context window.
        """
        # Split text into rough paragraph chunks first to preserve sentence structures
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            # If a single paragraph is too large, break it down by sentences
            if para_tokens > max_tokens:
                sentences = para.replace(". ", ".\n").split("\n")
                for sentence in sentences:
                    sentence_tokens = self.count_tokens(sentence)
                    if current_tokens + sentence_tokens > max_tokens:
                        if current_chunk:
                            chunks.append(" ".join(current_chunk))
                        current_chunk = [sentence]
                        current_tokens = sentence_tokens
                    else:
                        current_chunk.append(sentence)
                        current_tokens += sentence_tokens
            # If adding paragraph exceeds the limit, flush the current chunk
            elif current_tokens + para_tokens > max_tokens:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_tokens = para_tokens
            else:
                current_chunk.append(para)
                current_tokens += para_tokens

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks


    def process_and_embed(self, text: str) -> Dict[str, Any]:
        """Evaluates token size, chunks if necessary, and extracts fastembed embeddings."""
        total_tokens = self.count_tokens(text)
        
        # Define a safe chunk threshold (e.g., 400 tokens) to leave room for special tokens 
        # like [CLS] and [SEP] added by the model architecture.
        safe_threshold = 400 
        
        if total_tokens > safe_threshold:
            print(f"⚠️ Text size ({total_tokens} tokens) exceeds safe threshold ({safe_threshold}). Chunking text...")
            chunks = self.recursive_token_splitter(text, max_tokens=safe_threshold)
        else:
            print(f"✅ Text size ({total_tokens} tokens) is safe for single-pass embedding.")
            chunks = [text]

        # Generate vectors using fastembed
        # fastembed returns a generator, we cast to list to resolve the arrays
        embeddings = list(self.embed_model.embed(chunks))
        
        return {
            "original_token_count": total_tokens,
            "was_chunked": total_tokens > safe_threshold,
            "num_chunks": len(chunks),
            "chunks": chunks,
            "embeddings": embeddings
        }

# ==========================================
# Example Execution
# ==========================================
if __name__ == "__main__":
    pipeline = FastEmbedPipeline()

    # Long example text simulation
    sample_press_release = (
        "Breaking News. " * 150 + 
        "\n\n" + 
        "Second Paragraph Details. " * 100
    )

    result = pipeline.process_and_embed(sample_press_release)
    
    print(f"\nResults Summary:")
    print(f"- Total Raw Tokens: {result['original_token_count']}")
    print(f"- Split Required: {result['was_chunked']}")
    print(f"- Generated Chunks: {result['num_chunks']}")
    print(f"- Embedding Vector Length (per chunk): {len(result['embeddings'][0])}")
