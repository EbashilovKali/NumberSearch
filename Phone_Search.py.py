#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @name   : PhoneSearch
# @url    : https://github.com/sundowndev
# @author : (Ebashilov @linux_ebashilov)

import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone

def search_phone_number(phone_number):
    url = "https://mysmsbox.ru/phone-search/" + phone_number
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check response status code
    if response.status_code != 200:
        print("Error during request:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find elements with phone type, operator, and country record information
    phone_type = soup.find("span", string="Тип телефона:")
    operator = soup.find("span", string="Оператор:")
    country_record = soup.find("span", string="Запись внутри страны:")

    # Extract information if available
    if phone_type:
        phone_type = phone_type.find_next_sibling().get_text(strip=True)
    if operator:
        operator = operator.find_next_sibling().get_text(strip=True)
    if country_record:
        country_record = country_record.find_next_sibling().get_text(strip=True)

    # Search for Telegram account
    telegram_url = search_telegram(phone_number)

    # Search for social network information
    vk_profiles, vk_mentions, ok_profiles, ok_mentions, twitter_profile, twitter_mentions = search_social(phone_number)

    # Add search for messengers
    whatsapp_url, viber_url, skype_url = search_messengers(phone_number)

    return phone_type, operator, country_record, telegram_url, vk_profiles, vk_mentions, ok_profiles, ok_mentions, twitter_profile, twitter_mentions, whatsapp_url, viber_url, skype_url

def search_telegram(phone_number):
    telegram_url = f"https://t.me/{phone_number}"
    response = requests.get(telegram_url)

    if response.status_code == 200:
        return telegram_url
    else:
        return "Аккаунт не зарегестрирован"

def search_messengers(phone_number):
    whatsapp_url = f"https://wa.clck.bar/{phone_number}"
    viber_url = f"viber://chat?number={phone_number}"
    skype_url = f"skype:{phone_number}?chat"

    return whatsapp_url, viber_url, skype_url

def search_social(phone_number):
    base_url = f"https://mysmsbox.ru/phone-search/{phone_number}/social?s=1&mstrack=sphoneToolsSocial"
    response = requests.get(base_url)

    if response.status_code != 200:
        return None, None, None, None, None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find social network information
    vk_profiles = soup.find("a", string="ВК профили пользователей")
    if vk_profiles:
        vk_profiles = vk_profiles["href"]

    vk_mentions = soup.find("a", string="ВК упоминания номера")
    if vk_mentions:
        vk_mentions = vk_mentions["href"]

    ok_profiles = soup.find("a", string="ОДНОКЛАССНИКИ профили пользователя")
    if ok_profiles:
        ok_profiles = ok_profiles["href"]

    ok_mentions = soup.find("a", string="ОДНОКЛАССНИКИ упоминания номера")
    if ok_mentions:
        ok_mentions = ok_mentions["href"]

    twitter_profile = soup.find("a", string="TWITTER упоминания профиля")
    if twitter_profile:
        twitter_profile = twitter_profile["href"]

    twitter_mentions = soup.find("a", string="TWITTER упоминания номера")
    if twitter_mentions:
        twitter_mentions = twitter_mentions["href"]

    return vk_profiles, vk_mentions, ok_profiles, ok_mentions, twitter_profile, twitter_mentions

if __name__ == "__main__":
    phone_number = input("Введите номер телефона: ")
    phone_type, operator, country_record, telegram_url, vk_profiles, vk_mentions, ok_profiles, ok_mentions, twitter_profile, twitter_mentions, whatsapp_url, viber_url, skype_url = search_phone_number(phone_number)

    # Display information if it was obtained
    if phone_type or operator or country_record or telegram_url or vk_profiles or vk_mentions or ok_profiles or ok_mentions or twitter_profile or twitter_mentions or whatsapp_url or viber_url or skype_url:
        print("Тип телефона:", phone_type if phone_type else "Не указан")
        print("Оператор:", operator if operator else "Не указан")
        print("Запись внутри страны:", country_record if country_record else "Не указан")
        print("Telegram:", telegram_url if isinstance(telegram_url, str) else "Не найдено")

        print("ВК профили пользователей:", vk_profiles if vk_profiles else "Не найдено")
        print("ВК упоминания номера:", vk_mentions if vk_mentions else "Не найдено")
        print("ОДНОКЛАССНИКИ профили пользователя:", ok_profiles if ok_profiles else "Не найдено")
        print("ОДНОКЛАССНИКИ упоминания номера:", ok_mentions if ok_mentions else "Не найдено")
        print("TWITTER упоминания профиля:", twitter_profile if twitter_profile else "Не найдено")
        print("TWITTER упоминания номера:", twitter_mentions if twitter_mentions else "Не найдено")

        # Add messengers URLs
        print("WhatsApp:", whatsapp_url if whatsapp_url else "Не найдено")
        print("Viber:", viber_url if viber_url else "Не найдено")
        print("Skype:", skype_url if skype_url else "Не найдено")
    else:
        print("Не удалось получить информацию о номере телефона.")

    # Wait for user input before closing the program
    input("Нажмите Enter для выхода...")