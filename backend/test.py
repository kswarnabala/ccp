import pickle

# Load the trained model and vectorizer
with open("phishing_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)


def is_suspicious_email(email_text):
    """Check if email is suspicious using trained model"""
    features = vectorizer.transform([email_text])
    prediction = model.predict(features)[0]  # 1 = suspicious, 0 = safe
    return prediction == 1


# Test emails
emails = [
    "Congratulations! You won a lottery. Click here to claim.",
    "Please find attached the project report.",
    "Your account has been compromised. Reset password immediately!",
    "Meeting is scheduled at 3 PM today."
]

for email in emails:
    if is_suspicious_email(email):
        print(f"Suspicious: {email}")
    else:
        print(f"Safe: {email}")
