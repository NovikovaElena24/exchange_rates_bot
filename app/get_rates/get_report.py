# Project imports
from get_rates.get_rates import get_mig_current_rate
from get_rates.get_rates import get_mig_official_rate
from get_rates.get_rates import get_cbr_official_rate
import logging


async def diff_rate(diff):
    if diff < 0:
        return f"(🔻{diff})"
    elif diff > 0:
        return f"(🔺{diff})"
    return f"(🟢{diff})"


async def alarm_mig_rate(
    mig_rates_buy, mig_rates_sell, last_buy_rates, last_sell_rates
):

    # Заголовок таблицы
    mig_rates_text = (
        f"❗️<b><u>Произошло значительное изменение курса по данным «МиГ» с момента последней рассылки:</u></b>\n\n"
        f"💰<b>Текущие курсы валют «МиГ»:</b>\n"
    )

    # Форматирование строк
    if mig_rates_buy and mig_rates_sell:
        mig_rates_text += f"\n<code>{'Валюта':<8}{'Покупка':<13}\n"
        for currency in sorted(mig_rates_buy):
            buy_rate = mig_rates_buy[currency]
            last_buy_rate = last_buy_rates[currency]
            diff_buy = await diff_rate(round(buy_rate - last_buy_rate, 2))
            mig_rates_text += f"{currency:<8}{buy_rate:<6}{diff_buy:<7}\n"
        mig_rates_text += "</code>"

        mig_rates_text += f"\n<code>{'Валюта':<8}{'Продажа':<13}\n"
        for currency in sorted(mig_rates_sell):
            sell_rate = mig_rates_sell[currency]
            last_sell_rate = last_sell_rates[currency]
            diff_sell = await diff_rate(round(sell_rate - last_sell_rate, 2))
            mig_rates_text += f"{currency:<8}{sell_rate:<6}{diff_sell:<7}\n"
        mig_rates_text += "</code>"
    else:
        mig_rates_text += "Не удалось получить данные, попробуйте запросить информацию позже командой /send_rates\n"
    return mig_rates_text


async def mig_rate(mig_rates_buy, mig_rates_sell):

    # Заголовок таблицы
    mig_rates_text = "💰<b><u>Курсы валют «МиГ»:</u></b>\n"

    # Форматирование строк
    if mig_rates_buy and mig_rates_sell:
        mig_rates_text += "\n<code>Валюта    Покупка   Продажа\n"
        for currency in sorted(mig_rates_buy):
            buy_rate = mig_rates_buy[currency]
            sell_rate = mig_rates_sell[currency]
            mig_rates_text += f"{currency:<10}{buy_rate:<10}{sell_rate:<7}\n"
        mig_rates_text += "</code>"
    else:
        mig_rates_text += "Не удалось получить данные, попробуйте запросить информацию позже командой /send_rates\n"
    return mig_rates_text


async def kz_rate(official_rates_kz):

    # Заголовок таблицы
    official_rates_kz_text = "🇵🇼<b><u>Курсы валют НБ РК:</u></b>\n"

    # Форматирование строк
    if official_rates_kz:
        official_rates_kz_text += "<code>"
        official_rates_kz_text += (
            "\n".join(
                f"{k:<10}{official_rates_kz[k]:<10}" for k in sorted(official_rates_kz)
            )
            + "\n</code>"
        )
    else:
        official_rates_kz_text += "Не удалось получить данные, попробуйте запросить информацию позже командой /send_rates\n"
    return official_rates_kz_text


async def ru_rate(official_rates_ru):

    # Заголовок таблицы
    official_rates_ru_text = "🇷🇺<b><u>Курсы валют ЦБ РФ:</u></b>\n"

    # Форматирование строк
    if official_rates_ru:
        official_rates_ru_text += "<code>"
        official_rates_ru_text += (
            "\n".join(f"{k:<10}{v:<10}" for k, v in official_rates_ru.items())
            + "\n</code>"
        )
    else:
        official_rates_ru_text += "Не удалось получить данные, попробуйте запросить информацию позже командой /send_rates\n"
    return official_rates_ru_text


async def get_message():
    # Получаем курс обменника "МиГ" с сайта https://mig.kz
    mig_rates_buy, mig_rates_sell = get_mig_current_rate()
    mig_rates_text = await mig_rate(mig_rates_buy, mig_rates_sell)

    # Получаем официальный курс НБ РК с сайта "https://mig.kz"
    official_rates_kz = get_mig_official_rate()
    official_rates_kz_text = await kz_rate(official_rates_kz)

    # Получаем официальный курс ЦБ РФ с сайта
    official_rates_ru = get_cbr_official_rate()
    official_rates_ru_text = await ru_rate(official_rates_ru)

    # Формируем сообщение для рассылки
    message = f"{mig_rates_text}\n{official_rates_kz_text}\n{official_rates_ru_text}"

    logging.debug(f"Сформировано сообщение для рассылки")
    return message, mig_rates_buy, mig_rates_sell
