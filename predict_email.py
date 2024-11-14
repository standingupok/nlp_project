def predict_email(email, classifier, w2v_model):

    def isSpam(email):
      email_cleaned = preprocess_email(email)
      email_vector = vectorize(email_cleaned, w2v_model)
      predicted_label = classifier.predict(email_vector)
      print('Spam' if predicted_label[0] == 0 else 'Ham',' ---', email)

    results = []

    if(type(email) == str):
        isSpam(email)
      # results.append(isSpam(email))

    elif(type(email) == list):
      for corpus in email:
        isSpam(corpus)
