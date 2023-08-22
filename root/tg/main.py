import asyncio
import datetime
import os
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, ParseMode
from aiogram.utils.exceptions import ChatNotFound
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.exc import IntegrityError

from . import callback_data_models, utils, keyboards
from root.gsheets import main as gsh
from root.logger.config import logger

logger = logger

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TG_API'))
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)

MANAGER_IDS = [459471362]
# MANAGER_IDS = [459471362]

database_error_message = ("У нас проблемы с базой данных. Если Вы видите это сообщение, напишите, "
                          "пожалуйста, мне @dimatatatarin")


# async def belarus_path(user_id):
#     await bot.send_message(user_id, 'Выберите наиболее удобный для Вас способ:',
#                            reply_markup=keyboards.get_ikb_to_choose_way_of_payment_bel())


# async def russia_path(user_id):
#     await bot.send_message(user_id,
#                            'Введите Ваш номер телефона, по которому можно перевести деньги в формате +74956667788')
#     await storage.set_state(chat=user_id, user=user_id, state='UserStates:get_phone_number')


# country_path_dict = {
#     'Беларусь': belarus_path,
#     'Россия': russia_path
# }


# country_step1_get_ikb = {
#     0: keyboards.get_ikb_to_get_erip_info(),
#     1: keyboards.get_ikb_to_get_phone_number()
# }


class UserStates(StatesGroup):
    # send_message_to_manager = State()
    get_phone_number = State()
    get_product_link = State()
    get_review_screenshot = State()
    get_bel_bank_creds = State()
    get_mobile_operator = State()


@logger.catch
@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message):
    await message.delete()
    
    await message.answer('Добро пожаловать в программу лояльности Veloman. '
                         'Благодарим за покупку в нашем магазине.\n\n'
                         'Хотим подарить Вам бонус в размере н рублей на карту или на телефон.\n\n'
                         'Чтобы получить бонус, оставьте, пожалуйста, отзыв о нашем товаре на Wildberries.\n\n'
                         'Может быть Вы уже успели оставили отзыв?', reply_markup=keyboards.get_ikb_to_choose_start_action())
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.register_user, user_id=message.from_user.id,
                                                       username=message.from_user.username,
                                                       user_full_name=message.from_user.full_name))


