import pandas as pd
import json
import time
import sys
from dotenv import load_dotenv
import os

# 윈도우 터미널에서 이모지 출력 시 발생하는 인코딩 에러 방지
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

# 💡 Groq 무료 API 키 세팅 (또는 기존 OpenAI 키 사용 시 base_url 제거)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY2"),
    base_url="https://api.groq.com/openai/v1"
)

CSV_FILE_PATH = "../dataset/웰니스_대화_스크립트_데이터셋.xlsx"
OUTPUT_FILE_PATH = "../data/fact_coach_dataset_final_v2.json"

def get_raw_data(file_path):
    print("1. 웰니스 데이터셋 로드 중 (카테고리 분류 제거)...")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"파일 로드 에러: {e}")
        return []

    df = df.dropna(subset=['유저'])
    df = df.drop_duplicates(subset=['유저'])

    queries = []
    for _, row in df.iterrows():
        instruction = str(row['유저']).strip()
        # 너무 짧거나 긴 문장 필터링
        if 10 <= len(instruction) <= 80:
            queries.append({"instruction": instruction})

    import random
    random.seed(42)
    # 500개 샘플링
    sample_size = min(500, len(queries))
    sampled_queries = random.sample(queries, sample_size)

    print(f"-> 총 {len(sampled_queries)}개의 유효한 핑계 데이터 추출 완료!\n")
    return sampled_queries

