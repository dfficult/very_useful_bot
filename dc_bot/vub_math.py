import discord
from discord import app_commands
from discord.app_commands import Choice
import random, math, statistics
from typing import Optional
import math2 as m


# 分數
@app_commands.command(name="simfrac", description="[分數] 約分分數")
@app_commands.describe(a="分子", b="分母")
async def simfrac(interaction: discord.Interaction, a: int, b: int):
    frac: m.Fraction = m.Fraction(a,b)
    frac.simplify()
    if frac.b == 1:
        t = f"約分：{frac.a}"
    else:
        t = f"約分：{frac.a} / {frac.b}"
    embed = discord.Embed(
        title=t,
        description=f"原分數：{a} / {b}",
        color=discord.Color.green()
    )
    embed.add_field(name="以小數表示", value=frac.to_float(), inline=True)
    embed.add_field(name="以百分率表示", value=f"{frac.to_percentage()}%", inline=True)
    await interaction.response.send_message(embed=embed)


# 解方程式
@app_commands.command(name="solve_21", description="[解方程式] 解二元一次方程式")
@app_commands.describe(eq1="第一式", eq2="第二式")
async def solve_21(interaction: discord.Interaction, eq1:str, eq2: str):

    # "3x+2-5=0" -> [["3x"],["-3"]]
    ...


# 數據分析
@app_commands.command(name="average", description="[數據分析] 計算算術平均數")
@app_commands.describe(items="輸入數個有理數，每項數值以空格分開")
async def average(interaction: discord.Interaction, items: str):
    nums = items.split(" ")
    try:
        nums = [float(i) for i in nums]
        result = sum(nums)/len(nums)
        embed=discord.Embed(
            title=f"算術平均：{result}",
            color=discord.Color.green()
        )
        for i in range(len(nums)):
            embed.add_field(name=f"第{i+1}個值",value=nums[i],inline=True)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description="輸入的值必須為有理數",
            color=discord.Color.red()
        )
        for i in range(len(nums)):
            embed.add_field(name=f"第{i+1}個值",value=nums[i],inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)



# 隨機
@app_commands.command(name="rand", description="[隨機] 隨機選擇一個")
@app_commands.describe(items="輸入選項，選項間以空格分開")
async def rand(interaction: discord.Interaction, items: str):
    choices: list = items.split(" ")
    rand_i = random.randint(0,len(choices)-1)
    s = choices[rand_i]
    embed = discord.Embed(
        title=f"隨機：{s}",
        description=items.replace(" ", ", "),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="dice", description="[隨機] 骰骰子")
@app_commands.describe(faces="骰子的面數 (正整數，可不填，預設為6)")
async def dice(interaction: discord.Interaction, faces: Optional[int]):
    if faces:
        ran = random.randint(1,faces)
    else:
        ran = random.randint(1,6)
    await interaction.response.send_message(ran)


# 排列、組合與機率
@app_commands.command(name="p", description="[排列組合] 計算從n個取k個，有多少種排列(Permutation)順序")
@app_commands.describe(n="n值。P(n,k)：從n個中，取k個進行排列", k="k值。P(n,k)：從n個中，取k個進行排列")
async def p(interaction: discord.Interaction, n: int, k: int):
    if n > 50:
        embed = discord.Embed(
            title="錯誤!",
            description="輸入的值必須<50",
            color=discord.Color.red()
        )
        embed.add_field(name="n值(正整數)",value=n,inline=True)
        embed.add_field(name="k值(正整數)",value=k,inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    try:
        result = math.perm(n,k)
    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description="輸入的值必須為正整數",
            color=discord.Color.red()
        )
        embed.add_field(name="n值(正整數)",value=n,inline=True)
        embed.add_field(name="k值(正整數)",value=k,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=f"排列：{result}種",
            description=f"P({n}, {k})",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

@app_commands.command(name="c", description="[排列組合] 計算從n個取k個，有多少種組合(Combination)")
@app_commands.describe(n="n值。C(n,k)：從n個中，取k個進行組合", k="k值。C(n,k)：從n個中，取k個進行組合")
async def c(interaction: discord.Interaction, n: int, k: int):
    try:
        result = math.comb(n,k)
    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description=f"輸入的值必須為正整數",
            color=discord.Color.red()
        )
        embed.add_field(name="n值(正整數)",value=n,inline=True)
        embed.add_field(name="k值(正整數)",value=k,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=f"組合：{result}種",
            description=f"C({n}, {k})",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)


