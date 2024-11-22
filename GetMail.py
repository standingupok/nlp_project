import imaplib
import email
from email.header import decode_header
import re

# Thông tin đăng nhập
username = "tuanbenten24@gmail.com"
password = "uxwg rsjz mzdr amey"

# username = "nguyenhoanglong0165@gmail.com"
# password = "cyaz ewkp ewjt vmck"

# Kết nối đến Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
mail.select("inbox")

# Tìm kiếm 8 email gần nhất
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()[-8:]  # Lấy 8 email gần nhất

emails = []

# Hàm làm sạch nội dung email
def clean_email_content(content):
    # Loại bỏ các đường link
    content = re.sub(r"http\S+|www\S+|https\S+", "", content, flags=re.MULTILINE)
    # Loại bỏ các thẻ HTML của hình ảnh
    content = re.sub(r"<img[^>]*>", "", content, flags=re.MULTILINE)
    # Loại bỏ ký tự xuống dòng và khoảng trắng thừa
    content = re.sub(r'\r\n|\n', ' ', content)
    content = re.sub(r'\s+', ' ', content).strip()
    return content

# Lặp qua từng email
for email_id in email_ids:
    # Lấy email bằng ID
    res, msg = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg[0][1])

    # Giải mã tiêu đề
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else 'utf-8')

    # Lấy và làm sạch nội dung email
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            # Chỉ lấy nội dung dạng text, bỏ qua các tệp đính kèm
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body += part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()

    # Làm sạch và lưu thông tin email
    clean_body = clean_email_content(body)
    emails.append({"subject": subject, "content": clean_body})

# Đăng xuất
mail.logout()

# Gọi hàm dự đoán spam cho từng email
predictions = []
for email_data in emails:
    # Chuyển đổi nội dung email thành vector
    email_vector = vectorize(preprocess_email(email_data["content"]), w2v_model)

    # Dự đoán nhãn cho email
    prediction = knnClassifier.predict(email_vector)
    # Gọi hàm dự đoán spam cho từng email
predictions = []
for email_data in emails:
    # Chuyển đổi nội dung email thành vector
    cleaned_email = preprocess_email(email_data["content"])
    # print(cleaned_email)
    email_vector = vectorize(cleaned_email, w2v_model)
    # print(email_vector)

    # Dự đoán nhãn cho email
    prediction = knnClassifier.predict(email_vector)

    # Chuyển đổi dự đoán từ mảng 1D sang định dạng dễ đọc
    predictions.append('Spam' if prediction[0] == 0 else 'Ham')


# In ra thông tin từng email và dự đoán
for i, email_data in enumerate(emails):
    print("Subject:", email_data["subject"])
    print("Content:", email_data["content"])
    print("Prediction:", predictions[i])  # In ra dự đoán tương ứng
    print("-" * 40)
