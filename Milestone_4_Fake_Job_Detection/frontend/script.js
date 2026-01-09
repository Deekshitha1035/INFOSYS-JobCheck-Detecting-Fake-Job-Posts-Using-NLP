async function predict() {
  const textArea = document.getElementById("jobText");
  const resultDiv = document.getElementById("result");

  const jobText = textArea.value.trim();
  if (!jobText) {
    alert("Please enter a job description");
    return;
  }

  // Show loading
  resultDiv.className = "result loading";
  resultDiv.innerHTML = "🔍 Analyzing job description...";
  resultDiv.classList.remove("hidden");

  try {
    // ✅ Get token from localStorage by key "token"
    const token = localStorage.getItem("token");

      alert("Please login first!");
      resultDiv.className = "result fake";
      resultDiv.innerHTML = "❌ No token found. Login first!";
      return;
    }

    // ✅ Use the token variable in Authorization header
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHAiOjE3Njc2Mjc4OTZ9.Mb7AoYv1LgtemVRvekMS-nVqSEIjvc1V20oGeaXJfWI}` // Correct
      },
      body: JSON.stringify({ text: jobText })
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();
    const isFake = data.prediction.toLowerCase() === "fake";
    const colorClass = isFake ? "fake" : "real";

    resultDiv.className = `result ${colorClass}`;
    resultDiv.innerHTML = `
      <h2>${isFake ? "❌ Fake Job" : "✅ Real Job"}</h2>
      <p><strong>Confidence:</strong> ${data.confidence}%</p>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width:${data.confidence}%"></div>
      </div>
    `;
  } catch (error) {
    resultDiv.className = "result fake";
    resultDiv.innerHTML = "❌ Server error. Is backend running?";
    console.error(error);
  }
}
