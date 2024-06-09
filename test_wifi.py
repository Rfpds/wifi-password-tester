import subprocess

def check_permissions():
    try:
        # Tenta executar um comando básico do nmcli para verificar permissões
        result = subprocess.run(['nmcli', 'general', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Erro: Permissões insuficientes para executar comandos do nmcli.")
            print("Você precisa das seguintes permissões:")
            print("- Permissão para executar comandos de rede usando 'nmcli'.")
            print("- Acesso sudo para alterar configurações de rede.")
            ignore_warning = input("Você deseja ignorar este aviso e continuar? (s/n): ").strip().lower()
            if ignore_warning == 's':
                return True
            else:
                return False
        return True
    except Exception as e:
        print(f"Erro ao verificar permissões: {e}")
        return False

def test_wifi_password(network_identifier, password, use_mac=False):
    try:
        if use_mac:
            result = subprocess.run(
                ['nmcli', 'dev', 'wifi', 'connect', network_identifier, 'password', password, 'bssid', network_identifier],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            result = subprocess.run(
                ['nmcli', 'dev', 'wifi', 'connect', network_identifier, 'password', password],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode == 0 and 'successfully activated' in result.stdout.lower():
            return True
        else:
            print(f"Erro ao tentar a senha {password}: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Erro ao tentar a senha {password}: {e}")
        return False

def main():
    if not check_permissions():
        return

    network_name = input("Por favor, insira o nome da rede (ou pressione Enter para pular): ")
    ssid = input("Por favor, insira o SSID da rede (ou pressione Enter para pular): ")
    mac_address = input("Por favor, insira o endereço MAC da rede (ou pressione Enter para pular): ")

    if network_name:
        network_identifier = network_name
        use_mac = False
    elif ssid:
        network_identifier = ssid
        use_mac = False
    elif mac_address:
        network_identifier = mac_address
        use_mac = True
    else:
        print("Você deve fornecer pelo menos uma forma de identificação da rede (nome, SSID ou endereço MAC).")
        return

    choice = input("Você deseja usar senhas padrão (1) ou inserir suas próprias senhas (2)? Insira 1 ou 2: ")

    if choice == '1':
        passwords = [
            'teste1',
            'teste2',
            'teste3',
            # Adicione mais senhas conforme necessário
        ]

        for password in passwords:
            print(f'Testando senha: {password}')  # Informação de debug
            if test_wifi_password(network_identifier, password, use_mac):
                print(f'Senha encontrada: {password}')
                break
            else:
                print(f'Senha incorreta: {password}')
    elif choice == '2':
        while True:
            password = input("Por favor, insira a senha para tentar (ou pressione Enter para terminar): ")
            if not password:
                print("Finalizando tentativas.")
                break

            print(f'Testando senha: {password}')  # Informação de debug
            if test_wifi_password(network_identifier, password, use_mac):
                print(f'Senha encontrada: {password}')
                break
            else:
                print(f'Senha incorreta: {password}')
    else:
        print("Escolha inválida. Por favor, execute o script novamente e insira 1 ou 2.")

if __name__ == "__main__":
    main()
