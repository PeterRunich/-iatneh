from ..kb.main_menu import main_menu_builder

async def handler(msg, state=None):
    await msg.delete()
    await state.finish()

    kb = main_menu_builder()
    await msg.answer('Главное меню', reply_markup=kb)
