import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import setup_database
from handlers.user import start, shop, cart, order
from handlers.admin import add_product, admin_orders
from handlers.admin import admin_menu
from handlers.user import start, shop

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    setup_database()

    dp.include_router(start.router)
    dp.include_router(shop.router)
    dp.include_router(cart.router)
    dp.include_router(order.router)
    dp.include_router(add_product.router)
    dp.include_router(admin_orders.router)
    dp.include_router(admin_menu.router)


    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


