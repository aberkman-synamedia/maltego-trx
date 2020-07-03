from maltego_trx.oauth import MaltegoOauth

okta_ciphertoken = "pZ598ZEZ7EwpBQSOJSvCZJKkcWhtbX95K7Q0f0hwbk93O+xaUB4/NegK3r54PH1NReis/Jgt4UbGc5oCuU+R7UDM1icoDUmyCmV1U78iqjHElPdDBHlxPrl2zoXBwcU1iFbukDNy49Xghy3cwwqhmEXg/FKnYUlBQl6jdf06kE1pwfHiRgF5NrJISAD7eCmUybqiAVRDW4lbLeMGk/uSrrCpDQBxd2Em/sYKBzqO87pQRPLll23G9KNxyVinHQksGgc+dI0OPYv9EQcUs7g1JFraUKUeFjHAf/OyGGrp6WH84nGqG35afkH9xsDmySBb5DZWRjef8DzSd7oRagoGq3wKBHDh700mMKf/YkR8L9cK4l1w4yNh7EfIVlCWD5yWJUx4a1lN9CvJmFs7N9A903spVVGeP8avz50raWFb5g/4XhtIpei4ylVFi49dDeVjgb0BR0I4vuU7VDmcwFweAtSfclPb5Xfp98zI9yXnr8DB31gmzf3DIkVFIIFLxZe0gG+BSIEmC7/z0L7J+YvIqoGDq8jC0Ehe9IVXYfK1yluWAsbwj62rNAzkPVSe5l+FMQFrQRXpxZFBMXzphqRAhyYKfGNX/tocoMJoLFp8O3PBRC0kIHjTNaSX8KpftNYWreEdZx6wjk2n2eeOXM5nVeSOx4uoIifRe4NUV7VYzbGm3FSRc0k1HZIGHwn1WTvn95U3crvwFN86N3k41JU+0kzSpsLxy+Y63VfPxYTbRUET/wIOf0NTfG96QCPtVKkdVh9aTqnhaN0TpGoaZQEjUqpURxbj+8mT3g6MI4vOC9Qr6vw2wIkvzehr/yKxh6vsnfUUw8UJ1YtlZI7exPsHyFLUr2J3VvpDsaemRcn1KY/uHJZ3MMHK9GNciLA6Skw8SL38mw1tJJZ1h1bMMk1IYgBZLe2ZSXXyv7JaDPq/WJmHWDaIalmXE1cKMA56qMgYGdHxs3Pai5nwEtzIGVS1OcuMnBF6sOMMBTKSFAJmlcYo8NGwjKqe/yy1cVJZe7Ucv/jy/IS3AdE1my8cDya92jDsxifsaONQMm6YIs54SIA=$f7TU33wTTxYFtbVnwJeGGw==$c64l75qukq+980EkB1tQZKEicryt6HBB0IOjeMSRQmLOYCQpTcaXlPRJ3QdS+DfRocor7OL36wLAooRqz1IaN4QQ5+6Wx5reEXFVgKtaDX777I046DM5QU3Jf+iibSbm3mXYMw0z+OknbXyGLnc7ceSaPTJdP1LkCGQ75fLMXHCLWSpqwOKHOBhqyQGwrYlj2WxPzmOfAMaIkjKZIQWzoGjrYRzwkNCQbxykJcwD5TVuVDwAHyp84zcvW0WWoUZ+rrrooJwuJJQEdiTwLZsseqklXRNso4e5eFQwH49T9IDPHkKfVusu6rLiMNgFyc18rFR1d/BYLXBu7uzMAuvQ8wZdcOtJYx+JLJmOaPI65ymGNFTpwTHYnDBTXmpW0qX2dtEglAERw1nrdl94fwsa+I/iw3H7VIivqRF3pAchfvdNF75MIEm6XH2UXY/sZD7zjMdxxwKQiaEg2bpLd2mEtqsLc0mTq/zd03ZLEUnzXsXlp8brCfDgjoVsZAJH+ElQ6wr3dxzRMlDIxWWBYFcv8LnGVQk/Vciqtee780Yh/lgttv06kyXz81dIWjumz8TqV2eV9ZpP/YxTnNzAa91fleGNah/IKhMOV8PsGy2uOnHRiUL218p1T6+Cm9B2kmL1C/2MM3080NjJVWIfqYsyTGPbR+hURK0RB/oteG5QWPs="
private_key_path = "test_private_key.pem"


def testOktaDecrypt():
    decrypted_linkedIn_token = MaltegoOauth.decrypt_secrets(private_key_path, okta_ciphertoken)['token']
    expected_token = "eyJraWQiOiJ4ZzEyMmNZMXQ0NU5GM2l5YlUzUF9tWGluYkxEXzVrRHFwMkQ0VEl2RGd3IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULklldnVNcXNJNDFqMURldEdPU1N2Q2VoNlI5eUxEQ0EydFBJdl9FZ3hDU3ciLCJpc3MiOiJodHRwczovL2Rldi02MTcyNDUub2t0YS5jb20vb2F1dGgyL2RlZmF1bHQiLCJhdWQiOiJhcGk6Ly9kZWZhdWx0IiwiaWF0IjoxNTg5NzgzNjU0LCJleHAiOjE1ODk3ODcyNTQsImNpZCI6IjBvYTR1YTZ1YlJIeFRDTGg4NHg2IiwidWlkIjoiMDB1NHU0ZzA4SDFqYXQwVnA0eDYiLCJzY3AiOlsib3BlbmlkIl0sInN1YiI6InRtQG1hbHRlZ28uY29tIn0.dAZrIZ9NCIqIx3fr8_0EexYCzarj8CC4CvWpVgZQCvfhtV08tGnMdWN8yuzADYvJUSzDz_meqIMMUCaVOpYZ5vzepr3LZfT-Xn00KoaaRcHGLPowphvsEPkpimvJqgnRmWw0e0VTH5Pfg9eyl3o2UUUsDofM-RkJNjxB4Uf0D6IyZaCyl0s_KhcXGZuh7hDGoR76UcKaCqRXqmqnOZs_GoMPIoDS5NHIze0MOK6sgKr8uiLikIhdh481n8PyWzPX2XZLUNcjogqX280so6Ki24VBloyxt5VgAJ1gV-e9SDj-9QSdQohQNDDSHbgiO4s1TUlhFKIm5UQWUImdhSuv1w"
    assert decrypted_linkedIn_token == expected_token


def testReadKey():
    private_key = open(private_key_path).read()
    assert private_key.__sizeof__() == 3292


def testCipherSplit():
    encrypted_fields = okta_ciphertoken.split("$")
    assert len(encrypted_fields) == 3


def testToken_Field_Creation():
    encrypted_fields = okta_ciphertoken.split("$")
    aes_key = MaltegoOauth._rsa_decrypt(private_key_path, encrypted_fields[2])
    token = MaltegoOauth._aes_decrypt(aes_key, encrypted_fields[0])
    token_secret = MaltegoOauth._aes_decrypt(aes_key, encrypted_fields[1])
    token_fields = {
        "token": token,
        "token_secret": token_secret
    }
    decrypted_azure_token_dict = MaltegoOauth.decrypt_secrets(private_key_path, okta_ciphertoken)
    assert token_fields == decrypted_azure_token_dict
