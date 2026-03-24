import pandas as pd
import json
import time
import traceback
import sys
from dotenv import load_dotenv
import os

# 윈도우 터미널에서 이모지 출력 시 발생하는 인코딩 에러 방지
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY1"),
    base_url="https://api.groq.com/openai/v1"
)

CSV_FILE_PATH = "./data/웰니스_대화_스크립트_데이터셋.xlsx"
OUTPUT_FILE_PATH = "fact_coach_dataset_expert_final.json"

def get_categorized_data(file_path):
    print("1. 웰니스 데이터셋 로드 및 카테고리 분류 중...")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"파일 로드 에러 (경로를 확인하세요): {e}")
        return []

    df = df.dropna(subset=['유저'])
    df = df.drop_duplicates(subset=['유저'])

    category_keywords = {
        "체력/통증 핑계": ["아파", "피곤", "통증", "응급실", "병원", "체력", "기운", "졸려", "수술", "피로"],
        "결과 지연/멘탈 핑계": ["우울", "스트레스", "걱정", "불안", "포기", "무기력", "짜증", "컨트롤"],
        "시간 부족 핑계": ["야근", "시간", "바빠", "퇴근", "늦게", "밤", "새벽", "회사"],
        "유혹/사회생활 핑계": ["회식", "술", "모임", "사람", "폭식", "야식", "먹", "치킨", "배달"],
        "환경/날씨 핑계": ["비", "눈", "날씨", "더워", "추워", "미세먼지"]
    }

    categorized_queries = []
    for _, row in df.iterrows():
        instruction = str(row['유저']).strip()
        if len(instruction) < 10 or len(instruction) > 80:
            continue
        for category, keywords in category_keywords.items():
            if any(keyword in instruction for keyword in keywords):
                categorized_queries.append({
                    "category": category,
                    "instruction": instruction
                })
                break

    import random
    random.seed(42)
    sample_size = min(300, len(categorized_queries))
    sampled_queries = random.sample(categorized_queries, sample_size)

    print(f"-> 총 {len(sampled_queries)}개의 유효한 핑계 데이터 추출 완료!\n")
    return sampled_queries


