import joblib

# Load model + vectorizer
model = joblib.load("phishing_model.pk1")
vectorizer = joblib.load("vectorizer.pk1")

# Test with some emails
emails_to_test = [
    "Your password has expired. Click here to reset it.",
    "Let's meet tomorrow at the office.",
    "Congratulations! You won a gift card. Claim now.",
]

for email in emails_to_test:
    X_test = vectorizer.transform([email])
    prediction = model.predict(X_test)[0]
    print(f"Email: {email}")
    print("Prediction:", "Phishing 🚨" if prediction == 1 else "Safe ✅")
    print("-" * 50)