@logger.catch
@dp.callback_query_handler(lambda c: c.data == 'already_left_review', state='*')
async def register_review(callback_query: types.CallbackQuery):
    wait_message = await callback_query.message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    country = await gsh.async_execute_of_sync_gsheets(gsh.get_value, user_id=callback_query.from_user.id,
                                                      col_index=6)
    await wait_message.delete()
    if country:
        await callback_query.message.answer('Выберите наиболее удобный для Вас способ получения бонуса',
                                            reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()
    
    else:
        await callback_query.message.answer('Из какой Вы страны?', reply_markup=keyboards.get_ikb_to_set_country())
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()


@logger.catch
@dp.callback_query_handler(lambda c: c.data == 'wanna_leave_review', state='*')
async def wanna_leave_review(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Отлично!\n\nЧтобы оставить отзыв, нужно выполнить несколько простых шагов:\n\n'
                                        'На компьютере:\n'
                                        '1. Зайдите в личный кабинет Wildberries;\n'
                                        '2. Наведите мышкой на раздел "Профиль" в правом верхнем углу и выберите "Покупки";\n'
                                        '3. Нажмите на товар, который Вы купили в нашем магазине;\n'
                                        '4. Нажмите на кнопку "Оставить отзыв", она будет в правой части экрана под фотографиями товара;\n'
                                        '5. Напишите честный отзыв, прикрепите фотографию товара и поставьте оценку. нажмите "Отправить";\n'
                                        '6. Сделайте скриншот готового отзыва, чтобы отправить его нам.\n\n'
                                        'На телефоне:\n'
                                        '1. Зайдите в мобильное приложение Wildberries;\n'
                                        '2. Нажмите на иконку профиля в самом низу экрана (самая правая иконка);\n'
                                        '3. Нажмите на товар, который Вы купили в нашем магазине;\n'
                                        '4. Нажмите на кнопку "оценить товар". Она будет ниже, под описанием товара и блоком "Похожие товары";\n'
                                        '5. Напишите честный отзыв, прикрепите фотографию товара и поставьте оценку. нажмите "Отправить";\n'
                                        '6. Сделайте скриншот готового отзыва, чтобы отправить его нам.\n\n'
                                        'Когда оставите отзыв, нажмите на кнопку под этим сообщением, чтобы мы смогли отправить Вам бонус.',
                                        reply_markup=keyboards.get_ikb_to_proceed_after_leaving_review())
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


@dp.callback_query_handler(callback_data_models.set_country_cb_data.filter(), state='*')
async def get_country(callback_query: CallbackQuery, callback_data: dict):
    country = callback_data['country']
    
    await callback_query.message.edit_text(f'Вы выбрали страну: {country}',
                                           reply_markup=keyboards.get_ikb_to_edit_country())
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.set_user_country, user_id=callback_query.from_user.id,
                                                       country=country))
    
    await callback_query.message.answer('Выберите наиболее удобный для Вас способ получения бонуса',
                                        reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))
    
    # path = country_path_dict[country]
    # await path(callback_query.from_user.id)
    
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'payment_by_card_bel', state='*')
async def payment_by_card_bel(callback_query: types.CallbackQuery):
    state = dp.get_current().current_state()
    await state.update_data(payment_type='bel_bank')
    await callback_query.message.edit_text(f'Вы выбрали: перевод на карту',
                                           reply_markup=keyboards.get_ikb_to_edit_payment_option())
    
    wait_message = await callback_query.message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    bank_creds = await gsh.async_execute_of_sync_gsheets(gsh.check_if_user_has_saved_creds,
                                                         user_id=callback_query.from_user.id,
                                                         creds_type='bel_bank')
    await wait_message.delete()
    
    if bank_creds:
        
        await state.update_data(bel_bank=bank_creds[0], bel_bank_category=bank_creds[1], bel_bank_creds=bank_creds[2])
        await callback_query.message.answer(f'Мы помним Вас. Проверьте Ваши данные:\n\n'
                                            f'Банк:\n{bank_creds[0]}\n\n'
                                            f'Категория для перевода в ЕРИП:\n{bank_creds[1]}\n\n'
                                            f'Необходимые данные для перевода:\n{bank_creds[2]}\n\n',
                                            reply_markup=keyboards.get_ikb_to_edit_bel_bank())
        
        await callback_query.message.answer('Если все в порядке, то следующим сообщением пришлите ссылку на товар, '
                                            'под которым Вы оставили отзыв')
        await callback_query.message.answer('Чтобы найти ссылку на товар в мобильном приложении Wildberries:\n'
                                            '1. Зайдите на страницу товара;\n'
                                            '2. Нажмите в правом верхнем углу кнопку (она называется "Поделиться");\n'
                                            '3. В открывшемся меню выберите "Скопировать ссылку".\n\n'
                                            'Ссылка скопирована. Теперь вставьте ее в этот чат и отправьте.')
        
        await UserStates.get_product_link.set()
    else:
        await callback_query.message.answer('Выберите Ваш банк:',
                                            reply_markup=keyboards.get_ikb_to_choose_belarusian_bank())


@dp.callback_query_handler(lambda c: c.data == 'payment_by_phone_bel', state='*')
async def payment_by_phone_bel(callback_query: types.CallbackQuery):
    state = dp.get_current().current_state()
    await state.update_data(payment_type='phone')
    await callback_query.message.edit_text(f'Вы выбрали: перевод на телефон',
                                           reply_markup=keyboards.get_ikb_to_edit_payment_option())
    
    wait_message = await callback_query.message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    phone_creds = await gsh.async_execute_of_sync_gsheets(gsh.check_if_user_has_saved_creds,
                                                          user_id=callback_query.from_user.id,
                                                          creds_type='phone')
    await wait_message.delete()
    
    if phone_creds:
        await state.update_data(phone_number=phone_creds[0], mobile_operator=phone_creds[1])
        await callback_query.message.answer(f'Мы помним Вас. Проверьте Ваши данные:\n\n'
                                            f'Номер телефона:\n{phone_creds[0]}\n\n'
                                            f'Мобильный оператор:\n{phone_creds[1]}',
                                            reply_markup=keyboards.get_ikb_to_edit_phone_number())
        
        await callback_query.message.answer('Если все в порядке, то следующим сообщением пришлите ссылку на товар, '
                                            'под которым Вы оставили отзыв')
        await UserStates.get_product_link.set()
    
    else:
        await callback_query.message.answer(
            'Введите Ваш номер телефона, по которому можно перевести деньги в формате +375291112233')
        await UserStates.get_phone_number.set()


