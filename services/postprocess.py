FIELD_MAPPING = {
    "id": "Số",
    "name": "Họ và tên",
    "dob": "Ngày sinh",
    "gender": "Giới tính",
    "nationality": "Quốc tịch",
    "hometown": "Quê quán",
    "address": "Nơi thường trú",
    "expiry": "Có giá trị đến"
}


def postprocess_result(raw_result):
    final_result = {}

    for key, value in raw_result.items():

        # Remove extra spaces
        value = value.strip()

        # Convert field name
        vietnamese_key = FIELD_MAPPING.get(key, key)

        final_result[vietnamese_key] = value

    return final_result