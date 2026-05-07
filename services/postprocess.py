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

FIELD_MAPPING_PASSPORT = {
    "passport_id": "Số hộ chiếu",
    "name": "Họ và tên",
    "nationality": "Quốc tịch",
    "dob": "Ngày sinh",
    "birth_place": "Nơi sinh",
    "gender": "Giới tính",
    "id_card": "Số GCMND",
    "issue_date": "Ngày cấp",
    "expiry": "Có giá trị đến",
    "issue_place": "Nơi cấp"
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