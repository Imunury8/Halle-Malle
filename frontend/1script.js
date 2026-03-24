// 침 + 입력칸을 같이 올릴 거리(px)
const MOVE = 30;

const needleWrap = document.getElementById("needleWrap");
const inputWrap = document.getElementById("inputWrap");
const guideText = document.getElementById("guideText");
const input = document.getElementById("mainInput");
const button = document.querySelector(".input-wrap button");
const mainTitle = document.querySelector(".title");

if (mainTitle) {
  mainTitle.style.cursor = "pointer";
  mainTitle.addEventListener("click", () => {
    input.value = "";
    resultBox.innerHTML = "";
  });
}
if (needleWrap) needleWrap.style.transform = `translateY(-${MOVE}px)`;
if (inputWrap) inputWrap.style.transform = `translateY(-${MOVE}px)`;

// 결과 표시용 div 만들기
let resultBox = document.createElement("div");
resultBox.className = "answer-style";   // ← 추가


resultBox.style.marginTop = "24px";
resultBox.style.maxWidth = "1000px";
resultBox.style.padding = "20px";
resultBox.style.whiteSpace = "pre-wrap";

document.querySelector(".main").appendChild(resultBox);
input.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // 기본 엔터 동작 방지
    button.click(); // 버튼 클릭 실행
  }
});

// 버튼 클릭 이벤트 
button.addEventListener("click", async () => {
  const userText = input.value.trim();
  if (!userText) return;

  // 1. 답변 생성 시작 시 안내 문구 숨기기
  if (guideText) {
    guideText.style.display = "none";
  }

  resultBox.innerText = "답변 생성 중...";


  try {
    // 2. 내 파이썬 서버(main.py)로 데이터 전송
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_text: userText
      })
    });

    const data = await res.json();

    // 3. 응답 처리
    if (data.error) {
      resultBox.innerText = `API 에러 발생: ${data.error}`;
    } else if (data.answer) {
      const lines = data.answer
        .split("\n")
        .filter(line => line.trim() !== "")
        .slice(0, 3);

      resultBox.innerHTML = "";

      lines.forEach((line, index) => {
        const p = document.createElement("div");
        p.innerText = line;

        // 문장 내부 줄 간격
        p.style.lineHeight = "5";

        // 문장 사이 간격
        p.style.marginBottom = "18px";

        resultBox.style.wordBreak = "keep-all";

        resultBox.appendChild(p);
      });
    } else {
      resultBox.innerText = "응답 데이터 형식이 올바르지 않습니다.";
    }

  } catch (e) {
    // 서버가 안 켜져 있으면 이 에러가 뜹니다.
    resultBox.innerText = `네트워크 에러: ${e.message}\n(파이썬 서버 main.py를 실행했는지 확인하세요!)`;
    console.error("Fetch Error:", e);
  }
}); // <-- 여기서 닫는 괄호가 정확히 들어가야 합니다!

