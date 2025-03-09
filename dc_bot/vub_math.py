# === vub_math.py ===
import discord
from discord import app_commands
from discord.app_commands import Choice
import random, math, statistics
from typing import Optional
import math_module as m
import settings


# --- Command: simfrac ---
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
        color=settings.Colors.math
    )
    embed.add_field(name="以小數表示", value=frac.to_float(), inline=True)
    embed.add_field(name="以百分率表示", value=f"{frac.to_percentage()}%", inline=True)
    await interaction.response.send_message(embed=embed)


# --- Command: factorize ---
@app_commands.command(name="factorize", description="[分數] 質因數分解")
@app_commands.describe(n="輸入要進行質因數分解的整數")
async def factorize(interaction: discord.Interaction, n: int):
    x = m.factorize(n)
    x.sort()
    t = f"{n}是質數" if len(x) == 1 else x
    embed = discord.Embed(
        title=f"質因數分解{n}：",
        description=t,
        color=settings.Colors.math
    )
    await interaction.response.send_message(embed=embed)


# --- Command: solve21 ---
@app_commands.command(name="solve21", description="[解方程式] 解二元一次方程式")
@app_commands.describe(eq1="第一式", eq2="第二式")
async def solve21(interaction: discord.Interaction, eq1:str, eq2: str):
    try:
        s = m.solve_21(eq1, eq2)
        d = ""
        t = "此方程組恰有一解"
        for key, value in s.items():
            if type(value) == bool:
                if value == False:
                    t = "此方程組無解"
                    break
                if value == True:
                    t = "此方程組有無限多解"
                    break
            else:
                if type(value) == m.Fraction:
                    value = f"{value.a}/{value.b}"
                d += f"{key}={value}\n"
        embed = discord.Embed(
            title=t,
            description=d,
            color=settings.Colors.math
        )
        embed.add_field(name=f"第一式",value=eq1,inline=True)
        embed.add_field(name=f"第二式",value=eq2,inline=True)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description="發生錯誤",
            color=settings.Colors.fail
        )
        embed.add_field(name=f"第一式",value=eq1,inline=True)
        embed.add_field(name=f"第二式",value=eq2,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# --- Command: solve31 ---
@app_commands.command(name="solve31", description="[解方程式] 解三元一次方程式")
@app_commands.describe(eq1="第一式", eq2="第二式", eq3="第三式")
async def solve31(interaction: discord.Interaction, eq1:str, eq2: str, eq3: str):
    try:
        s = m.solve_31(eq1, eq2, eq3)
        d = ""
        t = "此方程組恰有一解"
        for key, value in s.items():
            if type(value) == bool:
                if value == False:
                    t = "此方程組無解"
                    break
                if value == True:
                    t = "此方程組有無限多解"
                    break
            else:
                if type(value) == m.Fraction:
                    value = f"{value.a}/{value.b}"
                d += f"{key}={value}\n"
        embed = discord.Embed(
            title=t,
            description=d,
            color=settings.Colors.math
        )
        embed.add_field(name=f"第一式",value=eq1,inline=True)
        embed.add_field(name=f"第二式",value=eq2,inline=True)
        embed.add_field(name=f"第三式",value=eq3,inline=True)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description="發生錯誤",
            color=settings.Colors.fail
        )
        embed.add_field(name=f"第一式",value=eq1,inline=True)
        embed.add_field(name=f"第二式",value=eq2,inline=True)
        embed.add_field(name=f"第三式",value=eq3,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# --- Command: average ---
@app_commands.command(name="average", description="[數據分析] 計算算術平均數")
@app_commands.describe(items="輸入數個有理數，每項數值以空格分開")
async def average(interaction: discord.Interaction, items: str):
    nums = items.split(" ")
    try:
        nums = [float(i) for i in nums]
        result = sum(nums)/len(nums)
        embed=discord.Embed(
            title=f"算術平均：{result}",
            color=settings.Colors.math
        )
        for i in range(len(nums)):
            embed.add_field(name=f"第{i+1}個值",value=nums[i],inline=True)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description="輸入的值必須為有理數",
            color=settings.Colors.fail
        )
        for i in range(len(nums)):
            embed.add_field(name=f"第{i+1}個值",value=nums[i],inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)


