import discord
from discord import app_commands
import os, json, datetime
import settings
from discord.app_commands import Choice, Range
from lang import *


def get_user_wallet(user_id: int) -> dict:
    path = f"assets/expenses/{user_id}.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        with open(path, 'w') as f:
            user_wallet = {
                "name": user_id,
                "balance": 0,
                "history": [{
                    "date": datetime.datetime.now().strftime("%Y%m%d_%H%M"),
                    "amount": 0,
                    "category": text("expenses.categories.other_income"),
                    "description": text("expenses.initialize"),
                    "balance": 0
                }]
            }
            f.write(json.dumps(user_wallet, indent=4, ensure_ascii=False))
        return user_wallet


income_categories = [
    text("expenses.categories.main_income"),
    text("expenses.categories.side_job"),
    text("expenses.categories.investment"),
    text("expenses.categories.borrow"),
    text("expenses.categories.other_income")
]
expense_categories = [
    text("expenses.categories.monthly_expenses"),
    text("expenses.categories.food"),
    text("expenses.categories.transportation"),
    text("expenses.categories.entertainment"),
    text("expenses.categories.education"),
    text("expenses.categories.donation"),
    text("expenses.categories.lend"),
    text("expenses.categories.other_expenses")
]


@app_commands.command(name="m_wallet", description=text("cmd.m_wallet.description"))
async def m_wallet(interaction: discord.Interaction):
    user_wallet = get_user_wallet(interaction.user.id)
    embed = discord.Embed(
        title=text("cmd.m_wallet.someones_wallet", interaction.user.name),
        description=text("cmd.m_wallet.your_balance", user_wallet['balance']),
        color=settings.Colors.money,
        timestamp=datetime.datetime.now()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.command(name="m_new_record", description=text("cmd.m_new_record.description"))
@app_commands.describe(amount=text("cmd.m_new_record.amount"), category=text("cmd.m_new_record.category"), description=text("cmd.m_new_record.des"))
@app_commands.choices(
    category = [Choice(name=text("cmd.m_new_record.income", i), value=i) for i in income_categories] + [Choice(name=text("cmd.m_new_record.expense", i), value=i) for i in expense_categories]
)
async def m_new_record(interaction: discord.Interaction, amount: Range[int, 1, None], category: Choice[str], description: str):
    # get user wallet
    user_wallet = get_user_wallet(interaction.user.id)
    # income or expense
    if amount < 0: amount = amount * -1
    amount = amount * -1 if category.value in expense_categories else amount
    # transaction
    this = {
        "date": datetime.datetime.now().strftime("%Y%m%d_%H%M"),
        "amount": amount,
        "category": category.value,
        "description": description,
        "balance": user_wallet['balance'] + amount
    }
    user_wallet['history'].append(this)
    user_wallet['balance'] = this['balance']
    # sync to json file
    with open(f"assets/expenses/{interaction.user.id}.json", 'w') as f:
        f.write(json.dumps(user_wallet, indent=4, ensure_ascii=False))
    # embed
    embed = discord.Embed(
        title=f"+ {this['amount']}" if this['amount']>0 else this['amount'],
        description=this['description'],
        color=settings.Colors.money,
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name=text("cmd.m_new_record.category"), value=this["category"])
    embed.add_field(name=text("cmd.m_new_record.balance"), value=this["balance"])
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@app_commands.command(name="m_history", description=text("cmd.m_history.description"))
async def m_history(interaction: discord.Interaction):
    # Coming soon
    ...
