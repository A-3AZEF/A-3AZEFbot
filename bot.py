from telethon import TelegramClient, events, functions
import asyncio
import pytz
from datetime import datetime
from keep_alive import keep_alive


# بياناتك
api_id = 26845245
api_hash = '0d17e3caac8b751aa91089cebf3e2439'
SESSION = "1BJWap1sBu5cSA0qzs_HsnhRvQs3_jBOlsOzT-oe-E0xNl2G5YLACUBANGOYaC2n2av7alHrl_5BcC8vrEOZtW_VnZaPtWf5oodbgREhCOS9QdrHSoc1NfO_TOBGdYagMdrLoZd2KaETSe2OiR2Re8cZiadXMKfb-EKrUnrwgf4FHwJyRwN0CrdQ4RbyKmaJtonG23h7WRktU932K_Ro8FQVPXvJdzk5ctw0ozfv1dAV23nGB6kq2UB7twHyvMYtqWFUIO7l3ECvSwJylTmzA944UbEE3I6KipozpQLGNsrdffAsAZCpHDfbpRqgVwAkBn_pVygZJaNcaCvgCz5Tt8kbtdxw72O8="
OWNER_ID = 6211998691  # ID الخاص بك

client = TelegramClient('mysession', api_id, api_hash)
muted_users = set()
away_mode = True

# 🕒 تحويل الوقت إلى شكل مزخرف
def fancy_time(text):
    mapping = {
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗', ':': ':'
    }
    return ''.join([mapping.get(c, c) for c in text])

# ⏰ تحديث الاسم بالساعة المزخرفة
async def update_profile_name():
    while True:
        try:
            egypt_tz = pytz.timezone("Africa/Cairo")
            now = datetime.now(egypt_tz)
            current_time = now.strftime("%H:%M")
            fancy = fancy_time(current_time)

            me = await client.get_me()

            if me.first_name != fancy:
                await client(functions.account.UpdateProfileRequest(
                    first_name=fancy
                ))
        except Exception as e:
            print(f"[خطأ في تحديث الاسم]: {e}")

        await asyncio.sleep(60)

# 📌 كتم الشات الحالي
@client.on(events.NewMessage(pattern=r"\.كتم$"))
async def mute_current_chat_user(event):
    if event.sender_id != OWNER_ID:
        return
    try:
        chat = await event.get_input_chat()
        target_id = chat.user_id if hasattr(chat, 'user_id') else event.chat_id
        muted_users.add(target_id)
        await event.respond("✅ تم كتم الشات الحالي.")
    except Exception as e:
        await event.respond(f"❌ حصل خطأ أثناء الكتم: {e}")

# 📌 فك الكتم
@client.on(events.NewMessage(pattern=r"\.الغاء كتم$"))
async def unmute_current_chat_user(event):
    if event.sender_id != OWNER_ID:
        return
    try:
        chat = await event.get_input_chat()
        target_id = chat.user_id if hasattr(chat, 'user_id') else event.chat_id

        if target_id in muted_users:
            muted_users.remove(target_id)
            await event.respond("✅ تم إلغاء كتم الشات الحالي.")
        else:
            await event.respond("❌ هذا الشات غير مكتوم.")
    except Exception as e:
        await event.respond(f"❌ حصل خطأ أثناء إلغاء الكتم: {e}")

# 📝 عرض المكتومين
@client.on(events.NewMessage(pattern=r"\.المكتومين"))
async def list_muted_users(event):
    if event.sender_id != OWNER_ID:
        return
    if not muted_users:
        await event.respond("📭 لا يوجد أي شات مكتوم حالياً.")
    else:
        text = "📋 قائمة الشاتات المكتومة:\n\n"
        for user_id in muted_users:
            try:
                entity = await client.get_entity(user_id)
                name = f"• [{getattr(entity, 'title', getattr(entity, 'first_name', 'غير معروف'))}](tg://user?id={user_id})"
            except:
                name = f"• شات غير معروف - ID: {user_id}"
            text += name + "\n"
        await event.respond(text)

