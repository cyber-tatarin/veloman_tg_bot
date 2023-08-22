from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import callback_data_models, utils
from root.logger.config import logger

logger = logger


def get_ikb_to_set_country():
    ikb_to_send_country = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Беларусь', callback_data=callback_data_models.set_country_cb_data.new('Беларусь'))
    b2 = InlineKeyboardButton(text='Россия', callback_data=callback_data_models.set_country_cb_data.new('Россия'))
    ikb_to_send_country.add(b1, b2)
    return ikb_to_send_country


def get_ikb_to_get_erip_info():
    pass


def get_ikb_to_get_phone_number():
    pass


def get_ikb_to_choose_belarusian_bank():
    ikb_to_choose_belarusian_bank = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Альфа-Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Альфа-Банк'))
    b2 = InlineKeyboardButton(text='Банк БелВЭБ', callback_data=callback_data_models.set_bel_bank_cb_data.new('Банк БелВЭБ'))
    b3 = InlineKeyboardButton(text='Банк ВТБ (Беларусь)', callback_data=callback_data_models.set_bel_bank_cb_data.new('Банк ВТБ (Беларусь)'))
    b4 = InlineKeyboardButton(text='Банк Дабрабыт', callback_data=callback_data_models.set_bel_bank_cb_data.new('Банк Дабрабыт'))
    b5 = InlineKeyboardButton(text='Банк Решение', callback_data=callback_data_models.set_bel_bank_cb_data.new('Банк Решение'))
    b6 = InlineKeyboardButton(text='Белагропромбанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Белагропромбанк'))
    b7 = InlineKeyboardButton(text='Беларусбанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Беларусбанк'))
    b8 = InlineKeyboardButton(text='Белгазпромбанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Белгазпромбанк'))
    b9 = InlineKeyboardButton(text='БНБ-Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('БНБ-Банк'))
    b10 = InlineKeyboardButton(text='БСБ Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('БСБ Банк'))
    b11 = InlineKeyboardButton(text='БТА Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('БТА Банк'))
    b12 = InlineKeyboardButton(text='МТБанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('МТБанк'))
    b13 = InlineKeyboardButton(text='Паритетбанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Паритетбанк'))
    b14 = InlineKeyboardButton(text='Приорбанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Приорбанк'))
    b15 = InlineKeyboardButton(text='РРБ-Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('РРБ-Банк'))
    b16 = InlineKeyboardButton(text='Сбер Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Сбер Банк'))
    b17 = InlineKeyboardButton(text='СтатусБанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('СтатусБанк'))
    b18 = InlineKeyboardButton(text='Технобанк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Технобанк'))
    b19 = InlineKeyboardButton(text='Цептер Банк', callback_data=callback_data_models.set_bel_bank_cb_data.new('Цептер Банк'))
    ikb_to_choose_belarusian_bank.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12,
                                      b13, b14, b15, b16, b17, b18, b19)
    return ikb_to_choose_belarusian_bank


def get_ikb_to_choose_bel_bank_erip_info(bel_bank):
    ikb_to_choose_bel_bank_erip_info = InlineKeyboardMarkup(row_width=1)
    for index, erip_category in enumerate(utils.bel_bank_erip_categories[bel_bank]):
        b = InlineKeyboardButton(text=erip_category,
                                 callback_data=callback_data_models.set_bel_bank_category_cb_data.new(index))
        ikb_to_choose_bel_bank_erip_info.add(b)
    
    return ikb_to_choose_bel_bank_erip_info


def get_ikb_to_choose_start_action():
    ikb_to_choose_start_action = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Я хочу оставить отзыв', callback_data='wanna_leave_review')
    b2 = InlineKeyboardButton(text='Я уже оставил(а) отзыв', callback_data='already_left_review')
    ikb_to_choose_start_action.add(b1, b2)
    return ikb_to_choose_start_action


def get_ikb_to_proceed_after_leaving_review():
    ikb_to_choose_start_action = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Я оставил(а) отзыв', callback_data='already_left_review')
    ikb_to_choose_start_action.add(b1)
    return ikb_to_choose_start_action


def get_ikb_to_choose_way_of_payment(country):
    ikb_to_choose_start_action = InlineKeyboardMarkup(row_width=1)
    # b1 = InlineKeyboardButton(text='На карту', callback_data='payment_by_card_bel')
    # b2 = InlineKeyboardButton(text='На телефон', callback_data='payment_by_phone')
    # ikb_to_choose_start_action.add(b1, b2)
    
    for payment_option in utils.country_payment_options[country]:
        b = InlineKeyboardButton(text=payment_option[0], callback_data=payment_option[1])
        ikb_to_choose_start_action.add(b)
    
    return ikb_to_choose_start_action


def get_ikb_to_edit_country():
    ikb_to_edit_country = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Изменить страну', callback_data='edit_country')
    ikb_to_edit_country.add(b1)
    return ikb_to_edit_country


def get_ikb_to_edit_payment_option():
    ikb_to_edit_payment_option = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Изменить способ оплаты', callback_data='edit_payment_option')
    ikb_to_edit_payment_option.add(b1)
    return ikb_to_edit_payment_option


def get_ikb_to_edit_phone_number():
    ikb_to_edit_phone_number = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Изменить номер телефона', callback_data='edit_phone_number')
    ikb_to_edit_phone_number.add(b1)
    return ikb_to_edit_phone_number


def get_ikb_to_edit_bel_bank():
    ikb_to_edit_bel_bank = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Изменить банк', callback_data='edit_bel_bank')
    ikb_to_edit_bel_bank.add(b1)
    return ikb_to_edit_bel_bank


def get_ikb_to_mark_order_as_done():
    ikb_to_mark_order_as_done = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Выполнил', callback_data='mark_order_as_done')
    b2 = InlineKeyboardButton(text='Фейковый отзыв', callback_data='mark_order_as_fake')
    ikb_to_mark_order_as_done.add(b1, b2)
    return ikb_to_mark_order_as_done

