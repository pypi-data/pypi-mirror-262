<h1 align="center">pyaes_util</h1>

- aes_util.py

aes非对称加密的各种封装方法，使用示例：

```python
key = '12223'
data = 'hc刺激啊四神聪骄傲i'
encrypt = encrypt_aes(data, key)
print(encrypt)
print(decrypt_aes(encrypt, key))
```