# 🧾 قائمة الأوامر المزخرفة
@client.on(events.NewMessage(pattern=r"\.اوامر"))
async def show_commands(event):
    if event.sender_id != OWNER_ID:
        return
    msg = (
        "╔═══════《⛧ أوامـر سـورس 𝟑𝑨𝒁𝑬𝑭 ⛧》═══════╗\n\n"
        "⌯ .كـتـم ⌯ كتم الشات الحالي\n"
        "⌯ .الغـاء كـتـم ⌯ فك الكتم عن الشات الحالي\n"
        "⌯ .المكـتومين ⌯ عرض الشاتات المكتومة\n"
        "⌯ .سـبام [كلمة] [عدد] ⌯ سبام برسائل منفصلة\n"
        "⌯ .انشاء جروب [عدد] ⌯ جروبات + بوستات + حذف\n"
        "⌯ .نشر تلقائي [رسالة] ⌯ نشر في جميع الجروبات\n"
        "⌯ .اون ⌯ تفعيل الرد التلقائي\n"
        "⌯ .اوف ⌯ إيقاف الرد التلقائي\n"
        "⌯ .اوامـر ⌯ عرض هذه القائمة\n\n"
        "╚═══════《 𝑺𝑶𝑼𝑹𝑪𝑬 𝟑𝑨𝒁𝑬𝑭 ⛧ 》═══════╝\n"
        "⌯ المطور: [@T_8l8](https://t.me/T_8l8)"
    )
    await event.respond(msg, link_preview=False)

# 📣 سبام
@client.on(events.NewMessage(pattern=r"\.سبام (.+)"))
async def spam_handler(event):
    if event.sender_id != OWNER_ID:
        return
    args = event.pattern_match.group(1).split(" ")
    if len(args) < 2:
        await event.respond("❌ الاستخدام: .سبام [كلمة أو جملة] [عدد]")
        return

    text = " ".join(args[:-1])
    try:
        count = int(args[-1])
    except ValueError:
        await event.respond("❌ العدد يجب أن يكون رقم صحيح.")
        return

    await event.respond(f"📤 سبام {text} عدد: {count}")
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(0.2)

# 🛠 إنشاء جروبات
@client.on(events.NewMessage(pattern=r"\.انشاء جروب (\d+)"))
async def create_groups(event):
    if event.sender_id != OWNER_ID:
        return
    try:
        count = int(event.pattern_match.group(1))
        await event.respond(f"🚀 جاري إنشاء {count} جروب...\n⏳ برجاء الانتظار")

        for i in range(1, count + 1):
            group_name = f"جروب {i}"
            try:
                result = await client(functions.messages.CreateChatRequest(
                    users=[event.sender_id],
                    title=group_name
                ))
                chat = result.chats[0]

                for j in range(1, 8):
                    await client.send_message(chat.id, f"📌 البوست رقم {j} في {group_name}")
                    await asyncio.sleep(0.2)

                await asyncio.sleep(1)

                await client(functions.messages.DeleteChatUserRequest(
                    chat_id=chat.id,
                    user_id='me'
                ))

                await event.respond(f"✅ تم إنشاء وحذف {group_name}")
                await asyncio.sleep(1)

            except Exception as e:
                await event.respond(f"❌ خطأ في {group_name}: {e}")
                continue

        await event.respond("✅ تم الانتهاء من كل الجروبات.")

    except Exception as e:
        await event.respond(f"❌ حصل خطأ: {e}")

# 💬 الرد التلقائي تشغيل/إيقاف
@client.on(events.NewMessage(pattern=r"\.اون"))
async def enable_auto_reply(event):
    if event.sender_id != OWNER_ID:
        return
    global away_mode
    away_mode = True
    await event.respond("✅ تم تفعيل الرد التلقائي.")

@client.on(events.NewMessage(pattern=r"\.اوف"))
async def disable_auto_reply(event):
    if event.sender_id != OWNER_ID:
        return
    global away_mode
    away_mode = False
    await event.respond("❌ تم إيقاف الرد التلقائي.")

# 🤖 الرد التلقائي عند التفعيل
@client.on(events.NewMessage(incoming=True))
async def auto_reply_when_away(event):
    if away_mode and event.is_private and not event.out:
        await event.reply("3AZEF مش موجود دلوقتي")

# 🧼 حذف رسائل المكتومين تلقائيًا
@client.on(events.NewMessage())
async def auto_delete(event):
    if event.chat_id in muted_users and not event.out:
        await event.delete()

# 📤 نشر تلقائي في الجروبات
@client.on(events.NewMessage(pattern=r"\.نشر تلقائي (.+)"))
async def auto_broadcast_to_groups(event):
    if event.sender_id != OWNER_ID:
        return
    message = event.pattern_match.group(1)
    await event.respond("📣 جاري النشر في كل الجروبات...")

    count = 0
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            try:
                await client.send_message(dialog.id, message)
                count += 1
                await asyncio.sleep(0.3)
            except:
                continue

    await event.respond(f"✅ تم إرسال الرسالة إلى {count} جروب.")

# 🚀 تشغيل البوت وتحديث الاسم
keep_alive()
client.start()
client.loop.create_task(update_profile_name())

client.run_until_disconnected()
