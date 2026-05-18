import re
from datetime import datetime

FIELD_MAPPING = {
    "id": "Số",
    "name": "Họ và tên",
    "dob": "Ngày sinh",
    "gender": "Giới tính",
    "nationality": "Quốc tịch",
    "origin_place": "Quê quán",
    "current_place": "Nơi thường trú",
    "expire_date": "Có giá trị đến"
}

def validate_id(id_str):
    """Kiểm tra số CCCD (phải là 12 chữ số)"""
    return bool(re.match(r'^\d{12}$', id_str))

def validate_date(date_str):
    """Kiểm tra định dạng ngày DD/MM/YYYY"""
    try:
        if not date_str: return False
        # Hỗ trợ các định dạng OCR thường sai (dùng . hoặc - thay vì /)
        clean_date = date_str.replace('.', '/').replace('-', '/')
        datetime.strptime(clean_date, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validate_gender(gender_str):
    """Kiểm tra giới tính (Nam/Nữ)"""
    valid_genders = ['Nam', 'Nữ', 'NAM', 'NỮ']
    return any(g in gender_str for g in valid_genders)

def postprocess_result(raw_result):
    final_result = {}
    validations = {}

    for eng_key, vn_key in FIELD_MAPPING.items():
        value = raw_result.get(eng_key, "").strip()
        is_valid = True
        
        # Áp dụng Rule-based Validation
        if eng_key == "id":
            is_valid = validate_id(value)
        elif eng_key in ["dob", "expire_date"]:
            is_valid = validate_date(value)
        elif eng_key == "gender":
            is_valid = validate_gender(value)
        elif eng_key == "name":
            is_valid = len(value) > 2 
            
        final_result[vn_key] = {
            "value": value,
            "is_valid": is_valid
        }
        
    return final_result