async function predict() {
  const text = document.getElementById("jobText").value;
  if (text.length < 20) {
    alert("Please enter a valid job description");
    return;
  }

  const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  const result = document.getElementById("result");

  result.classList.remove("hidden", "real", "fake");
  result.classList.add(data.label.toLowerCase());
  result.innerHTML = `
    ${data.label} Job <br>
    Confidence: ${data.confidence}% <br>
    Time: ${data.processing_time} ms
  `;
}

function clearText() {
  document.getElementById("jobText").value = "";
  document.getElementById("result").classList.add("hidden");
}
