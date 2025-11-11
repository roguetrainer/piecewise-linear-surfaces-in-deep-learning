# In How Many Dimensions Does a Foundation LLM Live?

## The Short Answer

A foundation LLM lives in **multiple overlapping dimensional spaces simultaneously**, depending on which aspect you're examining. The answer ranges from:

- **~50,000 - 100,000 dimensions** (vocabulary/token embedding space)
- **Thousands to tens of thousands of dimensions** (hidden representation space)
- **Billions to trillions of parameters** (total parameter space)
- **Hundreds of thousands to millions of tokens** (context/sequence space)

Let's unpack what each of these means.

---

## Parameter Counts: The Scale of Modern LLMs

Based on current 2024-2025 data, here are typical parameter counts for foundation models:

### Small Models (7B - 13B parameters)
- **LLaMA 2/3 7B**: 7 billion parameters
- **LLaMA 2/3 13B**: 13 billion parameters
- **Mistral 7B**: 7 billion parameters
- **Phi-3 Small**: ~7 billion parameters

### Medium Models (30B - 70B parameters)
- **LLaMA 2/3 70B**: 70 billion parameters
- **Mixtral 8x7B**: 47 billion total parameters (MoE architecture)
- **Qwen**: Various sizes up to 72B

### Large Models (100B - 500B parameters)
- **GPT-4**: Estimated ~1 trillion parameters (OpenAI hasn't disclosed exact count)
- **LLaMA 3.1 405B**: 405 billion parameters (largest publicly available open model)
- **Claude (Anthropic)**: Parameter count not disclosed, estimated in hundreds of billions
- **Gemini**: Estimated in hundreds of billions
- **DeepSeek-V3**: 671 billion total parameters (MoE with 37B active)

### Mixture-of-Experts (MoE) Models
- **LLaMA 4 Behemoth**: ~2 trillion total parameters (in development)
- **DeepSeek-V3**: 671B total, 37B active per token
- **Mixtral**: Multiple expert models activated selectively

**Key Insight**: "Parameter count" refers to the total number of learnable weights in the network, not the dimensionality of any single space.

---

## The Multiple Dimensions of an LLM

### 1. Vocabulary/Token Embedding Dimension (Input Space)

**Dimension: ~50,000 - 100,000+**

This is the **first** dimensional space an LLM encounters:

| Model | Vocabulary Size | Initial Dimension |
|-------|----------------|-------------------|
| GPT-2/GPT-3 | 50,257 | 50,257 |
| GPT-4 | ~100,000 | ~100,000 |
| Claude | ~100,000 | ~100,000 |
| LLaMA | 32,000 | 32,000 |
| Mistral | ~32,000 | ~32,000 |

**How it works:**
- Each token in the vocabulary gets a unique ID (0 to V-1, where V is vocabulary size)
- Initially, each token is represented as a **one-hot vector** in V-dimensional space
- The first layer (embedding layer) projects this into a dense representation

**Example:**
```
Token "hello" → [0, 0, 0, ..., 1, ..., 0, 0]  (50,000-dimensional one-hot)
                      ↓ embedding layer
                 [0.23, -0.45, 0.67, ..., 0.12]  (d-dimensional dense)
```

### 2. Hidden Representation Dimension (Model Space)

**Dimension: 768 - 18,432 (typical range)**

This is the **primary working space** where the LLM does most of its computation:

| Model | Hidden Dimension (d_model) |
|-------|---------------------------|
| GPT-2 Small | 768 |
| GPT-2 Medium | 1,024 |
| GPT-2 Large | 1,280 |
| GPT-3 | 12,288 |
| LLaMA 7B | 4,096 |
| LLaMA 13B | 5,120 |
| LLaMA 70B | 8,192 |
| GPT-4 | Estimated ~18,000-20,000 |
| Claude | Estimated ~12,000-16,000 |

**This is where the "origami" happens!**
- Every token, at every layer, is represented as a vector in this d-dimensional space
- Each transformer layer "folds" this space through attention and feed-forward operations
- The model learns to position similar concepts close together in this space

**Example:**
For LLaMA 70B with d=8,192:
- Each token → 8,192-dimensional vector
- Each of 80 layers transforms this 8,192-dimensional space
- Total: 80 × 8,192 dimensional transformations

### 3. Attention Head Dimension (Per-Head Space)

**Dimension: 64 - 256 (per head)**

Each attention head operates in a **lower-dimensional subspace**:

| Model | Num Heads | Head Dimension |
|-------|-----------|----------------|
| GPT-2 | 12-96 | 64 |
| GPT-3 | 96 | 128 |
| LLaMA 70B | 64 | 128 |

**Formula**: `head_dimension = hidden_dimension / num_heads`

**Why this matters:**
- Different heads can specialize in different types of relationships
- Each head learns to "fold" its subspace differently
- Together, they create a rich multi-faceted representation

### 4. Feed-Forward Intermediate Dimension

**Dimension: 3,072 - 73,728**

The feed-forward layers temporarily **expand** into a higher-dimensional space:

| Model | FFN Intermediate Dimension |
|-------|---------------------------|
| GPT-2 | 3,072 |
| GPT-3 | 49,152 |
| LLaMA 70B | 28,672 |
| GPT-4 | Estimated ~73,000 |

**Formula**: Typically `4 × hidden_dimension` or `8 × hidden_dimension`

**This is critical for capacity:**
- The FFN expands into high-dimensional space
- Applies ReLU (creating our "origami folds")
- Projects back down to hidden dimension
- This expansion gives the model room to compute complex transformations

### 5. Context Window (Sequence Dimension)

**Dimension: 2,048 - 2,000,000+ tokens**

This is the **temporal/sequential dimension**:

| Model | Context Window (tokens) |
|-------|------------------------|
| GPT-3 | 2,048 |
| GPT-4 | 128,000 |
| Claude 3 | 200,000 |
| Claude 3.5 | 200,000 |
| Gemini 1.5 | 1,000,000 |
| Claude (extended) | 2,000,000 |
| LLaMA 3.1 | 128,000 |
| LLaMA 4 Scout | 10,000,000 |

**How to think about it:**
- The model processes a **sequence** of tokens
- Each position in the sequence is a separate "slot"
- The attention mechanism lets positions "talk to" each other
- Longer context = more positions to attend to

### 6. Parameter Space (Weight Space)

**Dimension: Billions to Trillions**

This is the **total number of learnable parameters**:

The parameter count includes:
- **Embedding matrices**: vocab_size × hidden_dim
- **Attention weights**: Multiple projection matrices per layer
- **Feed-forward weights**: Two large matrices per layer
- **Layer norms**: Small parameter count
- **Output projection**: hidden_dim × vocab_size

**Approximate breakdown for LLaMA 70B:**
```
Embeddings:        32,000 × 8,192 = 262M parameters
80 layers × (
  Attention:       8,192 × 8,192 × 4 = 268M per layer × 80 = 21.5B
  FFN:             8,192 × 28,672 × 2 = 470M per layer × 80 = 37.6B
  Layer norms:     ~1M per layer × 80 = 80M
)
Output head:       8,192 × 32,000 = 262M
Total:             ~70B parameters
```

---

## Visualizing the Dimensional Hierarchy

```
Input Token: "quantum"
     ↓
[One-hot: 100,000 dimensions] ← Vocabulary space
     ↓ Embedding layer
[Dense vector: 8,192 dimensions] ← Primary representation space
     ↓ Layer 1
[Attention: 64 heads × 128 dims each] ← Multi-head subspaces
[FFN: expand to 28,672 dims, then back] ← Temporary expansion
     ↓ Layer 2
[Attention: 64 heads × 128 dims each]
[FFN: expand to 28,672 dims, then back]
     ↓ ... (80 layers total)
     ↓ Layer 80
[Dense vector: 8,192 dimensions]
     ↓ Output projection
[Logits: 100,000 dimensions] ← Probability over vocabulary
     ↓ Softmax
Next token prediction
```

---

## The Geometry of LLM Space

### Linear Subspaces and Manifolds

Despite having thousands of dimensions, LLMs learn to use **lower-dimensional manifolds**:

1. **Semantic subspaces**: Related concepts cluster together
   - "king" - "man" + "woman" ≈ "queen" (the famous word2vec example)
   - This happens in the d-dimensional hidden space

2. **Syntactic subspaces**: Grammatical relationships form patterns
   - Singular/plural relationships
   - Verb tenses
   - Part-of-speech groupings

3. **Task-specific subspaces**: Different capabilities use different regions
   - Coding knowledge
   - Mathematical reasoning
   - Factual knowledge
   - Creative writing

### The Origami Perspective

Remember our origami analogy? Here's how it applies:

**Each layer performs origami in d-dimensional space:**
1. **Attention mechanism**: Mixes information across positions (folding along different axes)
2. **Feed-forward network**: Expands to higher dimension, applies ReLU (creates folds), projects back
3. **Residual connections**: Preserve information from previous layers (like keeping the original paper visible)

**With 70-80 layers:**
- That's 70-80 successive origami operations
- Each fold creates piecewise linear regions
- The number of possible regions grows exponentially: up to 2^(num_neurons)

---

## Memory and Computation Requirements

### Memory Footprint by Precision

For a 70B parameter model:

| Precision | Bytes per Parameter | Total Memory |
|-----------|-------------------|--------------|
| FP32 (32-bit) | 4 bytes | 280 GB |
| FP16 (16-bit) | 2 bytes | 140 GB |
| INT8 (8-bit) | 1 byte | 70 GB |
| INT4 (4-bit) | 0.5 bytes | 35 GB |

**Additional memory needed:**
- **Activations**: Batch_size × Sequence_length × Hidden_dim × Num_layers
- **Optimizer states**: 2-3× parameter memory (for Adam optimizer)
- **Gradients**: Same as parameters (during training)

**Training a 70B model requires:**
- ~1-2 TB of GPU memory
- Multiple high-end GPUs (e.g., 8× A100 80GB GPUs)
- ~15 trillion tokens of training data

### Computational Complexity

For a forward pass with sequence length S and model dimension d:

**Attention complexity**: O(S² × d)
- Why: Each of S positions attends to S other positions
- Each attention requires d-dimensional operations

**Feed-forward complexity**: O(S × d × FFN_dim)
- Why: Each of S positions goes through FFN
- FFN has dimension ~4d

**Total per layer**: O(S² × d + S × d²)

**For GPT-4 (estimated 80 layers, d≈18,000, S=128,000):**
- Attention: ~2.5 × 10^14 operations
- FFN: ~1.6 × 10^14 operations
- Total per token: ~10^14 operations
- **That's 100 trillion operations per token!**

---

## Comparing Model Scales

### Small vs Large: What Changes?

| Aspect | Small (7B) | Large (70B) | Giant (1T+) |
|--------|------------|-------------|-------------|
| Hidden dimension | 4,096 | 8,192 | ~20,000 |
| Num layers | 32 | 80 | ~100 |
| Num heads | 32 | 64 | ~128 |
| FFN dimension | 11,008 | 28,672 | ~80,000 |
| Context window | 2,048 | 128,000 | 128,000+ |
| Training data | ~1T tokens | ~2T tokens | ~10T+ tokens |
| Training GPUs | 512 | 16,000 | 100,000+ |
| Training time | Weeks | Months | Months |
| Inference cost/token | $0.0001 | $0.001 | $0.01 |

### Scaling Laws

**Kaplan et al. (2020) and Chinchilla (2022) showed:**
- Performance scales as a power law with:
  - Model size (parameters)
  - Dataset size (tokens)
  - Compute budget (FLOPs)

**Optimal scaling:** ~20 tokens per parameter
- 70B model → ~1.4T training tokens
- 1T model → ~20T training tokens

---

## Practical Implications

### 1. Why More Dimensions = More Capability

**Higher hidden dimension d allows:**
- More complex representations
- Better separation of concepts
- Richer feature interactions
- Greater "origami" complexity (more folds in higher-dimensional space)

**But with diminishing returns:**
- 768 → 4,096: Huge improvement
- 4,096 → 8,192: Significant improvement
- 8,192 → 16,384: Moderate improvement
- 16,384 → 32,768: Smaller improvement

### 2. The Curse and Blessing of Dimensionality

**Curse:**
- Computational cost grows as O(d²)
- Memory grows as O(d × parameters)
- Harder to train (optimization in high dimensions)

**Blessing:**
- More room to separate concepts
- Can represent more complex functions
- Better generalization (paradoxically!)

### 3. Compression and Distillation

**Observation**: Large models can often be compressed dramatically
- 70B → 7B with 90% of performance
- 1T → 70B with 85% of performance

**Why?**
- Large models learn redundant representations
- Knowledge is distributed across many dimensions
- Smaller models can capture the "essential" structure
- Like compressing a high-resolution image

---

## The Fundamental Question Answered

### So, How Many Dimensions?

The most meaningful answer is the **hidden dimension d**:

- **GPT-4**: ~18,000-20,000 dimensions
- **Claude 3**: ~12,000-16,000 dimensions
- **LLaMA 70B**: 8,192 dimensions
- **LLaMA 7B**: 4,096 dimensions

**This is where the model "thinks"** - where it:
- Represents concepts
- Performs reasoning
- Stores knowledge
- Generates responses

### But the Complete Answer is Multi-Scale

1. **Token level**: ~100,000 dimensions (vocabulary)
2. **Representation level**: ~8,000-20,000 dimensions (hidden space)
3. **Sub-representation level**: ~64-128 dimensions (per attention head)
4. **Expansion level**: ~30,000-80,000 dimensions (FFN intermediate)
5. **Sequence level**: ~100,000-10,000,000 dimensions (context window)
6. **Parameter level**: ~7,000,000,000-2,000,000,000,000 dimensions (weight space)

**The LLM inhabits ALL of these spaces simultaneously, at different scales!**

---

## Philosophical Implications

### Is Intelligence Dimensional?

The fact that we can create intelligence-like behavior in ~10,000-20,000 dimensional spaces raises fascinating questions:

1. **Is human thought lower-dimensional than we think?**
   - The human brain has ~86 billion neurons
   - But perhaps thinking happens in an effective space of ~10,000 dimensions?
   - Different neural populations might serve as "dimensions"

2. **Is there a minimum dimensionality for intelligence?**
   - Small models (1,000 dims) can do pattern matching
   - Medium models (4,000 dims) can do reasoning
   - Large models (20,000 dims) can do complex reasoning
   - Is there a threshold?

3. **Why does high-dimensional origami work so well?**
   - Piecewise linear functions in high dimensions
   - Can approximate any function
   - Natural for gradient-based learning
   - Efficient to compute

### The Geometry of Meaning

**Meanings emerge from geometry:**
- Concepts are regions in d-dimensional space
- Analogies are parallel vectors
- Reasoning is path-following through the space
- Understanding is finding the right subspace

**This suggests:**
- Meaning itself might be fundamentally geometric
- Intelligence might be navigation in high-dimensional space
- Learning is discovering the right dimensional structure

---

## Conclusion

A foundation LLM lives in **a hierarchy of dimensional spaces**, with the most important being:

**Primary workspace**: 8,000-20,000 dimensions (hidden representation)
- This is where concepts live
- Where reasoning happens
- Where knowledge is encoded

**With extensions into**:
- Vocabulary space (~100,000 dims)
- Attention subspaces (64-128 dims × many heads)
- Temporary expansion spaces (30,000-80,000 dims)
- Sequential space (100k-10M positions)
- Parameter space (billions to trillions)

The remarkable insight is that intelligence-like behavior emerges from:
1. **Strategic folding** of these high-dimensional spaces
2. **Learned geometry** that captures meaning
3. **Compositional structure** across many layers
4. **Attention mechanisms** that mix information

Modern LLMs are performing **elaborate origami in ~10,000-20,000 dimensional space**, with each of 70-100 layers creating new folds that separate concepts and enable reasoning.

The question "how many dimensions?" has no single answer - but understanding the dimensional hierarchy helps us grasp what these models really are: **geometric engines that transform high-dimensional representations through learned, piecewise-linear operations**.

---

## References

### Parameter Counts and Architecture Details
- Meta AI (2024). "LLaMA 3.1: Herd of Models"
- OpenAI (2023). "GPT-4 Technical Report"
- Anthropic (2024). "Claude 3 Model Card"
- Google DeepMind (2024). "Gemini 1.5: Unlocking Multimodal Understanding"

### Scaling Laws
- Kaplan et al. (2020). "Scaling Laws for Neural Language Models"
- Hoffmann et al. (2022). "Training Compute-Optimal Large Language Models" (Chinchilla)

### Architecture and Geometry
- Vaswani et al. (2017). "Attention Is All You Need"
- Elhage et al. (2021). "A Mathematical Framework for Transformer Circuits"
- Olah et al. (2018). "The Building Blocks of Interpretability"