# --- Command: correlation ---
@app_commands.command(name="correlation", description="[數據分析] 計算相關係數")
@app_commands.describe(x="輸入第一組數據，數字間以空格隔開", y="輸入第二組數據，數字間以空格隔開")
async def correlation(interaction: discord.Interaction, x: str, y: str):
    xi = x.split(" ")
    yi = y.split(" ")
    if len(xi) != len(yi):
        await interaction.response.send_message("err1")
    
    xi = [int(i) for i in xi]
    yi = [int(i) for i in yi]
    ax = sum(xi) / len(xi)  # average x
    ay = sum(yi) / len(yi)  # average y
    xi_ax = [i - ax for i in xi]  # x離均差
    yi_ay = [i - ay for i in yi]  # y離均差
    xaya = [xi_ax[i] * yi_ay[i] for i in range(len(xi))]  # 上面兩個相乘
    xi_ax_2 = [i * i for i in xi_ax]  # x離均差平方
    yi_ay_2 = [i * i for i in yi_ay]  # y離均差平方

    def is_int(n: float) -> bool:
        return n % 1 == 0

    print(sum(xaya), sum(xi_ax_2), sum(yi_ay_2))

    # r = xaya / (√xi_ax_2 * √yi_ay_2)
    if is_int(sum(xaya)) and is_int(sum(xi_ax_2)) and is_int(sum(yi_ay_2)):
        fa = int(sum(xaya))  # 分子
        fb = m.sim_sqrt(int(sum(xi_ax_2) * sum(yi_ay_2)))  # 分母
        if fb[1] == 1:
            frac = m.Fraction(fa,fb[0])
            frac.simplify()
            r = [frac, 1]
            if r[0].b == 1:
                des = f"{r[0].a}"
            else:
                des = f"{r[0].a} / {r[0].b}"
        else:
            frac = m.Fraction(fa,fb[0]*fb[1])
            frac.simplify()
            r = [frac,fb[1]]
            if r[0].b == 1:
                des = f"{r[0].a} * √{r[1]}"
            else:
                des = f"{r[0].a} / {r[0].b} * √{r[1]}"
    else:
        des = sum(xaya) / (math.sqrt(sum(xi_ax_2)) * math.sqrt(sum(yi_ay_2)))


    embed = discord.Embed(
        title="相關係數",
        description=des,
        color=settings.Colors.math
    )
    embed.add_field(name="x資料", value=tuple(xi))
    embed.add_field(name="y資料", value=tuple(yi))
    await interaction.response.send_message(embed=embed)


# --- Command: rand ---
@app_commands.command(name="rand", description="[隨機] 隨機選擇一個")
@app_commands.describe(items="輸入選項，選項間以空格分開", amount="選取的數量 (正整數，可不填，預設為1，輸入0會選出隨機個)")
async def rand(interaction: discord.Interaction, items: str, amount: Optional[int]):
    choices: list = items.split(" ")
    if (not amount and amount != 0) or amount < 0 or amount > len(choices):
        rand_i = random.randint(0,len(choices)-1)
        s = choices[rand_i]
        embed = discord.Embed(
            title=f"隨機：{s}",
            description=items.replace(" ", ", "),
            color=settings.Colors.math
        )
    else:
        if amount == 0: amount = random.randint(2,len(choices))
        # amount
        for i in range(len(choices)-amount):
            rand_i = random.randint(0,len(choices)-1)
            choices.pop(rand_i)
        # random order
        for i in range(len(choices)):
            i1 = random.randint(0, len(choices)-1)
            i2 = random.randint(0, len(choices)-1)
            choices[i1], choices[i2] = choices[i2], choices[i1]
        s = str(choices).replace('[','').replace(']','').replace("'",'')
        embed = discord.Embed(
            title=f"隨機取{amount}個：{s}",
            description=items.replace(" ", ", "),
            color=settings.Colors.math
        )  
    await interaction.response.send_message(embed=embed)