# 三角函數
# @app_commands.command(name="tri2v", description="[三角函數] 給兩向量，求出所圍三角形的資訊")
# @app_commands.describe(
#     x0="A向量的x值", y0="A向量的y值", z0="A向量的z值 (若為平面向量，請填0)",
#     x1="B向量的x值", y1="B向量的y值", z1="B向量的z值 (若為平面向量，請填0)"
# )
# async def tri2v(
#     interaction: discord.Interaction,
#     x0: int, y0: int, z0: int,
#     x1: int, y1: int, z1: int
# ):
#     embed = discord.Embed(
#         title="三角形",
#         color=discord.Color.green()
#     )
    
#     # area = 1/2 * |(x0,y0,z0) X (x1,y1,z1)|
#     a = m.Fraction(1,2)
#     s = m.sim_sqrt(pow(y0*z1-z0*y1,2) + pow(z0*x1-z0*z1,2) + pow(x0*y1-y0*x1,2))
#     a.multiply(m.Fraction(s[0],1))
#     b = s[1]
#     area = f"{a.a} √{b}" if a.b == 1 else f"{a.a}/{a.b} √{b}"
#     embed.add_field(name="面積", value=area, inline=True)

#     side1_sq = x0*x0+y0*y0+z0*z0
#     side2_sq = x1*x1+y1*y1+z1*z1
#     # vector a dot b = abcosθ
#     theta = math.acos((x0*x1+y0*y1+z0*z1)/ math.sqrt(side1_sq*side2_sq))
#     side3_sq = pow(side1_sq,2) + pow(side2_sq) - 2*math.sqrt()



# 向量
@app_commands.command(name="vector", description="[向量] 計算向量、向量的內積、向量的外積")
@app_commands.describe(
        x0="A點/A向量的x值",
        y0="A點/A向量的y值",
        z0="A點/A向量的z值(若為平面，輸入0)",
        action="選擇運算",
        x1="B點/B向量的x值",
        y1="B點/B向量的y值",
        z1="B點/B向量的z值(若為平面，輸入0)"
)
@app_commands.choices(
        action=[
                Choice(name="to", value="to"),
                Choice(name="dot", value="dot"),
                Choice(name="cross", value="cross")
        ]
)
async def vector(
    interaction: discord.Interaction,
    x0: int, y0: int, z0: int,
    action: Choice[str],
    x1: int, y1: int, z1: int
):
    
    a = (x0, y0, z0)
    b = (x1, y1, z1)
    
    match action.value:
        case "to":
            # 計算向量
            ab = (x1-x0, y1-y0, z1-z0)
            length = m.sim_sqrt(ab[0]*ab[0]+ab[1]*ab[1]+ab[2]*ab[2])
            if length[0] == 1:
                t = f"向量長度：√{length[1]}"
            elif length[1] == 1:
                t = f"向量長度：{length[1]}"
            else:
                t = f"向量長度：{length[0]}√{length[1]}"

            embed = discord.Embed(
                title=f"AB向量：{ab}",
                description=t,
                color=discord.Color.green()
            )
            embed.add_field(name="A點", value=a, inline=True)
            embed.add_field(name="B點", value=b, inline=True)
            await interaction.response.send_message(embed=embed)
        case "dot":
            # 內積
            a_dot_b = x0*x1 + y0*y1 + z0*z1
            embed = discord.Embed(
                title=f"內積：{a_dot_b}",
                color=discord.Color.green()
            )
            embed.add_field(name="A向量", value=a, inline=True)
            embed.add_field(name="B向量", value=b, inline=True)
            await interaction.response.send_message(embed=embed)
        case "cross":
            # 外積
            # |y0 z0| |z0 x0| |x0 y0|
            # |y1 z1|,|z1 x1|,|x1 y1|

            o = [
                y0*z1 - z0*y1,
                z0*x1 - x0*z1,
                x0*y1 - y0*x1
            ]
            length = m.sim_sqrt(o[0]*o[0]+o[1]*o[1]+o[2]*o[2])
            if length[0] == 1:
                t = f"向量長度：√{length[1]}"
            elif length[1] == 1:
                t = f"向量長度：{length[1]}"
            else:
                t = f"向量長度：{length[0]}√{length[1]}"

            embed = discord.Embed(
                title=f"外積：({o[0]}, {o[1]}, {o[2]})",
                description=t,
                color=discord.Color.green()
            )
            embed.add_field(name="A向量", value=a, inline=True)
            embed.add_field(name="B向量", value=b, inline=True)
            await interaction.response.send_message(embed=embed)

