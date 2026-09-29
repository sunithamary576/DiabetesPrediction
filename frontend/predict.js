const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        HighBP: Number(document.getElementById("HighBP").value),
        HighChol: Number(document.getElementById("HighChol").value),
        CholCheck: Number(document.getElementById("CholCheck").value),
        BMI: Number(document.getElementById("BMI").value),
        Smoker: Number(document.getElementById("Smoker").value),
        Stroke: Number(document.getElementById("Stroke").value),
        HeartDiseaseorAttack: Number(
            document.getElementById("HeartDiseaseorAttack").value
        ),
        PhysActivity: Number(
            document.getElementById("PhysActivity").value
        ),
        Fruits: Number(document.getElementById("Fruits").value),
        Veggies: Number(document.getElementById("Veggies").value),
        HvyAlcoholConsump: Number(
            document.getElementById("HvyAlcoholConsump").value
        ),
        AnyHealthcare: Number(
            document.getElementById("AnyHealthcare").value
        ),
        NoDocbcCost: Number(
            document.getElementById("NoDocbcCost").value
        ),
        GenHlth: Number(document.getElementById("GenHlth").value),
        MentHlth: Number(document.getElementById("MentHlth").value),
        PhysHlth: Number(document.getElementById("PhysHlth").value),
        DiffWalk: Number(document.getElementById("DiffWalk").value),
        Sex: Number(document.getElementById("Sex").value),
        Age: Number(document.getElementById("Age").value),
        Education: Number(
            document.getElementById("Education").value
        ),
        Income: Number(document.getElementById("Income").value)
    };

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.prediction === 1) {
        document.getElementById("message").textContent =
            "Prediction: Higher diabetes risk";
    } else {
        document.getElementById("message").textContent =
            "Prediction: Lower diabetes risk";
    }
});