# тексты ошибок

EMPTY_URL = {
    'text': 'url является обязательным параметром для запроса. Пожалуйста, введите корректный запрос.',
    'reason': '400 Bad Request - URL Is Empty',
}

INVALID_URL = {
    'text': 'Был введен некорректный или несуществующий URL. Проверьте введенный URL.',
    'reason': '{} {} - URL Is Invalid',
}

INVALID_TEXT_WIDTH = {
    'text': 'Параметр output_text_width должен быть целым числом больше 0.',
    'reason': '400 Bad Request - Invalid Text Width Parameter',
}

INVALID_IMG_LINKS = {
    'text': 'Параметр saving_img_links должен принимать значения True или False.',
    'reason': '400 Bad Request - Invalid Images Links Parameter',
}

INVALID_FILE_NAME = {
    'text': 'Неверно задано имя файла.',
    'reason': '400 Bad Request - Invalid File Name',
}