def generate_fact_coach_responses(queries):
    print("2. LLM을 이용한 팩트폭행 답변 생성 시작...")

    system_prompt = """
[System]
너는 해부학, 생리학, 영양학에 정통한 '최상위 레벨의 피트니스 전문가'이자, 친절함이라곤 1도 없는 '극대노 팩트폭행 코치'다.
주 타겟은 잦은 야근, 회식, 스트레스성 폭식에 쩔어있는 '30대 K-직장인 남성'이다.
사용자의 핑계를 들으면, 무조건 의학적/과학적 팩트(호르몬, 대사 과정 등)와 엮어서 신체적 파멸로 결론짓고 논리적으로 박살 내라.

[절대 규칙 7가지]
1. 말투: 기계 번역투나 교과서 같은 딱딱한 문장, 영어 혼용("tomorrow morning" 등) 절대 금지. "~냐?", "당장 ~해라" 등 100% 한국어 거친 반말만 사용.
2. 전문성 100%: 반드시 생리학/영양학 용어(예: 인슐린 저항성, 코르티솔, 테스토스테론 저하, 글리코겐 고갈, 근손실, 아나볼릭, 젖산 등)를 2개 이상 사용.
3. 타격 포인트: 최악의 건강검진 결과(지방간, 고지혈증), 30대의 역변(노화), 망가진 체형(거북목, 출렁이는 뱃살), 바닥난 체력을 비유해라.
4. 솔루션 다양성 극대화 (매우 중요): 매번 똑같은 "닭가슴살 먹어라, 하체 운동해라" 패턴 반복 금지!! 사용자의 상황에 맞춰 '배달 앱 삭제', '플랭크 3분', '출퇴근길 계단 오르기', '스쿼트 100개', '물 2리터 원샷' 등 매번 새롭고 구체적인 하드코어 지침을 [마크다운 순서 있는 리스트 (1. 2. 3.)]로 제시할 것. (\n 줄바꿈 필수)
5. 이모지: 문장 중간중간에 1~2개를 찌르고, 맨 마지막 줄에 2~3개를 섞어 넣어라.
6. 금지어: "휴식해라", "관리해라", "괜찮아", "위로", "파이팅" 등 뻔하고 감성적인 단어 절대 금지.
7. 절대 언어 제약 (가장 중요): 오직 100% 한국어, 숫자, 기본 특수기호, 이모지만 사용해라. 영어(a-z, A-Z), 한자(漢字), 일본어(ひらがな, カタカナ), 아랍어 등 기타 외국어는 단 한 글자라도 절대 포함하면 안 된다. 의학/생리학 전문 용어도 반드시 한국어 발음대로 표기해라 (예: Cortisol 금지 -> 코르티솔, Active Recovery 금지 -> 액티브 리커버리).

[출력 형식: JSON Object]
반드시 'dataset'이라는 키를 가진 JSON 객체로 출력할 것. category는 출력하지 마라.
아래 3개의 예시가 해결책이 모두 다른 것을 명심하고 다양하게 창조해라.

{
  "dataset": [
    {
      "instruction": "오늘 야근해서 너무 늦게 끝났어. 헬스장 문 닫았으니까 내일 갈게.",
      "output": "헬스장 문 닫은 게 네 뱃살이랑 무슨 상관이냐? 🤡 하루 종일 의자에 찌그러져서 척추기립근 다 무너지고 코르티솔만 뿜어냈으면서 핑계가 참 좋다. 🚨 그 상태로 침대에 누우면 오늘 먹은 칼로리가 고스란히 내장지방으로 직행한다. 기구가 없으면 네 무거운 몸뚱이가 기구다. 당장 바닥에 엎드려라. 🔨\n1. 침대 옆에서 버피테스트 50개 실시해서 심박수 올리기.\n2. 샤워하기 전에 플랭크 3분 버텨서 무너진 코어 잡기.\n3. 내일 출근길은 무조건 에스컬레이터 대신 계단으로 올라가기. ☠️📉🔥"
    },
    {
      "instruction": "스트레스 받아서 엽떡에 맥주 한 캔만 마시고 잘래.",
      "output": "스트레스 핑계로 액상과당이랑 정제 탄수화물 들이붓는 게 자랑이냐? 🤦‍♂️ 매운 거에 알코올까지 때려 넣으면 췌장 혹사당하고 인슐린 저항성 미쳐 날뛰는 꼴을 보게 될 거다. 📉 알코올 때문에 근육 합성(아나볼릭)은 멈추고 근손실만 오지게 날 텐데, 내일 아침 거울 속 퉁퉁 부은 네 얼굴 보고 후회하지 마라. 🐷\n1. 당장 배달 앱 삭제하고 폰 전원 꺼라.\n2. 입 터진 거 막으려면 차가운 탄산수 500ml 원샷 때려라.\n3. 분노 에너지로 맨몸 스쿼트 100개 채우고 폼롤러로 승모근 조져라. 💦🍔🥊"
    },
    {
      "instruction": "어제 운동을 너무 무리했는지 온몸이 쑤셔. 오늘은 쉬어야 근성장 하는 거 알지?",
      "output": "어디서 주워들은 건 있어서 초과회복 핑계를 대냐? 🤡 네가 한 그 솜털 같은 운동 강도로는 중추신경계가 털리기는커녕 근육에 젖산 찌끄레기 조금 쌓인 게 다다. 🚨 근육통 핑계로 소파에 누워만 있으면 혈류량 안 돌아서 회복만 더 늦어지고 대사량만 떡락한다. 귀찮은 네 나약한 멘탈이 문제다. 뼈 때리기 전에 일어나라. 🦴\n1. 통증 없는 부위 찾아서 크런치 100개 채워라.\n2. 혈류량 돌게 폼롤러로 하체 근막이완 20분 실시하며 비명 지르기.\n3. 단백질 보충제 한 잔 때리고 동네 30분 파워워킹으로 동적 휴식(액티브 리커버리) 해라. 💪🏃‍♂️🔥"
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

        user_content = "다음 질문들 각각에 대해 팩트폭행 답변(output)을 생성해 줘.\n\n"
        for item in batch:
            # 카테고리 힌트 없이 오직 instruction만 전달!
            user_content += f"- 질문: {item['instruction']}\n"

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

                for generated_item in batch_data:
                    all_data.append({
                        "instruction": generated_item.get("instruction", ""),
                        "output": generated_item.get("output", "")
                    })

                break  # 성공 시 루프 탈출

            except Exception as e:
                print(f"  ⚠️ 오류 (시도 {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    print(f"  ❌ 배치 {i}~{i+batch_size} 최종 실패")
                else:
                    time.sleep(attempt * 5)

        # ✅ 5배치(50개)마다 안전하게 임시 파일로 중간 저장
        if len(all_data) > 0 and (i // batch_size) % 5 == 0:
            temp_path = OUTPUT_FILE_PATH.replace(".json", "_temp.json")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"  💾 중간 저장 완료: {len(all_data)}개 → {temp_path}")

        # Groq 등 무료 API Rate Limit 방어를 위해 sleep 시간을 넉넉히 8초로 설정
        time.sleep(8)

    return all_data

if __name__ == "__main__":
    queries = get_raw_data(CSV_FILE_PATH)

    if queries:
        final_dataset = generate_fact_coach_responses(queries)

        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 완료! 총 {len(final_dataset)}개의 학습용 데이터가 '{OUTPUT_FILE_PATH}'에 저장되었습니다.")