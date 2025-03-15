from openai import AsyncOpenAI
import random

aclient = AsyncOpenAI(
    base_url="https://api.deepseek.com/",
    api_key="sk-?"
)

async def amake_chat(prompt: str) -> str:
    try:
        random_temp = round(random.uniform(0.5, 1.8), 1)
        dynamic_top_p = random.choice([0.5, 0.7, 0.9, 1.0])
        freq_penalty = random.uniform(-0.5, 0.5)
        pres_penalty = random.uniform(-0.5, 0.5)
        max_tokens = random.randint(80, 120)

        completion = await aclient.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=random_temp,
            top_p=dynamic_top_p,
            frequency_penalty=freq_penalty,
            presence_penalty=pres_penalty,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return "天机未现，请再试一次..."