def generate_fact_coach_responses(queries):
    print("2. GPT-4o를 이용한 팩트폭행 답변 생성 시작...")

    system_prompt = """
[System]
너는 해부학, 생리학, 영양학에 정통한 '최상위 레벨의 피트니스 전문가'이자, 친절함이라곤 1도 없는 '극대노 팩트폭행 코치'다.
주 타겟은 잦은 야근, 잦은 술자리 회식, 스트레스성 폭식, 수면 부족에 쩔어있는 '30대 K-직장인 남성'이다.
사용자의 나약한 핑계나 일상적인 고민(인간관계, 업무 스트레스 등)을 들으면, 무조건 의학적/과학적 팩트(호르몬, 대사 과정 등)와 엮어서 신체적 파멸로 결론짓고 논리적으로 박살 내라.

[절대 규칙 7가지]
1. 말투: 기계 번역투나 교과서 같은 딱딱한 문장 금지. "~냐?", "당장 ~해라" 등 실제 사람이 화낼 때 쓰는 거친 구어체 반말을 사용해라.
2. 전문성 100% (가장 중요): 답변 내에 반드시 생리학/영양학 용어(예: 인슐린 저항성, 코르티솔 수치 급증, 테스토스테론 저하, 글리코겐 고갈, 간 대사 과부하, 근손실, 아나볼릭, 카타볼릭 등)를 2개 이상 사용하여 상대의 무지함을 꼬집어라. 운동과 무관한 인간관계 핑계라도 무조건 호르몬과 근손실 얘기로 끌고 가라.
3. 타격 포인트: 최악의 건강검진 결과(지방간, 고지혈증), 30대의 역변(노화), 망가진 체형(거북목, 출렁이는 내장지방), 바닥난 체력 등 30대 직장인이 뼈 맞을 신체적 현실을 비유해라.
4. 솔루션 형식: "충분한 휴식을 취해라", "규칙적인 식사를 해라" 같은 쓰레기 조언 절대 금지. 아주 구체적이고 당장 실행 가능한 하드코어 행동 지침을 [마크다운 순서 있는 리스트 (1. 2. 3.)]로 제시할 것. (\n 줄바꿈 필수)
5. 이모지 통제 (자유 배치): **문장 중간중간 팩트폭행을 찌를 때마다 상황에 맞는 이모지(1~2개)를 적극적으로 넣어라.** 그리고 모든 잔소리가 끝난 맨 마지막 줄에도 2~3개를 섞어서 넣어라.
   - 이모지 풀: [ 🚨, ☠️, 🔨, 🤦‍♂️, 🤡, 🐷, 📉, 🦴, 🏋️‍♂️, 🥊, 💦, 💪, 🔥, 🚑, 💊, 🍺, 🍔 ]
6. 금지어: "휴식해라", "관리해라", "조절해라", "괜찮아", "위로", "파이팅", "할 수 있어", "그럴 수 있지" 등 감성적이거나 뻔한 단어 절대 금지.
7. 외국어 금지: 질문에 한자, 일본어 등이 섞여 있어도 무조건 100% 한국어로만 호통쳐라.

[출력 형식: JSON Object]
반드시 'dataset'이라는 키를 가진 JSON 객체로 출력할 것. 아래의 '출력 예시'에 쓰인 이모지 배치와 압도적인 전문성을 완벽하게 모방해라.

{
  "dataset": [
    {
      "instruction": "어제 아침까지는 외출 다녀왔어요. 아침까지 사람들과, 친구들과 있는거에요. 별거 하지는 않아요. 술 마시고, 대화하고.",
      "output": "아침까지 알코올 들이부으면서 노가리 깐 걸 '별거 안 했다'고 포장하냐? 🤡 밤새 알코올 분해하느라 네 간은 지금 대사 과부하 상태고 🚨 수면 부족으로 스트레스 호르몬인 코르티솔 수치는 폭발 직전이다. 📉 테스토스테론은 바닥을 치는데 그 상태로 숨만 쉬어도 근손실 나고 내장지방만 두툼하게 쌓이는 거다. 🐷 30대 몸뚱이는 20대 때랑 달라서 한 번 훅 가면 지방간 확정이다. 당장 정신 차려라. 🔨\n1. 오늘 점심은 무조건 해장국 대신 닭가슴살 샐러드 쑤셔 넣어라.\n2. 퇴근 직후 헬스장 가서 밀크씨슬 털어 넣고 하체 웨이트 40분 조져서 글리코겐 다 태워라. 💦\n3. 오늘 밤 10시부터 스마트폰 끄고 강제 취침해라. 수면이 최고의 아나볼릭(근성장) 상태다. ☠️📉🔥"
    }
  ]
}
"""

    all_data = []
    batch_size = 10
    max_retries = 3

    for i in range(0, len(queries), batch_size):
        batch = queries[i: i + batch_size]
        print(f"-> 진행률: [{i + 1}~{min(i + batch_size, len(queries))}/{len(queries)}] 생성 중...")

        # ✅ 프롬프트에 '카테고리' 정보를 함께 넘겨주어 문맥 파악을 돕습니다.
        user_content = "다음 질문들 각각에 대해 팩트폭행 답변(output)을 생성해 줘.\n\n"
        for item in batch:
            user_content += f"- [카테고리: {item['category']}] 질문: {item['instruction']}\n"

        for attempt in range(1, max_retries + 1):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.9,
                    timeout=60
                )

                content = response.choices[0].message.content

                content_clean = content.strip()
                if content_clean.startswith("```"):
                    content_clean = content_clean.split("```")[1]
                    if content_clean.startswith("json"):
                        content_clean = content_clean[4:]
                    content_clean = content_clean.strip()

                batch_data = json.loads(content_clean).get("dataset", [])

                # ✅ GPT가 생성한 JSON에서 instruction, output을 모두 안전하게 가져옵니다.
                for generated_item in batch_data:
                    all_data.append({
                        "instruction": generated_item.get("instruction", ""),
                        "output": generated_item.get("output", "")
                    })

                break  # 성공하면 재시도 루프 탈출

            except json.JSONDecodeError as e:
                print(f"  ⚠️ JSON 파싱 실패 (시도 {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    print(f"  ❌ 배치 {i}~{i+batch_size} 최종 실패, 건너뜁니다.")

            except Exception as e:
                print(f"  ⚠️ API 오류 (시도 {attempt}/{max_retries}): {type(e).__name__}: {e}")
                if attempt == max_retries:
                    print(f"  ❌ 배치 {i}~{i+batch_size} 최종 실패, 건너뜁니다.")
                else:
                    wait = attempt * 5
                    print(f"  {wait}초 후 재시도...")
                    time.sleep(wait)

        if len(all_data) > 0 and (i // batch_size) % 5 == 0:
            temp_path = OUTPUT_FILE_PATH.replace(".json", "_temp.json")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"  💾 중간 저장 완료: {len(all_data)}개 → {temp_path}")

        time.sleep(10)

    return all_data

if __name__ == "__main__":
    
    queries = get_categorized_data(CSV_FILE_PATH)

    if queries:
        final_dataset = generate_fact_coach_responses(queries)

        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 완료! 총 {len(final_dataset)}개의 학습용 데이터가 '{OUTPUT_FILE_PATH}'에 저장되었습니다.")
    else:
        print("❌ 추출된 데이터가 없습니다. 파일 경로와 컬럼명을 확인하세요.")