# --- Command: dice ---
@app_commands.command(name="dice", description="[隨機] 骰骰子")
@app_commands.describe(faces="骰子的面數 (正整數，可不填，預設為6)")
async def dice(interaction: discord.Interaction, faces: Optional[int]):
    if faces:
        ran = random.randint(1,faces)
    else:
        ran = random.randint(1,6)
    await interaction.response.send_message(ran)


# --- Command: p ---
@app_commands.command(name="p", description="[排列組合] 計算從n個取k個，有多少種排列(Permutation)順序")
@app_commands.describe(n="n值。P(n,k)：從n個中，取k個進行排列", k="k值。P(n,k)：從n個中，取k個進行排列")
async def p(interaction: discord.Interaction, n: int, k: int):
    if n > 50:
        embed = discord.Embed(
            title="錯誤!",
            description="輸入的值必須<50",
            color=settings.Colors.fail
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
            color=settings.Colors.fail
        )
        embed.add_field(name="n值(正整數)",value=n,inline=True)
        embed.add_field(name="k值(正整數)",value=k,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=f"排列：{result}種",
            description=f"P({n}, {k})",
            color=settings.Colors.math
        )
        await interaction.response.send_message(embed=embed)


# --- Command: c ---
@app_commands.command(name="c", description="[排列組合] 計算從n個取k個，有多少種組合(Combination)")
@app_commands.describe(n="n值。C(n,k)：從n個中，取k個進行組合", k="k值。C(n,k)：從n個中，取k個進行組合")
async def c(interaction: discord.Interaction, n: int, k: int):
    try:
        result = math.comb(n,k)
    except Exception as e:
        embed = discord.Embed(
            title="錯誤!",
            description=f"輸入的值必須為正整數",
            color=settings.Colors.fail
        )
        embed.add_field(name="n值(正整數)",value=n,inline=True)
        embed.add_field(name="k值(正整數)",value=k,inline=True)
        embed.add_field(name="具體錯誤",value=e)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=f"組合：{result}種",
            description=f"C({n}, {k})",
            color=settings.Colors.math
        )
        await interaction.response.send_message(embed=embed)


# --- Command: vector ---
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
                color=settings.Colors.math
            )
            embed.add_field(name="A點", value=a, inline=True)
            embed.add_field(name="B點", value=b, inline=True)
            await interaction.response.send_message(embed=embed)
        case "dot":
            # 內積
            a_dot_b = x0*x1 + y0*y1 + z0*z1
            embed = discord.Embed(
                title=f"內積：{a_dot_b}",
                color=settings.Colors.math
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
                color=settings.Colors.math
            )
            embed.add_field(name="A向量", value=a, inline=True)
            embed.add_field(name="B向量", value=b, inline=True)
            await interaction.response.send_message(embed=embed)


# --- Command: vectorl ---
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
            color=settings.Colors.math
        )
        embed.add_field(name="向量", value=f"({x}, {y}, {z})", inline=True)
        await interaction.response.send_message(embed=embed)  


# --- Command: surface ---
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
        color=settings.Colors.math
    )
    embed.add_field(name="法向量", value=f"({nx}, {ny}, {nz})", inline=True)
    embed.add_field(name="任一點", value=f"({x}, {y}, {z})", inline=True)
    await interaction.response.send_message(embed=embed)


# --- Command: det3 ---
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
        color=settings.Colors.math
    )
    await interaction.response.send_message(embed=embed)


# --- Command: det2 ---
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
        color=settings.Colors.math
    )
    await interaction.response.send_message(embed=embed)


