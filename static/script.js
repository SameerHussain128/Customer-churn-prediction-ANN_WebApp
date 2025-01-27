document.getElementById("predictButton").addEventListener("click", async () => {
    const formData = new FormData(document.getElementById("churnForm"));
    const data = {};

    formData.forEach((value, key) => {
        data[key] = isNaN(value) ? value : parseFloat(value); // Convert numeric inputs to numbers
    });

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    const resultElement = document.getElementById("result");

    if (response.ok) {
        resultElement.textContent = `Prediction: ${result.prediction}, Probability: ${(result.probability * 100).toFixed(2)}%`;
    } else {
        resultElement.textContent = `Error: ${result.error}`;
    }
});
