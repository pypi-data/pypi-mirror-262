from src.SanauAutomationSDK.SanauAtomationSDK import SanauAutomationSDK
sasdk = SanauAutomationSDK('KZ', 'pbo.kz', '7nuLUYDYeQLyd3Rn')

print(sasdk.client.get_databases())
