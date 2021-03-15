import execjs
q = "哈哈哈"
with open('static/sign.js', 'r', encoding='utf-8') as f:
    ctx = execjs.compile(f.read())
    n = ctx.call('pro', q)
    sign_c = ctx.call('e', n)
    print(sign_c)
