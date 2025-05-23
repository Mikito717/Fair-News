import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

liberal_prompt = """あなたはリベラル（進歩主義的）な視点を持つ評論家です。個人の権利、社会的公正、環境保護、多様性の重要性を重視します。保守的な権力構造や国家主義的な論調には懐疑的です。以下のニュースに対して、リベラル的視点から見て、その内容がいかに公平であるか、または偏っているかを論じてください。"""
conservative_prompt = """あなたは保守的な視点を持つ評論家です。伝統、国家、家族の価値を重視し、個人の自由と責任を強調します。リベラルな政策や国家介入には懐疑的です。以下のニュースに対して、保守的視点から見て、その内容がいかに公平であるか、または偏っているかを論じてください。"""
neutral_prompt = """あなたは中立かつ事実ベースの立場から、ニュースの内容の正確性や信頼性を評価するファクトチェッカーです。事実、出典、論理性に基づいてこのニュースがどれだけ客観的かを評価してください。感情的・扇動的な表現についても指摘してください。"""

agent_prompts = {
    "liberal": liberal_prompt,
    "conservative": conservative_prompt,
    "neutral": neutral_prompt
}

def load_model_and_tokenizer(model_id="microsoft/Phi-4-mini-instruct"):
    """
    モデルとトークナイザーを初期化して返す
    """
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        attn_implementation="flash_attention_2"
    )
    model = torch.compile(model).eval()
    return model, tokenizer

# モジュールインポート時に自動で初期化
model, tokenizer = load_model_and_tokenizer()

def generate_response(agent, prompt, model=model, tokenizer=tokenizer):
    """
    指定したエージェントプロンプトと記事でレスポンスを生成
    """
    messages = (
        "<|im_start|>system\n"
        f"You are a helpful assistant. You have to answer the question in Japanese.\n{agent_prompts[agent]}"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt}"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    inputs = tokenizer(messages, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        generation = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
        output_ids = generation[0][input_len:]
    decoded = tokenizer.decode(output_ids, skip_special_tokens=True)
    print(agent,decoded)
    return decoded
