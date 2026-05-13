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

def postprocess_result(raw_result):
    final_result = {}
    for eng_key, vn_key in FIELD_MAPPING.items():
        value = raw_result.get(eng_key, "")
        final_result[vn_key] = value.strip()
    return final_result