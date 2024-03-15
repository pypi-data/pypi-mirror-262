# 南京大学统一认证登陆

从账号密码拿到 `CASTGC` cookie

```python
import nju_login_simple

response=nju_login.login('221223322','password')
castgc=response.cookies['CASTGC']
```