@dp.callback_query_handler(lambda c: c.data == 'payment_by_phone_rus', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    state = dp.get_current().current_state()
    await state.update_data(payment_type='phone')
    await callback_query.message.edit_text(f'Вы выбрали: перевод на телефон',
                                           reply_markup=keyboards.get_ikb_to_edit_payment_option())
    
    wait_message = await callback_query.message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    phone_creds = await gsh.async_execute_of_sync_gsheets(gsh.check_if_user_has_saved_creds,
                                                          user_id=callback_query.from_user.id,
                                                          creds_type='phone')
    await wait_message.delete()
    
    if phone_creds:
        await state.update_data(phone_number=phone_creds[0], mobile_operator=phone_creds[1])
        await callback_query.message.answer(f'Мы помним Вас. Проверьте Ваши данные:\n\n'
                                            f'Номер телефона:\n{phone_creds[0]}\n\n'
                                            f'Мобильный оператор:\n{phone_creds[1]}',
                                            reply_markup=keyboards.get_ikb_to_edit_phone_number())
        
        await callback_query.message.answer('Если все в порядке, то следующим сообщением пришлите ссылку на товар, '
                                            'под которым Вы оставили отзыв')
        await callback_query.message.answer('Чтобы найти ссылку на товар в мобильном приложении Wildberries:\n'
                                            '1. Зайдите на страницу товара;\n'
                                            '2. Нажмите в правом верхнем углу кнопку (она называется "Поделиться");\n'
                                            '3. В открывшемся меню выберите "Скопировать ссылку".\n\n'
                                            'Ссылка скопирована. Теперь вставьте ее в этот чат и отправьте.')
        
        await UserStates.get_product_link.set()
    
    else:
        await callback_query.message.answer(
            'Введите Ваш номер телефона в формате +74956667788')
        await UserStates.get_phone_number.set()


@dp.message_handler(state=UserStates.get_phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    if utils.is_valid_phone_number(message.text):
        await message.delete()
        await message.answer(f'Вы ввели номер телефона: {message.text}',
                             reply_markup=keyboards.get_ikb_to_edit_phone_number())
        await message.answer('Введите название Вашего мобильного оператора')
        
        await state.update_data(phone_number=message.text)
        
        await UserStates.get_mobile_operator.set()
        
        loop = asyncio.get_event_loop()
        loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.set_user_phone_number, user_id=message.from_user.id,
                                                           phone_number=message.text))
    
    else:
        await message.answer('Введите, пожалуйста, корректный номер телефона в формате:\n\n'
                             '+74956667788\n'
                             '+375291112233')


@dp.message_handler(state=UserStates.get_mobile_operator)
async def get_mobile_operator(message: types.Message, state: FSMContext):
    await state.update_data(mobile_operator=message.text)
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.set_user_mobile_operator, user_id=message.from_user.id,
                                                       mobile_operator=message.text))
    
    await message.answer('Следующим сообщением пришлите ссылку на товар, под которым Вы оставили отзыв')
    await message.answer('Чтобы найти ссылку на товар в мобильном приложении Wildberries:\n'
                                        '1. Зайдите на страницу товара;\n'
                                        '2. Нажмите в правом верхнем углу кнопку (она называется "Поделиться");\n'
                                        '3. В открывшемся меню выберите "Скопировать ссылку".\n\n'
                                        'Ссылка скопирована. Теперь вставьте ее в этот чат и отправьте.')
    await UserStates.get_product_link.set()


@dp.callback_query_handler(callback_data_models.set_bel_bank_cb_data.filter(), state='*')
async def get_bel_bank(callback_query: CallbackQuery, callback_data: dict):
    bel_bank = callback_data['bel_bank']
    await callback_query.message.edit_text(f'Вы выбрали банк: {bel_bank}',
                                           reply_markup=keyboards.get_ikb_to_edit_bel_bank())
    
    state = dp.get_current().current_state()
    await state.update_data(bel_bank=bel_bank)
    
    await callback_query.message.answer('Выберите категорию по которой мы можем перевести Вам деньги через ЕРИП',
                                        reply_markup=keyboards.get_ikb_to_choose_bel_bank_erip_info(bel_bank))
    
    await callback_query.answer()
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.set_user_bel_bank, user_id=callback_query.from_user.id,
                                                       bel_bank=bel_bank))