# --- Command: intrmtx2 ---
@app_commands.command(name="invrmtx2", description="[矩陣] 求出二階反方陣(inverse Matrix)")
@app_commands.describe(
    a="第1列，第1行 (左上) (橫列直行)",
    b="第1列，第2行 (右上) (橫列直行)",
    c="第2列，第1行 (左下) (橫列直行)",
    d="第2列，第2行 (右下) (橫列直行)"
)
async def invrmtx2(
    interaction: discord.Interaction,
    a: int, b: int,
    c: int, d: int
):
    # A = ⌈a b⌉, A^-1 = ⌈d/det(A) -b/det(A)⌉
    #     ⌊c d⌋         ⌊-c/det(A) a/det(A)⌋
    # 
    # det(A) = |a b|, no inverse if det(A)=0
    #          |c d|
    det = a * d - b * c
    has_invr = True if det != 0 else False
    if has_invr:
        a1 = d / det
        b1 = -b / det
        c1 = -c / det
        d1 = a / det
        # fraction
        if type(a1) == float and len(str(a1)) < 6: a1 = str(a1)
        else: t = m.Fraction(d,det); t.simplify; a1 = f"{t.a}/{t.b}" if t.b != 1 else t.a
        if type(b1) == float and len(str(b1)) < 6: b1 = str(b1)
        else: t = m.Fraction(-b,det); t.simplify; b1 = f"{t.a}/{t.b}" if t.b != 1 else t.a
        if type(c1) == float and len(str(c1)) < 6: c1 = str(c1)
        else: t = m.Fraction(-c,det); t.simplify; c1 = f"{t.a}/{t.b}" if t.b != 1 else t.a
        if type(d1) == float and len(str(d1)) < 6: d1 = str(d1)
        else: t = m.Fraction(a,det); t.simplify; d1 = f"{t.a}/{t.b}" if t.b != 1 else t.a


    # Format width
    width = max([len(str(i)) for i in [a,b,c,d]])
    embed = discord.Embed(
        title="此矩陣有反矩陣" if has_invr else "此矩陣沒有反矩陣",
        description=
        f"原矩陣：\n⌈{a: {width}d} {b: {width}d}⌉\n⌊{c: {width}d} {d: {width}d}⌋",
        color=settings.Colors.math
    )
    if has_invr:
        embed.description += f"\n反矩陣：\n⌈{a1} {b1}⌉\n⌊{c1} {d1}⌋"
    await interaction.response.send_message(embed=embed)


# --- MatrixMultiply window ---
class MatrixMultiply(discord.ui.Modal, title="矩陣乘法"):
    a = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="矩陣A",
        required=True,
        placeholder="請輸入矩陣，每一個數值以空格隔開，使用Enter換行"
    )

    b = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="矩陣B",
        required=True,
        placeholder="請輸入矩陣，每一個數值以空格隔開，使用Enter換行"
    )

    async def on_submit(self, interaction: discord.Interaction):
        # matrix a
        str_a: str = self.a.value
        mtx_a = str_a.split("\n")
        for i in range(len(mtx_a)): mtx_a[i] = mtx_a[i].split(" ")
        for i in range(len(mtx_a)):
            for j in range(len(mtx_a[i])):
                try: mtx_a[i][j] = int(mtx_a[i][j])
                except: await interaction.response.send_message(f"錯誤：{mtx_a[i][j]}不是整數，請再試一次")
        # matrix b
        str_b: str = self.b.value
        mtx_b = str_b.split("\n")
        for i in range(len(mtx_b)): mtx_b[i] = mtx_b[i].split(" ")
        for i in range(len(mtx_b)):
            for j in range(len(mtx_b[i])):
                try: mtx_b[i][j] = int(mtx_b[i][j])
                except: await interaction.response.send_message(f"錯誤：{mtx_b[i][j]}不是整數，請再試一次")
        # multiply            

    async def on_error(self, interaction: discord.Interaction, error):
        print(error)  # prints error


# --- Command: mtxmtply ---
@app_commands.command(name="mtxmtply", description="[矩陣] 矩陣相乘")
@app_commands.describe()
async def mtxmtply(interaction: discord.Interaction):
    await interaction.response.send_modal(MatrixMultiply())