@app_commands.command(name="vectorl", description="[向量] 計算向量的長度")
@app_commands.describe(x="x值",y="y值",z="z值 (若為平面向量，輸入0)")
async def vectorl(interaction: discord.Interaction, x: int, y: int, z: int):
        length = m.sim_sqrt(x*x + y*y + z*z)
        if length[0] == 1:
            t = f"向量長度：√{length[1]}"
        elif length[1] == 1:
            t = f"向量長度：{length[1]}"
        else:
            t = f"向量長度：{length[0]}√{length[1]}"

        embed = discord.Embed(
            title=t,
            color=discord.Color.green()
        )
        embed.add_field(name="向量", value=f"({x}, {y}, {z})", inline=True)
        await interaction.response.send_message(embed=embed)  

# 平面
@app_commands.command(name="surface", description="[平面] 給一法向量與平面上一點，求出該平面的一般式")
@app_commands.describe(
    nx="法向量的x值",
    ny="法向量的y值",
    nz="法向量的z值",
    x="平面上任意點的x值",
    y="平面上任意點的y值",
    z="平面上任意點的z值"
)
async def surface(
    interaction: discord.Interaction,
    nx: int, ny: int, nz: int,
    x: int, y: int, z: int
):
    d = nx*x + ny*y + nz*z
    surf = f"{nx}x{'+' if ny>0 else ''}{ny}y{'+' if nz>0 else ''}{nz}z={d}"
    embed = discord.Embed(
        title=f"平面(未化簡)：{surf}",
        color=discord.Color.green()
    )
    embed.add_field(name="法向量", value=f"({nx}, {ny}, {nz})", inline=True)
    embed.add_field(name="任一點", value=f"({x}, {y}, {z})", inline=True)
    await interaction.response.send_message(embed=embed)


# 行列式與矩陣
@app_commands.command(name="det3", description="[行列式] 計算三階行列式(determinant)之值")
@app_commands.describe(
    a1="第1列，第1行 (左上) (橫列直行)",
    a2="第1列，第2行 (中上) (橫列直行)",
    a3="第1列，第3行 (右上) (橫列直行)",
    b1="第2列，第1行 (左中) (橫列直行)",
    b2="第2列，第2行 (中間) (橫列直行)",
    b3="第2列，第3行 (右中) (橫列直行)",
    c1="第3列，第1行 (左下) (橫列直行)",
    c2="第3列，第2行 (中下) (橫列直行)",
    c3="第3列，第3行 (右下) (橫列直行)",
)
async def det3(
    interaction: discord.Interaction,
    a1: int, a2: int, a3: int,
    b1: int, b2: int, b3: int,
    c1: int, c2: int, c3: int
):
    # |a1 a2 a3|
    # |b1 b2 b3|
    # |c1 c2 c3|
    result = a1*b2*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1 - a2*b1*c3 - a1*b3*c2
    
    # Format width
    width = max([len(str(i)) for i in [a1,a2,a3,b1,b2,b3,c1,c2,c3]])
    
    embed = discord.Embed(
        title=f"行列式：{result}",
        description=
        f"|{a1: {width}d} {a2: {width}d} {a3: {width}d}|\n|{b1: {width}d} {b2: {width}d} {b3: {width}d}|\n|{c1: {width}d} {c2: {width}d} {c3: {width}d}|",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="det2", description="[行列式] 計算二階行列式(determinant)之值")
@app_commands.describe(
    a1="第1列，第1行 (左上) (橫列直行)",
    a2="第1列，第2行 (右上) (橫列直行)",
    b1="第2列，第1行 (左下) (橫列直行)",
    b2="第2列，第2行 (右下) (橫列直行)",
)
async def det2(
    interaction: discord.Interaction,
    a1: int, a2: int,
    b1: int, b2: int,
):
    # |a1 a2|
    # |b1 b2|
    result = a1*b2 - a2*b1
    
    # Format width
    width = max([len(str(i)) for i in [a1,a2,b1,b2]])
    
    embed = discord.Embed(
        title=f"行列式：{result}",
        description=
        f"|{a1: {width}d} {a2: {width}d}|\n|{b1: {width}d} {b2: {width}d}|",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