@dp.callback_query_handler(callback_data_models.set_bel_bank_category_cb_data.filter(), state='*')
async def get_bel_bank_category(callback_query: CallbackQuery, callback_data: dict):
    try:
        state = dp.get_current().current_state()
        data = await state.get_data()
        
        bel_bank = data['bel_bank']
        erip_category_index = int(callback_data['erip_category_index'])
        erip_category = utils.bel_bank_erip_categories[bel_bank][erip_category_index]
        erip_info = utils.bel_bank_category_cred_name[(bel_bank, erip_category)]
        
        await callback_query.message.edit_text(f'Вы выбрали категорию: {erip_category}',
                                               reply_markup=keyboards.get_ikb_to_edit_bel_bank())
        
        await state.update_data(bel_bank_category=erip_category)
        
        await callback_query.message.answer(erip_info)
        await UserStates.get_bel_bank_creds.set()
        
        await callback_query.answer()
        
        loop = asyncio.get_event_loop()
        loop.create_task(
            gsh.async_execute_of_sync_gsheets(gsh.set_user_bel_bank_category, user_id=callback_query.from_user.id,
                                              bel_bank_category=erip_category))
    
    except KeyError:
        wait_message = await callback_query.message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
        country = await gsh.async_execute_of_sync_gsheets(gsh.get_value, user_id=callback_query.from_user.id,
                                                          col_index=6)
        await wait_message.delete()
        await callback_query.message.answer('Извините, мы потеряли Ваши последние введенные данные... '
                                            'Выберите, пожалуйста, удобный способ получения бонуса',
                                            reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))


@dp.message_handler(state=UserStates.get_bel_bank_creds)
async def get_bel_bank_creds(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(bel_bank_creds=message.text)
    await message.answer(f'Вы выбрали ввели данные для пополнения карты:\n\n{message.text}',
                         reply_markup=keyboards.get_ikb_to_edit_bel_bank())
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.set_user_bel_bank_creds, user_id=message.from_user.id,
                                                       bel_bank_creds=message.text))
    
    await message.answer('Следующим сообщением пришлите ссылку на товар, под которым Вы оставили отзыв')
    await message.answer('Чтобы найти ссылку на товар в мобильном приложении Wildberries:\n'
                                        '1. Зайдите на страницу товара;\n'
                                        '2. Нажмите в правом верхнем углу кнопку (она называется "Поделиться");\n'
                                        '3. В открывшемся меню выберите "Скопировать ссылку".\n\n'
                                        'Ссылка скопирована. Теперь вставьте ее в этот чат и отправьте.')
    await UserStates.get_product_link.set()


@dp.message_handler(state=UserStates.get_product_link)
async def get_product_link(message: types.Message):
    state = dp.get_current().current_state()
    await state.update_data(product_link=message.text)
    
    await message.answer('Следующим сообщением пришлите скриншот Вашего отзыва')
    await UserStates.get_review_screenshot.set()


