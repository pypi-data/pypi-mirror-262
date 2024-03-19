from src.SanauAutomationSDK.SanauAtomationSDK import SanauAutomationSDK
sasdk = SanauAutomationSDK('KZ', 'pbo.kz', {'Access-Key': '7nuLUYDYeQLyd3Rn'})

print(sasdk.client.get_databases())