@dp.message_handler(state=UserStates.get_review_screenshot, content_types=['any'])
async def get_review_screenshot(message: types.Message, state: FSMContext):
    wait_message = await message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    country = await gsh.async_execute_of_sync_gsheets(gsh.get_value, user_id=message.from_user.id,
                                                      col_index=6)
    await wait_message.delete()
    
    try:
        data = await state.get_data()
        product_link = data['product_link']
        payment_type = data['payment_type']
        
        extra_message = f'Скриншот отзыва от пользователя {message.from_user.full_name} (@{message.from_user.username})' \
                        f'\n\nПродукт:\n{product_link}'
        
        if payment_type == 'bel_bank':
            bel_bank = data['bel_bank']
            bel_bank_creds = data['bel_bank_creds']
            erip_category = data['bel_bank_category']
            extra_message = f'{extra_message}\n\nСтрана: {country}\n\n' \
                            f'Банк: {bel_bank}\n\nКатегория: {erip_category}\n\nРеквизиты: `{bel_bank_creds}`\n\n' \
                            f'🟥🟥🟥🟥🟥🟥🟥\n' \
                            f'Статус: не выполнено'
            extra_message = utils.escape_special_characters(extra_message)
        
        elif payment_type == 'phone':
            phone_number = data['phone_number']
            mobile_operator = data['mobile_operator']
            extra_message = f'{extra_message}\n\nСтрана: {country}\n\n' \
                            f'Номер телефона для перевода: `{phone_number}`\n' \
                            f'Мобильный оператор: {mobile_operator}\n\n' \
                            f'🟥🟥🟥🟥🟥🟥🟥\n' \
                            f'Статус: не выполнено'
            extra_message = utils.escape_special_characters(extra_message)
        
        for manager_id in MANAGER_IDS:
            await utils.send_and_copy_message(bot, manager_id, message, extra_message,
                                              reply_markup=keyboards.get_ikb_to_mark_order_as_done(), divider=True)
        
        await message.answer('Спасибо за отзыв! Ваши данные отправлены менеджеру. '
                             'Как только он их увидит, Вы получите свой бонус.\n\n'
                             'Спасибо еще раз за покупку в магазине Veloman! Будем рады видеть Вас снова. '
                             'Если Вы оставили отзыв о другом нашем товаре, то нажмите кнопку под этим сообщением.',
                             reply_markup=keyboards.get_ikb_to_proceed_after_leaving_review())
        
        await state.finish()
    
    except KeyError:
        await state.finish()
        await message.answer('Извините, мы потеряли Ваши последние введенные данные... '
                             'Выберите, пожалуйста, удобный способ получения бонуса',
                             reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))


@dp.callback_query_handler(lambda c: c.data == 'edit_country', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Из какой Вы страны?', reply_markup=keyboards.get_ikb_to_set_country())
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'edit_payment_option', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    country = await gsh.async_execute_of_sync_gsheets(gsh.get_value, user_id=callback_query.from_user.id,
                                                      col_index=6)
    await callback_query.message.edit_text('Выберите наиболее удобный для Вас способ получения бонуса',
                                           reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'edit_phone_number', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer('Введите Ваш номер телефона в формате\n\n'
                                        '+74956667788\n'
                                        '+375291112233')
    await UserStates.get_phone_number.set()
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'edit_bel_bank', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Выберите банк:', reply_markup=keyboards.get_ikb_to_choose_belarusian_bank())
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'mark_order_as_done', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    new_text = callback_query.message.text[:-28] + '🟩🟩🟩🟩🟩🟩🟩\nСтатус: Выполнено'
    await callback_query.message.edit_text(new_text, reply_markup=None)
    await callback_query.answer()
    
    loop = asyncio.get_event_loop()
    loop.create_task(gsh.async_execute_of_sync_gsheets(gsh.submitted_review, user_id=callback_query.from_user.id))


@dp.callback_query_handler(lambda c: c.data == 'mark_order_as_fake', state='*')
async def payment_by_phone_rus(callback_query: types.CallbackQuery):
    new_text = callback_query.message.text[:-28] + '🟫🟫🟫🟫🟫🟫🟫\nСтатус: Фейковый отзыв'
    await callback_query.message.edit_text(new_text, reply_markup=None)
    await callback_query.answer()


@dp.message_handler(state='*', content_types=['any'])
async def get_review_screenshot(message: types.Message, state: FSMContext):
    await state.finish()
    wait_message = await message.answer('Мы кое-что проверяем, это может занять несколько секунд...')
    country = await gsh.async_execute_of_sync_gsheets(gsh.get_value, user_id=message.from_user.id,
                                                      col_index=6)
    await wait_message.delete()
    await message.answer('Извините, мы потеряли Ваши последние введенные данные... '
                         'Выберите, пожалуйста, удобный способ получения бонуса',
                         reply_markup=keyboards.get_ikb_to_choose_way_of_payment(country))


async def send_message_to_users_manually(user_ids_list: list, message):
    for user_id in user_ids_list:
        try:
            await bot.send_message(user_id, message)
            logger.info(f'message is sent to {user_id}')
        except ChatNotFound as x:
            logger.exception(x)
        except Exception as x:
            logger.exception(x)
        finally:
            await asyncio.sleep(0.036)


if __name__ == '__main__':
    with logger.catch():
        executor.start_polling(dispatcher=dp, skip_updates=True)
